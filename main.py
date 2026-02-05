import cv2
import pygame
import os
import sys

# Import local modules
from gestures.hand_tracker import HandTracker
from gestures.gesture_logic import GestureController
from ui.overlay import UIOverlay
from effects.scratch import ScratchEffect
from effects.filters import FilterController

def main():
    # 1. Initialize Audio Engine (Pygame)
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()

    # Verify songs exist
    song_a_path = os.path.join("songs", "track_a.mp3")
    song_b_path = os.path.join("songs", "track_b.mp3")

    if not os.path.exists(song_a_path) or not os.path.exists(song_b_path):
        print("❌ Error: Please place 'track_a.mp3' and 'track_b.mp3' in the 'songs/' folder.")
        return

    # Load Tracks as Sound objects to allow independent channel control
    print("Loading Audio...")
    track_a = pygame.mixer.Sound(song_a_path)
    track_b = pygame.mixer.Sound(song_b_path)

    channel_a = pygame.mixer.Channel(0)
    channel_b = pygame.mixer.Channel(1)

    # Start Playing (Loop indefinitely)
    channel_a.play(track_a, loops=-1)
    channel_b.play(track_b, loops=-1)
    
    # 2. Initialize Video & Logic
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) # Width
    cap.set(4, 720)  # Height

    tracker = HandTracker(max_hands=2)
    gesture_ctrl = GestureController()
    ui = UIOverlay()
    
    # Effects
    scratch_fx = ScratchEffect()
    filter_ctrl = FilterController()

    print("✅ System Ready. Press 'Q' to exit.")

    while True:
        success, img = cap.read()
        if not success:
            break

        # Flip image for mirror view
        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        # --- A. Hand Tracking ---
        img = tracker.find_hands(img)
        lm_list, _ = tracker.find_position(img) # Getting raw list for compatibility
        
        # We need to separate Left vs Right hands for logic
        # HandTracker returns a flat list for one hand in simple mode,
        # but for multi-hand, we need to extract properly.
        # Let's re-query the tracker object directly for clearer data
        
        right_hand_lms = []
        left_hand_lms = []

        if tracker.results.multi_hand_landmarks and tracker.results.multi_handedness:
            for idx, hand_handedness in enumerate(tracker.results.multi_handedness):
                label = hand_handedness.classification[0].label # "Left" or "Right"
                landmarks = tracker.results.multi_hand_landmarks[idx]
                
                # Convert landmarks to pixel coordinates list
                lm_data = []
                for i, lm in enumerate(landmarks.landmark):
                    lm_data.append([i, int(lm.x * w), int(lm.y * h)])

                if label == "Right":
                    right_hand_lms = lm_data
                else:
                    left_hand_lms = lm_data

        # --- B. Process Gestures ---
        controls = gesture_ctrl.process_gestures(img.shape, right_hand_lms, left_hand_lms)

        # --- C. Update Audio Engine ---
        
        # 1. Master Volume (Hand Distance)
        master_vol = controls.get('volume')
        if master_vol is None: master_vol = 0.5
        
        # 2. Crossfader
        xfade = controls.get('crossfade')
        if xfade is None: xfade = 0.5
        
        # Calculate individual channel volumes
        # Linear crossfade logic
        vol_a = (1.0 - xfade) * master_vol
        vol_b = xfade * master_vol
        
        # 3. Apply Filter Logic (Simulated by EQ volume adjustments)
        filter_ctrl.update(controls.get('filter_val'))
        filter_status = filter_ctrl.get_status_text()
        controls['filter_status'] = filter_status # Pass to UI
        
        # Bass Drop Logic (Max Volume momentarily)
        if controls.get('bass_drop'):
            vol_a = 1.0
            vol_b = 1.0
        
        # 4. Scratch Effect
        is_scratching = controls.get('scratch', False)
        scratch_fx.apply(channel_a, channel_b, is_scratching)

        # Set Volumes
        channel_a.set_volume(max(0.0, min(1.0, vol_a)))
        channel_b.set_volume(max(0.0, min(1.0, vol_b)))

        # --- D. UI Rendering ---
        ui.update(img, controls)

        # Show FPS
        cv2.imshow("GestureDJ - AI Mixer", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()