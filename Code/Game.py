import pygame
from Code.Score import Score
from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Level import Level
from Code.Menu import Menu
from Code.GameOver import GameOver
from Code.GameState import GameState  # Nova importação
from Code.Config_Screen import ConfigScreen
import Code.Const as Const  # Para atualizar as configurações


class Game:
    game_over = False  # Flag global de game over

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        GameState.game_over = False  # Resetar estado ao iniciar

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:  # "NOVO JOGO"
                player_score = [0]
                current_level = 'Level1'
                while True:
                    level = Level(self.window, current_level, menu_return, player_score)
                    level_return = level.run(player_score)

                    # Verifica condições de Game Over
                    if not level_return or Game.game_over or GameState.game_over:
                        game_over = GameOver(self.window)
                        choice_index = game_over.run()

                        # Reseta os flags de Game Over
                        Game.game_over = False
                        GameState.game_over = False

                        if choice_index == 0:  # Reiniciar
                            player_score = [0]
                            current_level = 'Level1'
                        else:  # Voltar ao Menu
                            break
                    else:
                        # Progressão de nível
                        if current_level == 'Level1':
                            current_level = 'Level2'
                        else:
                            score.save_score(menu_return, player_score)
                            break

            elif menu_return == MENU_OPTION[1]:  # "SCORE"
                score.show_score()

            elif menu_return == "CONFIGURAÇÕES":
                config = ConfigScreen(self.window)
                new_player_health, new_enemy_attack_speed, new_level_duration = config.run()
                # Atualiza as configurações globais
                Const.PLAYER_HEALTH = new_player_health
                Const.ENEMY_ATTACK_SPEED = new_enemy_attack_speed
                Const.LEVEL_DURATION = new_level_duration
                # Propaga as mudanças para os dicionários utilizados na criação de entidades
                Const.ENTITY_HEALTH['Player'] = new_player_health
                if 'Enemy1' in Const.ENTITY_SHOT_DELAY:
                    Const.ENTITY_SHOT_DELAY['Enemy1'] = new_enemy_attack_speed
                if 'Enemy2' in Const.ENTITY_SHOT_DELAY:
                    Const.ENTITY_SHOT_DELAY['Enemy2'] = new_enemy_attack_speed

            elif menu_return == MENU_OPTION[3] or menu_return == "SAIR":
                pygame.quit()
                quit()


if __name__ == "__main__":
    Game().run()