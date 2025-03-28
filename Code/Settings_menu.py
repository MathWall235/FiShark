# settings_menu.py
import pygame
import pygame_menu
from Code.Const import PLAYER_HEALTH, ENEMY_ATTACK_SPEED, LEVEL_DURATION

class SettingsMenu:
    def __init__(self, window):
        self.window = window
        self.player_health = PLAYER_HEALTH
        self.enemy_attack_speed = ENEMY_ATTACK_SPEED
        self.level_duration = LEVEL_DURATION

        self.menu = pygame_menu.Menu('Configurações', 400, 300,
                                     theme=pygame_menu.themes.THEME_DARK)

        self.menu.add.range_slider('Saúde do Player', self.player_health, (100, 1000), 10,
                                   onchange=self.set_player_health)
        self.menu.add.range_slider('Velocidade de Ataque', self.enemy_attack_speed, (5, 50), 1,
                                   onchange=self.set_enemy_attack_speed)
        self.menu.add.range_slider('Duração do Nível (s)', self.level_duration / 1000, (10, 60), 1,
                                   onchange=self.set_level_duration)
        self.menu.add.button('Voltar', pygame_menu.events.BACK)

    def set_player_health(self, value):
        self.player_health = int(value)

    def set_enemy_attack_speed(self, value):
        self.enemy_attack_speed = int(value)

    def set_level_duration(self, value):
        self.level_duration = int(value * 1000)

    def run(self):
        self.menu.mainloop(self.window)
        return self.player_health, self.enemy_attack_speed, self.level_duration
