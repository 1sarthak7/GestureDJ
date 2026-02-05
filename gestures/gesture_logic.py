import math
import numpy as np
from collections import deque

class GestureController:
    def __init__(self):
        # Smoothing factors (Exponential Moving Average)
        self.alpha = 0.2
        self.prev_vol_dist = 0
        self.prev_crossfader_x = 0.5  # Center (0.0 to 1.0)
        self.prev_filter_y = 0.5
        
        # Scratch detection history
        self.scratch_history = deque(maxlen=10)
        self.is_scratching = False
        
        # Cooldowns to prevent flickering triggers
        self.play_pause_cooldown = 0
        
    def get_distance(self, p1, p2):
        x1, y1 = p1[1], p1[2]
        x2, y2 = p2[1], p2[2]
        return math.hypot(x2 - x1, y2 - y1)

    def process_gestures(self, img_shape, right_hand_lms, left_hand_lms):
        """
        Returns a dictionary of control values:
        {
            'volume': 0.0-1.0,
            'crossfade': 0.0-1.0,
            'scratch': bool,
            'filter_val': 0.0-1.0, # High/Low pass
            'play_pause': bool,    # Trigger
            'bass_drop': bool      # Trigger
        }
        """
        controls = {
            'volume': None,
            'crossfade': None,
            'scratch': False,
            'filter_val': None,
            'play_pause': False,
            'bass_drop': False
        }
        
        h, w, _ = img_shape

        # --- RIGHT HAND (Master Control) ---
        if right_hand_lms:
            # 1. Volume: Distance between Thumb Tip (4) and Index Tip (8)
            length = self.get_distance(right_hand_lms[4], right_hand_lms[8])
            # Normalize: ~20px is closed, ~200px is open (adjust based on camera)
            vol_norm = np.interp(length, [20, 200], [0, 1])
            # Smooth
            self.prev_vol_dist = (self.alpha * vol_norm) + ((1 - self.alpha) * self.prev_vol_dist)
            controls['volume'] = round(self.prev_vol_dist, 2)

            # 2. Crossfader: X position of Wrist (0)
            wrist_x = right_hand_lms[0][1]
            cross_norm = np.interp(wrist_x, [0, w], [0, 1])
            # Invert X because camera is mirrored
            cross_norm = 1 - cross_norm 
            self.prev_crossfader_x = (self.alpha * cross_norm) + ((1 - self.alpha) * self.prev_crossfader_x)
            controls['crossfade'] = round(self.prev_crossfader_x, 2)

        # --- LEFT HAND (Effects & Transport) ---
        if left_hand_lms:
            # 3. Filter/Effects: Y position of Wrist
            wrist_y = left_hand_lms[0][2]
            filter_norm = np.interp(wrist_y, [0, h], [1, 0]) # Up is High, Down is Low
            self.prev_filter_y = (self.alpha * filter_norm) + ((1 - self.alpha) * self.prev_filter_y)
            controls['filter_val'] = round(self.prev_filter_y, 2)

            # 4. Play/Pause: Open Palm vs Closed (Fingers extended)
            # Check if tips are above PIP joints (simple open hand check)
            fingers = []
            # Thumb (is tip to the left/right of ip depending on hand? skip thumb for simplicity)
            # Index (8 > 6), Middle (12 > 10), Ring (16 > 14), Pinky (20 > 18)
            # Note: Y coordinates increase downwards
            
            is_open = (left_hand_lms[8][2] < left_hand_lms[6][2] and 
                       left_hand_lms[12][2] < left_hand_lms[10][2] and 
                       left_hand_lms[16][2] < left_hand_lms[14][2] and 
                       left_hand_lms[20][2] < left_hand_lms[18][2])

            if self.play_pause_cooldown > 0:
                self.play_pause_cooldown -= 1
            
            # Simple Gesture: If hand is very open and high up
            if is_open and self.play_pause_cooldown == 0:
                 # We trigger play/pause only on a specific "Stop" gesture? 
                 # Let's use Index+Middle up only (Peace sign) for Pause/Play toggle to be distinct
                 pass 

            # 5. Beat Drop: Closed Fist
            is_fist = (left_hand_lms[8][2] > left_hand_lms[6][2] and 
                       left_hand_lms[12][2] > left_hand_lms[10][2] and 
                       left_hand_lms[16][2] > left_hand_lms[14][2] and 
                       left_hand_lms[20][2] > left_hand_lms[18][2])
            
            if is_fist:
                controls['bass_drop'] = True

            # 6. Scratch: Circular motion of Index Finger (8)
            cx, cy = left_hand_lms[8][1], left_hand_lms[8][2]
            self.scratch_history.append((cx, cy))
            if len(self.scratch_history) >= 5:
                # Calculate variance in movement
                # A circle has high variance in both X and Y
                arr = np.array(self.scratch_history)
                std_x = np.std(arr[:, 0])
                std_y = np.std(arr[:, 1])
                
                # If movement is erratic/circular enough
                if std_x > 15 and std_y > 15: 
                    controls['scratch'] = True

        return controls