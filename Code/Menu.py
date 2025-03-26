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
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(
                text_size=150,
                text="FiShark",
                text_color=COLOR,
                text_center_pos=(WIN_WIDTH / 2, 100)
            )
            for i, option in enumerate(MENU_OPTION):
                if i == menu_option:
                    self.menu_text(
                        text_size=30,  # Tamanho do texto ajustado
                        text=option,
                        text_color=C_YELLOW,
                        text_center_pos=(WIN_WIDTH / 2, 180 + 50 * i))
                else:
                    self.menu_text(
                        text_size=30,  # Tamanho do texto ajustado
                        text=option,
                        text_color=C_WHITE,
                        text_center_pos=(WIN_WIDTH / 2, 180 + 50 * i)
                    )
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:  # Down
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:  # Up
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Pacifico", size=text_size)
        time = pygame.time.get_ticks() / 300  # Controla a velocidade da flutuação

        # Cria superfície principal
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()

        # Efeito de flutuação vertical
        float_offset = int(math.sin(time) * 5)  # Amplitude de 5 pixels
        text_rect: Rect = text_surf.get_rect(center=(text_center_pos[0], text_center_pos[1] + float_offset))

        # Contorno estático
        outline_color = (0, 0, 0)
        outline_surf = text_font.render(text, True, outline_color).convert_alpha()

        # Desenha contorno
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for offset in offsets:
            offset_rect = text_rect.copy()
            offset_rect.move_ip(offset)
            self.window.blit(outline_surf, offset_rect)

        # Desenha texto flutuante
        self.window.blit(text_surf, text_rect)
