import pygame

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # We'll create simple sound effects using pygame's built-in synthesis
        # For a real game, you'd load actual sound files
        
        self.sounds_enabled = True
        self.music_enabled = True
        
        # Create simple beep sounds (we'll generate them)
        self.sounds = {
            'lane_change': self.create_beep(400, 100),
            'collect_money': self.create_beep(600, 150),
            'collect_multiplier': self.create_chord([600, 800, 1000], 200),
            'hit_obstacle': self.create_beep(200, 300),
            'warning': self.create_beep(300, 200),
            'game_over': self.create_beep(150, 500)
        }
        
    def create_beep(self, frequency, duration):
        """Create a simple beep sound"""
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate / 1000))
        
        # Generate sine wave
        import numpy as np
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2 ** (16 - 1) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            value = int(round(max_sample * 0.3 * np.sin(2 * np.pi * frequency * t)))
            buf[i][0] = value
            buf[i][1] = value
        
        sound = pygame.sndarray.make_sound(buf)
        return sound
    
    def create_chord(self, frequencies, duration):
        """Create a chord with multiple frequencies"""
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate / 1000))
        
        import numpy as np
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2 ** (16 - 1) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            value = 0
            for freq in frequencies:
                value += np.sin(2 * np.pi * freq * t)
            value = int(round(max_sample * 0.2 * value / len(frequencies)))
            buf[i][0] = value
            buf[i][1] = value
        
        sound = pygame.sndarray.make_sound(buf)
        return sound
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sounds_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Fail silently if sound doesn't work
    
    def toggle_sounds(self):
        """Toggle sound effects on/off"""
        self.sounds_enabled = not self.sounds_enabled
        return self.sounds_enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        return self.music_enabled
