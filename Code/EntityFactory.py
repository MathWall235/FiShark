# entityfactory.py
import random
from Code.Background import Background
from Code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED
from Code.Player import Player
from Code.Enemy import Enemy

class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'Level1Back':
                list_back = []
                for i in range(1, 6):  # Imagens do Level 1
                    list_back.append(Background(f'Level1Back{i}', (0, 0)))
                    list_back.append(Background(f'Level1Back{i}', (WIN_WIDTH, 0)))
                return list_back
            case 'Level2Back':
                list_back = []
                for i in range(1, 6):  # Imagens do Level 2
                    list_back.append(Background(f'Level2Back{i}', (0, 0)))
                    list_back.append(Background(f'Level2Back{i}', (WIN_WIDTH, 0)))
                return list_back
            case 'Player':
                return Player('Player', (10, WIN_HEIGHT / 2))
            case 'Enemy1':
                return Enemy('Enemy1', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))
            case 'Enemy2':
                return Enemy('Enemy2', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))
