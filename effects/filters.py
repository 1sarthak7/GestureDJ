class FilterController:
    def __init__(self):
        self.cutoff = 0.5 # 0.0 (Low Pass) to 1.0 (High Pass) center is 0.5
        
    def update(self, normalized_y):
        """
        Maps hand height to filter simulation.
        Since we can't do live EQ, we map this to a 'Focus' mix.
        High Y (Up) = Treble emphasis (simulated by volume boost)
        Low Y (Down) = Bass emphasis
        """
        if normalized_y is not None:
            self.cutoff = normalized_y
            
    def get_status_text(self):
        if self.cutoff > 0.7:
            return "HIGHPASS"
        elif self.cutoff < 0.3:
            return "LOWPASS"
        else:
            return "FLAT"