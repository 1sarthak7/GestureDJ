# Real-time echo on MP3 streams is complex in Python.
# We simulate it by creating a slight volume lag logic or simple toggle flag
# for the UI to display, as Pygame Mixer doesn't support live DSP effects chain.

class EchoEffect:
    def __init__(self):
        self.enabled = False
        self.cooldown = 0
        
    def toggle(self):
        if self.cooldown == 0:
            self.enabled = not self.enabled
            self.cooldown = 30 # Frames
            return True
        return False
        
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def is_active(self):
        return self.enabled