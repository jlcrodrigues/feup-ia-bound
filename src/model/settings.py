class Settings:
    """Settings class"""
    def __init__(self, music_volume=0.4, sound_effects_volume=0.4, board_size=1, bot_delay=2, skin='default'):
        self.music_volume = music_volume
        self.sound_effects_volume = sound_effects_volume
        self.board_size = board_size
        self.bot_delay = bot_delay
        self.skin = skin
        
    def bot_delay_in_sec(self):
        """Return the bot delay in seconds."""
        if self.bot_delay == 1:
            return 0.1
        elif self.bot_delay == 2:
            return 1
        elif self.bot_delay == 3:
            return 2