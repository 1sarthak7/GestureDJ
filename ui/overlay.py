import cv2
import numpy as np

class UIOverlay:
    def __init__(self):
        # Colors (BGR)
        self.color_base = (50, 50, 50)
        self.color_active = (0, 255, 217)  # Cyan
        self.color_text = (255, 255, 255)
        self.color_warn = (0, 0, 255)

    def draw_bar(self, img, x, y, w, h, value, label):
        # Background
        cv2.rectangle(img, (x, y), (x + w, y + h), self.color_base, -1)
        # Fill
        fill_w = int(w * value)
        cv2.rectangle(img, (x, y), (x + fill_w, y + h), self.color_active, -1)
        # Border
        cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), 2)
        # Label
        cv2.putText(img, f"{label}: {int(value*100)}%", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_text, 2)

    def draw_crossfader(self, img, x, y, w, h, value):
        cv2.rectangle(img, (x, y), (x + w, y + h), self.color_base, -1)
        # Knob
        knob_x = int(x + (w * value))
        cv2.circle(img, (knob_x, y + h//2), h//2 + 5, (0, 165, 255), -1)
        cv2.line(img, (x + w//2, y), (x + w//2, y+h), (100,100,100), 2) # Center marker
        
        cv2.putText(img, "CROSSFADER", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_text, 2)
        cv2.putText(img, "Track A", (x - 80, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1)
        cv2.putText(img, "Track B", (x + w + 10, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1)

    def draw_status(self, img, effects_status):
        y_start = 50
        for key, val in effects_status.items():
            color = self.color_active if val else (100, 100, 100)
            text = f"{key}: {'ON' if val else 'OFF'}"
            if isinstance(val, str): text = f"{key}: {val}"
            
            cv2.putText(img, text, (20, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_start += 35

    def update(self, img, controls):
        h, w, c = img.shape
        
        # Bottom area overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, h-150), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

        # Draw Crossfader (Bottom Center)
        cf_val = controls.get('crossfade', 0.5) or 0.5
        self.draw_crossfader(img, w//2 - 150, h - 60, 300, 20, cf_val)

        # Draw Volume (Right Side)
        vol_val = controls.get('volume', 0.5) or 0.5
        self.draw_bar(img, w - 50, h - 300, 20, 200, vol_val, "VOL")
        
        # Draw Effect Status
        status = {
            "SCRATCH": controls.get('scratch', False),
            "BASS DROP": controls.get('bass_drop', False),
            "FILTER": controls.get('filter_status', "FLAT")
        }
        self.draw_status(img, status)

        return img