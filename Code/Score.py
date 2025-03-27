import sys
import random
import math
from datetime import datetime
import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE, K_F12
from pygame.font import Font
from Code.Const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE, C_BLACK, WIN_WIDTH, WIN_HEIGHT
from Code.DBProxy import DBProxy


class Score:
    def __init__(self, window):
        self.window = window
        self.screen_width = WIN_WIDTH
        self.screen_height = WIN_HEIGHT

        # Configurações de layout
        self.column_positions = {
            'name': WIN_WIDTH * 0.15,  # 86px
            'score': WIN_WIDTH * 0.45,  # 259px
            'date': WIN_WIDTH * 0.75  # 432px
        }

        self.font_sizes = {
            'title': 26,
            'header': 20,
            'text': 18
        }

        # Configuração visual
        self.colors = {
            'title': (255, 223, 0),
            'top3': (255, 215, 0),
            'normal': C_WHITE,
            'input': (255, 255, 150)
        }

        # Sistema de partículas
        self.particles = []
        self.list_score = []

        # Background
        self.background = pygame.image.load('./asset/Score.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))

    def save_score(self, menu_return: str, player_score: list[int]):
        pygame.mixer.music.load('./asset/Score.wav')
        pygame.mixer.music.play(-1)
        db_proxy = DBProxy('DBScore')
        name = ''
        score = player_score[0]

        while True:
            self.window.blit(self.background, (0, 0))

            # Título animado centralizado
            self._draw_text('PARABÉNS!', self.font_sizes['title'],
                            self.colors['title'], (WIN_WIDTH // 2, 70), outline=True)
            self._draw_text('VOCÊ VENCEU!', self.font_sizes['title'],
                            self.colors['title'], (WIN_WIDTH // 2, 110), outline=True)

            if menu_return == MENU_OPTION[0]:
                # Elementos centralizados
                self._draw_text('DIGITE SEU NOME (4 LETRAS):', self.font_sizes['text'],
                                C_WHITE, (WIN_WIDTH // 2, 150), outline=True)

                # Campo de nome centralizado
                self._draw_text(name, self.font_sizes['text'], self.colors['input'],
                                (WIN_WIDTH // 2, 180), outline=True)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and 3 <= len(name) <= 4:
                        db_proxy.save({'name': name.upper(), 'score': score, 'date': self._get_date()})
                        self.show_score()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4 and event.unicode.isalnum():
                            name += event.unicode

            pygame.display.flip()

    def show_score(self):
        pygame.mixer.music.load('./asset/Score.wav')
        pygame.mixer.music.play(-1)

        db_proxy = DBProxy('DBScore')
        self.list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        self._generate_particles()

        while True:
            # Atualiza elementos
            delta_time = pygame.time.get_ticks() * 0.001
            title_y = 30 + math.sin(delta_time) * 5

            # Redesenha
            self.window.blit(self.background, (0, 0))

            # Título centralizado
            self._draw_text('TOP 10 SCORES', self.font_sizes['title'],
                            self.colors['title'], (WIN_WIDTH // 2, title_y), outline=True)

            # Cabeçalho
            self._draw_header()

            # Scores
            self._draw_scores()

            # Partículas
            self._update_particles()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:  # Verifica primeiro o tipo de evento
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_F12:  # Agora seguro para acessar 'key'
                        self._reset_database()
            pygame.display.flip()

    def _reset_database(self):
        """Reseta o banco de dados e atualiza a tela"""
        db_proxy = DBProxy('DBScore')
        db_proxy.reset()
        db_proxy.close()

        # Atualiza a lista local e partículas
        self.list_score = []
        self.particles = []

        # Recarrega os dados (que agora estarão vazios)
        db_proxy = DBProxy('DBScore')
        self.list_score = db_proxy.retrieve_top10()
        db_proxy.close()

    def _draw_header(self):
        y_pos = 70
        self._draw_text('NOME', self.font_sizes['header'], C_WHITE,
                        (self.column_positions['name'], y_pos), outline=True)
        self._draw_text('SCORE', self.font_sizes['header'], C_WHITE,
                        (self.column_positions['score'], y_pos), outline=True)
        self._draw_text('DATA', self.font_sizes['header'], C_WHITE,
                        (self.column_positions['date'], y_pos), outline=True)

    def _draw_scores(self):
        for idx, (id_, name, score, date) in enumerate(self.list_score):
            y_pos = 100 + idx * 24
            color = self.colors['top3'] if idx < 3 else self.colors['normal']

            self._draw_text(name[:4].ljust(4), self.font_sizes['text'], color,
                            (self.column_positions['name'], y_pos), outline=True)
            self._draw_text(f"{score:06d}", self.font_sizes['text'], color,
                            (self.column_positions['score'], y_pos), outline=True)
            self._draw_text(date[5:16], self.font_sizes['text'], color,
                            (self.column_positions['date'], y_pos), outline=True)

    def _generate_particles(self):
        self.particles = []
        for i in range(3):
            if i < len(self.list_score):
                y_pos = 100 + i * 24
                for _ in range(8):
                    self.particles.append({
                        'pos': [random.uniform(self.column_positions['name'] - 20, self.column_positions['date'] + 20),
                                y_pos],
                        'color': (random.randint(200, 255), random.randint(150, 200), 0),
                        'speed': [random.uniform(-1.5, 1.5), random.uniform(-3.5, -1.5)],
                        'size': random.randint(2, 3),
                        'life': 65
                    })

    def _update_particles(self):
        new_particles = []

        # Adiciona novas partículas periodicamente
        if random.random() < 0.3:
            self._generate_particles()

        for p in self.particles:
            p['pos'][0] += p['speed'][0]
            p['pos'][1] += p['speed'][1]
            p['speed'][1] += 0.12  # Gravidade
            p['life'] -= 1.0

            if p['life'] > 0 and p['pos'][1] < WIN_HEIGHT:
                alpha = int(255 * (p['life'] / 65))
                pygame.draw.circle(self.window, (*p['color'], alpha),
                                   (int(p['pos'][0]), int(p['pos'][1])), int(p['size']))
                new_particles.append(p)

        self.particles = new_particles

    def _draw_text(self, text: str, size: int, color: tuple, center_pos: tuple, outline=False):
        font = Font('./asset/PressStart2P.ttf', size)

        if outline:
            outline_surf = font.render(text, True, (0, 0, 0))
            for offset in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
                outline_rect = outline_surf.get_rect(center=(center_pos[0] + offset[0], center_pos[1] + offset[1]))
                self.window.blit(outline_surf, outline_rect)

        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=center_pos)
        self.window.blit(text_surf, text_rect)

    @staticmethod
    def _get_date():
        return datetime.now().strftime('%Y-%m-%d %H:%M')
