import random
import pygame
import sys
from typing import List
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory
import Code.Const as Const
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
        self.player = player  # Referência direta ao jogador
        player.score = player_score[0]
        self.entity_list.append(player)
        self.timeout = Const.LEVEL_DURATION
        pygame.time.set_timer(Const.EVENT_ENEMY, Const.SPAWN_TIME)
        pygame.time.set_timer(Const.EVENT_TIMEOUT, Const.TIMEOUT_STEP)
        self.fonts = {}  # Cache de fontes

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            players = [ent for ent in self.entity_list if isinstance(ent, Player)]
            enemies = [ent for ent in self.entity_list if isinstance(ent, Enemy)]

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == Const.EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == Const.EVENT_TIMEOUT:
                    self.timeout -= Const.TIMEOUT_STEP
                if self.timeout <= 0:
                    player_score[0] = self.player.score
                    return True

                # Processar tiros
                for ent in players:
                    shoot = ent.shoot(event)
                    if shoot is not None:
                        self.entity_list.append(shoot)
                for ent in enemies:
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            # Verificar se o jogador ainda está vivo
            if not any(isinstance(ent, Player) for ent in self.entity_list):
                return False

            # Atualizar entidades
            for ent in self.entity_list:
                ent.move()
                if isinstance(ent, Player):
                    ent.update()

            # Verificar colisões e saúde
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

            # Renderização
            self.window.fill(Const.C_BLACK)  # Limpar tela
            for ent in self.entity_list:
                self.window.blit(ent.surf, ent.rect)

            # Exibir informações
            self.level_text(20, f'{self.name} - Tempo: {self.timeout / 1000 :.1f}s', Const.C_GREEN, (10, 5))
            self.level_text(20, f'fps: {clock.get_fps() :.0f}', Const.C_DARK_RED, (10, Const.WIN_HEIGHT - 20))
            if players:
                self.level_text(18, f'Vida: {players[0].health} | Score {players[0].score}', Const.C_GREEN, (10, 25))

            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        # Cache de fontes
        if text_size not in self.fonts:
            self.fonts[text_size] = pygame.font.SysFont("Pacifico", text_size)
        text_font = self.fonts[text_size]

        text_surf_black = text_font.render(text, True, (0, 0, 0)).convert_alpha()
        text_rect = text_surf_black.get_rect(topleft=text_pos)

        # Bordas pretas
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for offset in offsets:
            self.window.blit(text_surf_black, text_rect.move(offset))

        # Texto colorido
        text_surf_color = text_font.render(text, True, text_color).convert_alpha()
        self.window.blit(text_surf_color, text_rect)