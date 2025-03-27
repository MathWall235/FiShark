import pygame
from Code.Score import Score
from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Level import Level
from Code.Menu import Menu
from Code.GameOver import GameOver
from Code.GameState import GameState  # Nova importação


class Game:
    game_over = False  # Mantenha esta declaração no escopo da classe

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        GameState.game_over = False  # Resetar estado ao iniciar

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:  # "Start"
                player_score = [0]
                current_level = 'Level1'
                while True:
                    level = Level(self.window, current_level, menu_return, player_score)
                    level_return = level.run(player_score)

                    # Verifica se houve game over por morte do jogador ou falha no nível
                    if not level_return or Game.game_over:
                        game_over = GameOver(self.window)
                        choice_index = game_over.run()
                        Game.game_over = False  # Reseta o flag

                        if choice_index == 0:  # Reiniciar
                            player_score = [0]
                            current_level = 'Level1'
                        else:  # Voltar ao Menu
                            break
                    else:
                        # Lógica de progressão de nível
                        if current_level == 'Level1':
                            current_level = 'Level2'
                        else:
                            score.save_score(menu_return, player_score)
                            break
                    if GameState.game_over or not level_return:
                        game_over = GameOver(self.window)
                        choice_index = game_over.run()
                        GameState.game_over = False  # Resetar flag
            elif menu_return == MENU_OPTION[1]:  # "Score"
                score.show_score()

            elif menu_return == MENU_OPTION[2]:  # "Quit"
                pygame.quit()
                quit()