# const.py
import pygame
from pygame.examples.grid import WINDOW_WIDTH

# CORES
COLOR = (32, 178, 170)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_YELLOW = (255, 223, 0)
C_CYAN = (0, 128, 128)
C_GREEN = (0, 128, 0)
C_RED = (255, 0, 0)
C_DARK_RED = (200, 0, 0)

# EVENTOS
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2

# DADOS DE VELOCIDADE
ENTITY_SPEED = {
    'Level1Back1': 0,
    'Level1Back2': 4,
    'Level1Back3': 3,
    'Level1Back4': 3,
    'Level1Back5': 4,
    'Level2Back1': 0,
    'Level2Back2': 3,
    'Level2Back3': 2,
    'Level2Back4': 2,
    'Level2Back5': 3,
    'Level2Back6': 3,
    'Player': 4,
    'Enemy1': 3,
    'Enemy2': 3,
    'PlayerShot': 3,
    'Enemy1Shot': 7,
    'Enemy2Shot': 5,
}

# CONFIGURAÇÕES AJUSTÁVEIS
PLAYER_HEALTH = 400
ENEMY_ATTACK_SPEED = 25  # Delay entre ataques dos inimigos
LEVEL_DURATION = 30000   # Duração do nível em milissegundos

ENTITY_HEALTH = {
    'Level1Back1': 999,
    'Level1Back2': 999,
    'Level1Back3': 999,
    'Level1Back4': 999,
    'Level1Back5': 999,
    'Level2Back1': 999,
    'Level2Back2': 999,
    'Level2Back3': 999,
    'Level2Back4': 999,
    'Level2Back5': 999,
    'Level2Back6': 999,
    'Player': 500,
    'PlayerShot': 1,
    'Enemy1': 50,
    'Enemy2': 50,
    'Enemy1Shot': 1,
    'Enemy2Shot': 1,
}

ENTITY_SHOT_DELAY = {
    'Enemy1': 25,
    'Enemy2': 25,
}

ENTITY_DAMAGE = {
    'Level1Back1': 0,
    'Level1Back2': 0,
    'Level1Back3': 0,
    'Level1Back4': 0,
    'Level1Back5': 0,
    'Level2Back1': 0,
    'Level2Back2': 0,
    'Level2Back3': 0,
    'Level2Back4': 0,
    'Level2Back5': 0,
    'Level2Back6': 0,
    'Player': 1,
    'PlayerShot': 50,
    'Enemy1': 1,
    'Enemy2': 1,
    'Enemy1Shot': 30,
    'Enemy2Shot': 30,
}

ENTITY_SCORE = {
    'Level1Back1': 0,
    'Level1Back2': 0,
    'Level1Back3': 0,
    'Level1Back4': 0,
    'Level1Back5': 0,
    'Level2Back1': 0,
    'Level2Back2': 0,
    'Level2Back3': 0,
    'Level2Back4': 0,
    'Level2Back5': 0,
    'Level2Back6': 0,
    'Player': 0,
    'PlayerShot': 0,
    'Enemy1': 100,
    'Enemy2': 100,
    'Enemy1Shot': 0,
    'Enemy2Shot': 0,
}

# MENU
MENU_OPTION = ('NOVO JOGO', 'SCORE', 'CONFIGURAÇÕES', 'SAIR')

# CONTROLES
PLAYER_KEY_UP = {'Player1': pygame.K_UP}
PLAYER_KEY_DOWN = {'Player1': pygame.K_DOWN}
PLAYER_KEY_LEFT = {'Player1': pygame.K_LEFT}
PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT}
PLAYER_KEY_SHOOT = {
    "Player1": pygame.K_SPACE,
    "Player": pygame.K_SPACE,
}

# OUTROS
SPAWN_TIME = 350
TIMEOUT_STEP = 100  # 100 mls
TIMEOUT_LEVEL = 30000  # 30s
WIN_WIDTH = 576
WIN_HEIGHT = 324

SCORE_POS = {
    'Title': (288, 30),
    'EnterName': (WIN_WIDTH / 2, 80),
    'Label': (WIN_WIDTH / 2, 90),
    'Name': (WIN_WIDTH / 2, 110),
    0: (WIN_WIDTH / 2, 110),
    1: (WIN_WIDTH / 2, 130),
    2: (WIN_WIDTH / 2, 150),
    3: (WIN_WIDTH / 2, 170),
    4: (WIN_WIDTH / 2, 190),
    5: (WIN_WIDTH / 2, 210),
    6: (WIN_WIDTH / 2, 230),
    7: (WIN_WIDTH / 2, 250),
    8: (WIN_WIDTH / 2, 270),
    9: (WIN_WIDTH / 2, 290),
}