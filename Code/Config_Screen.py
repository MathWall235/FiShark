import sys, math, random, pygame
from pygame import KEYDOWN, K_RETURN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.font import Font
from Code.Const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_YELLOW, C_BLACK, PLAYER_HEALTH, ENEMY_ATTACK_SPEED, LEVEL_DURATION

class ConfigScreen:
    def __init__(self, window):
        self.window = window
        # Utiliza o mesmo background da tela de Score (você pode trocar o asset se preferir)
        self.background = pygame.image.load('./asset/Score.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        self.font_path = './asset/PressStart2P.ttf'
        # Configurações iniciais (valores atuais)
        self.fields = [
            {
                "name": "Saúde do Player",
                "value": PLAYER_HEALTH,
                "min": 100,
                "max": 1000,
                "step": 10,
            },
            {
                "name": "Vel. de Ataque do Inimigo",
                "value": (5 + 50) - ENEMY_ATTACK_SPEED,
                "min": 5,
                "max": 50,
                "step": 1,
            },
            {
                "name": "Duração do Nível (s)",
                "value": LEVEL_DURATION // 1000,  # converte ms para segundos
                "min": 10,
                "max": 60,
                "step": 1,
            },
        ]
        self.selected_field = 0
        self.font_sizes = {
            "title": 26,
            "field": 18,
            "instruction": 9
        }
        self.colors = {
            "title": C_YELLOW,
            "field": C_WHITE,
            "selected": C_YELLOW,
            "instruction": C_WHITE
        }

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.window.blit(self.background, (0, 0))
            # Título centralizado
            self._draw_text("CONFIGURAÇÕES", self.font_sizes["title"], self.colors["title"], (WIN_WIDTH // 2, 40),
                            outline=True)

            # Desenha os campos de configuração
            start_y = 100
            spacing = 50
            for idx, field in enumerate(self.fields):
                pos_y = start_y + idx * spacing
                color = self.colors["selected"] if idx == self.selected_field else self.colors["field"]
                text = f"{field['name']}: {field['value']}"
                self._draw_text(text, self.font_sizes["field"], color, (WIN_WIDTH // 2, pos_y), outline=True)

            # Instruções
            instruction_text = "↑/↓: Navegar   ←/→: Alterar   ENTER: Confirmar   ESC: Voltar"
            self._draw_text(instruction_text, self.font_sizes["instruction"], self.colors["instruction"],
                            (WIN_WIDTH // 2, WIN_HEIGHT - 30), outline=True)

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected_field = (self.selected_field - 1) % len(self.fields)
                    elif event.key == K_DOWN:
                        self.selected_field = (self.selected_field + 1) % len(self.fields)
                    elif event.key == K_LEFT:
                        field = self.fields[self.selected_field]
                        field["value"] = max(field["min"], field["value"] - field["step"])
                    elif event.key == K_RIGHT:
                        field = self.fields[self.selected_field]
                        field["value"] = min(field["max"], field["value"] + field["step"])
                    elif event.key == K_RETURN:
                        # Retorna os valores atualizados (convertendo a duração para ms)
                        return (
                            self.fields[0]["value"],
                            (self.fields[1]['min'] + self.fields[1]['max'] - self.fields[1]["value"]),
                            # Converte para delay
                            self.fields[2]["value"] * 1000
                        )
                    elif event.key == K_ESCAPE:
                        # Sai sem alterar (retorna os valores originais)
                        return (PLAYER_HEALTH, ENEMY_ATTACK_SPEED, LEVEL_DURATION)

    def _draw_text(self, text, size, color, center_pos, outline=False):
        font = Font(self.font_path, size)
        if outline:
            outline_surf = font.render(text, True, C_BLACK)
            for offset in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
                outline_rect = outline_surf.get_rect(center=(center_pos[0] + offset[0], center_pos[1] + offset[1]))
                self.window.blit(outline_surf, outline_rect)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=center_pos)
        self.window.blit(text_surf, text_rect)
