# C
import pygame

COLOR = (32, 178, 170)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_YELLOW = (255, 223, 0)
C_CYAN = (0, 128, 128)
C_GREEN = (0, 128, 0)

# E
EVENT_ENEMY = pygame.USEREVENT + 1
ENTITY_SPEED = {
    'Level1Back1': 0,
    'Level1Back2': 3,
    'Level1Back3': 2,
    'Level1Back4': 2,
    'Level1Back5': 3,
    'Player': 4,
    'Enemy1': 3,
    'Enemy2': 3,
    'PlayerShot': 3,
    'Enemy1Shot': 7,
    'Enemy2Shot': 5,

}
ENTITY_HEALTH = {
    'Level1Back1': 999,
    'Level1Back2': 999,
    'Level1Back3': 999,
    'Level1Back4': 999,
    'Level1Back5': 999,
    'Player': 300,
    'PlayerShot': 1,
    'Enemy1': 50,
    'Enemy2': 50,
    'Enemy1Shot': 1,
    'Enemy2Shot': 1,
}

ENTITY_SHOT_DELAY = {
    'Enemy1': 5,  # Intervalo maior para Enemy1
    'Enemy2': 3,  # Intervalo maior para Enemy2
    #'Player': 5,  # Intervalo menor para Player
}

ENTITY_DAMAGE = {
    'Level1Back1': 0,
    'Level1Back2': 0,
    'Level1Back3': 0,
    'Level1Back4': 0,
    'Level1Back5': 0,
    'Player': 1,
    'PlayerShot': 10,
    'Enemy1': 1,
    'Enemy2': 1,
    'Enemy1Shot': 20,
    'Enemy2Shot': 20,

}

ENTITY_SCORE = {
    'Level1Back1': 0,
    'Level1Back2': 0,
    'Level1Back3': 0,
    'Level1Back4': 0,
    'Level1Back5': 0,
    'Player': 0,
    'PlayerShot': 0,
    'Enemy1': 100,
    'Enemy2': 100,
    'Enemy1Shot': 0,
    'Enemy2Shot': 0,
}

# S
SPAWN_TIME = 4000

# M
MENU_OPTION = ('NEW GAME', 'SCORE', 'EXIT')

# P
PLAYER_KEY_UP = {'Player1': pygame.K_UP}
PLAYER_KEY_DOWN = {'Player1': pygame.K_DOWN}
PLAYER_KEY_LEFT = {'Player1': pygame.K_LEFT}
PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT}
PLAYER_KEY_SHOOT = {
    "Player1": pygame.K_SPACE,
    "Player": pygame.K_SPACE,
}

# W
WIN_WIDTH = 576
WIN_HEIGHT = 324
