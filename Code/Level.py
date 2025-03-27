import random
import pygame
import sys
from typing import List
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory
from Code.Const import WIN_WIDTH, COLOR, MENU_OPTION, C_WHITE, WIN_HEIGHT, C_BLACK, C_YELLOW, EVENT_ENEMY, SPAWN_TIME, \
    C_GREEN, EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL, C_DARK_RED
from Code.EntityMediator import EntityMediator
from Code.Player import Player
from Code.Enemy import Enemy


class Level:
    def __init__(self, window, name, menu_option, player_score: list[int]):
        self.window = window
        self.name = name
        self.menu_option = menu_option
        self.entity_list: List[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Back'))
        player = EntityFactory.get_entity('Player')
        player.score = player_score[0]
        self.entity_list.append(player)
        self.timeout = TIMEOUT_LEVEL  # 20 Seconds
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.wav')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            # Eventos do pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                if self.timeout == 0:
                    for ent in self.entity_list:
                        if isinstance(ent, Player) and ent.name == 'Player':
                            player_score[0] = ent.score
                    return True

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True

                if not found_player:
                    return False

                # Chamar o método shoot para jogadores e inimigos
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        # Chama o método shoot para Player com event
                        shoot = ent.shoot(event)
                    elif isinstance(ent, Enemy):
                        # Chama o método shoot para Enemy sem event
                        shoot = ent.shoot()
                    else:
                        shoot = None

                    if shoot is not None:
                        self.entity_list.append(shoot)

            # Atualização das entidades
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, Player):
                    ent.update()

            # Atualizações de informações na tela
            self.level_text(18, f'{self.name} - Tempo: {self.timeout / 1000 :.1f}s', C_GREEN, (10, 5))
            self.level_text(18, f'fps: {clock.get_fps() :.0f}', C_DARK_RED, (10, WIN_HEIGHT - 20))

            # Atualização da saúde do jogador
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    self.level_text(18, f'Vida: {ent.health} | Score {ent.score}', C_GREEN, (10, 25))

            pygame.display.flip()

            # Verificações de colisões e saúde
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: pygame.font.Font = pygame.font.SysFont(name="Pacifico", size=text_size)

        # Renderizar o texto em preto para a borda
        text_surf_black: pygame.Surface = text_font.render(text, True, (0, 0, 0)).convert_alpha()
        text_rect_black: pygame.Rect = text_surf_black.get_rect(left=text_pos[0], top=text_pos[1])

        # Renderizar o texto na cor desejada
        text_surf_color: pygame.Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect_color: pygame.Rect = text_surf_color.get_rect(left=text_pos[0], top=text_pos[1])

        # Desenhar o texto preto ligeiramente deslocado para criar a borda
        self.window.blit(text_surf_black, text_rect_black.move(-1, -1))
        self.window.blit(text_surf_black, text_rect_black.move(1, -1))
        self.window.blit(text_surf_black, text_rect_black.move(-1, 1))
        self.window.blit(text_surf_black, text_rect_black.move(1, 1))

        # Desenhar o texto na cor desejada por cima
        self.window.blit(text_surf_color, text_rect_color)
