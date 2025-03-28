import pygame
import math
from pygame import Surface, Rect
from pygame.font import Font
from Code.Const import WIN_WIDTH, C_WHITE, WIN_HEIGHT, C_BLACK, C_YELLOW, C_DARK_RED, C_RED


class GameOver:
    def __init__(self, window):
        self.window = window
        self.options = ['Reiniciar', 'Voltar ao Menu']
        self.selected_option = 0
        self.surf = pygame.image.load('./asset/GameOver.png').convert_alpha()
        self.rect = self.surf.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

    def run(self):
        pygame.mixer.music.load('./asset/GameOver.mp3')
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()

        while True:
            # Fundo personalizado
            self.window.fill(C_BLACK)
            self.window.blit(self.surf, self.rect)

            # Efeito de pulsação
            time = pygame.time.get_ticks() / 300
            self.draw_text_with_effect("VOCÊ PERDEU", 50, C_RED, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 50), time)

            # Opções do menu
            for i, option in enumerate(self.options):
                color = C_YELLOW if i == self.selected_option else C_WHITE
                self.draw_text_with_outline(
                    text=option,
                    size=25,
                    color=color,
                    position=(WIN_WIDTH / 2, WIN_HEIGHT / 2 + 50 + i * 60),
                    shadow_color=C_BLACK
                )

            pygame.display.flip()
            clock.tick(60)

            # Controles
            selected = self.handle_input()
            if selected is not None:
                pygame.mixer.music.stop()
                return selected

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % 2
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % 2
                elif event.key == pygame.K_RETURN:
                    return self.selected_option
        return None

    def draw_text_with_effect(self, text, size, color, center_pos, time):
        try:
            text_font = Font('./asset/PressStart2P.ttf', size)
        except:
            text_font = Font(None, size)

        float_offset = int(math.sin(time) * 8)

        # Texto principal
        text_surf = text_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(center_pos[0], center_pos[1] + float_offset))

        # Sombra
        shadow_surf = text_font.render(text, True, (30, 30, 30))
        self.window.blit(shadow_surf, text_rect.move(3, 3))

        self.window.blit(text_surf, text_rect)

    def draw_text_with_outline(self, text, size, color, position, shadow_color):
        try:
            text_font = Font('./asset/PressStart2P.ttf', size)
        except:
            text_font = Font(None, size)

        # Renderizações para contorno
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1),
                   (1, -1), (1, 0), (1, 1)]

        for offset in offsets:
            text_surf = text_font.render(text, True, shadow_color)
            text_rect = text_surf.get_rect(center=(position[0] + offset[0], position[1] + offset[1]))
            self.window.blit(text_surf, text_rect)

        # Texto principal
        text_surf = text_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=position)
        self.window.blit(text_surf, text_rect)
