import pygame


class DeathAnimation:
    def __init__(self):
        self.frames = [
            pygame.image.load(f'./asset/death{i}.png').convert_alpha()
            for i in range(1, 6)
        ]
        self.current_frame = 0
        self.position = (0, 0)
        self.active = False
        self.start_time = 0
        self.frame_duration = 200  # ms por frame
        self.show_message = False

    def start(self, position):
        self.position = position
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.show_message = False

    def update(self):
        if self.active:
            elapsed = pygame.time.get_ticks() - self.start_time
            self.current_frame = elapsed // self.frame_duration

            if self.current_frame >= len(self.frames):
                self.active = False
                self.show_message = True

    def draw(self, screen):
        if self.active:
            current_image = self.frames[self.current_frame]
            screen.blit(current_image, self.position)