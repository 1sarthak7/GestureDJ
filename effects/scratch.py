import random

class ScratchEffect:
    def __init__(self):
        self.active = False
        self.scratch_timer = 0
        
    def apply(self, channel_a, channel_b, is_triggered):
        """
        Simulates scratching by rapidly gating volume.
        True DSP scratching requires raw buffer manipulation which causes
        latency in Pygame, so we use a 'Stutter' technique.
        """
        if is_triggered:
            self.active = True
            # Random stutter
            if random.random() > 0.5:
                channel_a.pause()
                channel_b.pause()
            else:
                channel_a.unpause()
                channel_b.unpause()
        elif self.active and not is_triggered:
            # Cleanup when gesture stops
            self.active = False
            channel_a.unpause()
            channel_b.unpause()
            
        return self.active