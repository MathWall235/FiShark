import random
import pygame


class ParticleSystem:
    def __init__(self, screen_width: int, screen_height: int, position_range: tuple):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position_range = position_range
        self.particles = []

        # Configurações padrão
        self.color_range = (200, 255, 150, 200)  # min/max R e G
        self.speed_range = (-2.5, 2.5, -4.0, -2.0)  # min/max X e Y
        self.size_range = (2, 3)
        self.life_range = (60, 80)
        self.spawn_chance = 0.25  # 25%

    def generate(self, quantity: int = 5):
        new_particles = []
        for _ in range(quantity):
            new_particles.append({
                'pos': [
                    random.randint(*self.position_range),
                    random.randint(self.screen_height // 4, self.screen_height // 2)
                ],
                'color': (
                    random.randint(self.color_range[0], self.color_range[1]),
                    random.randint(self.color_range[2], self.color_range[3]),
                    0
                ),
                'speed': [
                    random.uniform(self.speed_range[0], self.speed_range[1]),
                    random.uniform(self.speed_range[2], self.speed_range[3])
                ],
                'size': random.randint(*self.size_range),
                'life': random.randint(*self.life_range)
            })
        self.particles.extend(new_particles)

    def update(self):
        new_particles = []

        # Gera novas partículas aleatoriamente
        if random.random() < self.spawn_chance:
            self.generate()

        # Atualiza partículas existentes
        for p in self.particles:
            p['pos'][0] += p['speed'][0]
            p['pos'][1] += p['speed'][1]
            p['speed'][1] += 0.15  # gravidade
            p['life'] -= 1.2

            if p['life'] > 0 and 0 < p['pos'][1] < self.screen_height:
                new_particles.append(p)

        self.particles = new_particles

    def draw(self, surface: pygame.Surface):
        for p in self.particles:
            alpha = int(255 * (p['life'] / self.life_range[1]))
            pygame.draw.circle(
                surface,
                (*p['color'], alpha),
                (int(p['pos'][0]), int(p['pos'][1])),
                int(p['size'])
            )
