import random
import pygame
from typing import List
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory
from Code.Const import WIN_WIDTH, COLOR, MENU_OPTION, C_WHITE, WIN_HEIGHT, C_BLACK, C_YELLOW, EVENT_ENEMY, SPAWN_TIME
from Code.EntityMediator import EntityMediator
from Code.Player import Player
from Code.Enemy import Enemy


class Level:
    def __init__(self, window, name, menu_option):
        self.window = window
        self.name = name
        self.menu_option = menu_option
        self.entity_list: List[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Back'))
        self.entity_list.append(EntityFactory.get_entity('Player'))
        self.timeout = 20000  # 20 Seconds
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

    def run(self):
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

            # Atualizações de informações na tela
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps() :.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            # Verificações de colisões e saúde
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: pygame.font.Font = pygame.font.SysFont(name="Pacifico", size=text_size)
        text_surf: pygame.Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: pygame.Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)