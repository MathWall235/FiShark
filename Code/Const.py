# C
import pygame

COLOR = (32, 178, 170)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_YELLOW = (255, 223, 0)

# E
EVENT_ENEMY = pygame.USEREVENT +1
ENTITY_SPEED = {
    'Level1Back1': 0,
    'Level1Back2': 3,
    'Level1Back3': 2,
    'Level1Back4': 3,
    'Level1Back5': 4,
    'Player': 4,
    'Enemy1': 3,
    'Enemy2': 4,
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
    'Enemy1': 6,  # Intervalo maior para Enemy1
    'Enemy2': 4,  # Intervalo maior para Enemy2
}



#S
SPAWN_TIME = 4000


# M
MENU_OPTION = ('NEW GAME', 'SCORE', 'EXIT')

#P
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
