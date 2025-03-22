from Code.Background import Background
from Code.Const import WIN_WIDTH


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:
            case 'Level1Back':
                list_back = []
                for i in range(1, 6):
                    list_back.append(Background(f'Level1Back{i}', (0,0)))
                    list_back.append(Background(f'Level1Back{i}', (WIN_WIDTH, 0)))
                return list_back
