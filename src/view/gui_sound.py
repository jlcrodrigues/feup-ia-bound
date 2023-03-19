import pygame

FADEOUT = 1000 #fadeout delay
LOOP = -1

class GUISound:
    """
    Play music and sound effects.
    """
    def __init__(self):
        self.menu_music = pygame.mixer.Sound("../assets/sound/music/menu.mp3")
        self.game_music = pygame.mixer.Sound("../assets/sound/music/game.mp3")
        self.music = self.menu_music
        
        self.music_volume = 0.5
        self.effects_volume = 0.5

        self.play_music()
    
    def toggle_menu(self):
        """Start playing the menu music."""
        self.music.fadeout(FADEOUT)
        self.music = self.menu_music
        self.play_music()

    def toggle_game(self):
        """Start playing the game music."""
        self.music.fadeout(FADEOUT)
        self.music = self.game_music
        self.play_music()

    def play_music(self):
        """Play the current music."""
        self.music.set_volume(self.music_volume)
        self.music.play(LOOP)

    def play_effect(self, effect):
        """Play a sound effect."""
        move = pygame.mixer.Sound(f"../assets/sound/effects/{effect}.mp3")
        move.set_volume(self.effects_volume)
        move.play()
