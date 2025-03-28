# menu.py
import pygame
import math
from pygame import Surface, Rect
from pygame.font import Font
from Code.Const import WIN_WIDTH, COLOR, MENU_OPTION, C_WHITE, WIN_HEIGHT, C_BLACK, C_YELLOW

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer.music.load('./asset/MenuSom.mp3')
        pygame.mixer.music.play(-1)
        while True:
            # Desenha o background
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(
                text_size=70,
                text="FiShark",
                text_color=COLOR,
                text_center_pos=(WIN_WIDTH / 2, 100)
            )
            # Ajuste: posição inicial e espaçamento reduzidos para caber todas as opções
            start_y = 160
            spacing = 40
            # Desenha as opções do menu
            for i, option in enumerate(MENU_OPTION):
                y = start_y + spacing * i
                if i == menu_option:
                    self.menu_text(
                        text_size=20,
                        text=option,
                        text_color=C_YELLOW,
                        text_center_pos=(WIN_WIDTH / 2, y)
                    )
                else:
                    self.menu_text(
                        text_size=20,
                        text=option,
                        text_color=C_WHITE,
                        text_center_pos=(WIN_WIDTH / 2, y)
                    )
            # Incluir o texto "Feito por: ..." na borda inferior da tela
            self.menu_text(
                text_size=9,
                text="Feito por: Matheus Wallace Pedroso de Almeida / RU: 4525258",
                text_color=C_WHITE,
                text_center_pos=(WIN_WIDTH / 2, WIN_HEIGHT - 10)
            )
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    if event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.Font('./asset/PressStart2P.ttf', text_size)
        time_val = pygame.time.get_ticks() / 300
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        float_offset = int(math.sin(time_val) * 5)
        text_rect: Rect = text_surf.get_rect(center=(text_center_pos[0], text_center_pos[1] + float_offset))
        outline_color = (0, 0, 0)
        outline_surf = text_font.render(text, True, outline_color).convert_alpha()
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for offset in offsets:
            offset_rect = text_rect.copy()
            offset_rect.move_ip(offset)
            self.window.blit(outline_surf, offset_rect)
        self.window.blit(text_surf, text_rect)
