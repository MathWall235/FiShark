import pygame
import pygame.key
from Code.Entity import Entity
from Code.Const import WIN_HEIGHT, ENTITY_SPEED, WIN_WIDTH, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY  # ENTITY_SHOT_DELAY
from Code.PlayerShot import PlayerShot

# Inicialize o Pygame
pygame.init()


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        try:
            self.walk_images = [pygame.image.load(f'./asset/walk1.png'),
                                pygame.image.load(f'./asset/walk2.png'),
                                pygame.image.load(f'./asset/walk3.png'),
                                pygame.image.load(f'./asset/walk4.png')]
            self.up_images = [pygame.image.load(f'./asset/up1.png'),
                              pygame.image.load(f'./asset/up2.png'),
                              pygame.image.load(f'./asset/up3.png'),
                              pygame.image.load(f'./asset/up4.png')]
            self.down_images = [pygame.image.load(f'./asset/down1.png'),
                                pygame.image.load(f'./asset/down2.png'),
                                pygame.image.load(f'./asset/down3.png'),
                                pygame.image.load(f'./asset/down4.png')]
            self.attack_images = [pygame.image.load(f'./asset/attack1.png'),
                                  pygame.image.load(f'./asset/attack2.png'),
                                  pygame.image.load(f'./asset/attack3.png'),
                                  pygame.image.load(f'./asset/attack4.png'),
                                  pygame.image.load(f'./asset/attack5.png')]
            self.initial_image = pygame.image.load(f'./asset/Player.png')
        except FileNotFoundError as e:
            print(f"Erro ao carregar imagens: {e}")
            self.walk_images = [pygame.Surface((50, 50)) for _ in range(4)]  # Placeholder images
            self.up_images = [pygame.Surface((50, 50)) for _ in range(4)]  # Placeholder images
            self.down_images = [pygame.Surface((50, 50)) for _ in range(4)]  # Placeholder images
            self.attack_images = [pygame.Surface((50, 50)) for _ in range(5)]  # Placeholder images
            self.initial_image = pygame.Surface((50, 50))  # Placeholder image
        self.current_image = 0
        self.surf = self.initial_image
        self.attacking = False
        self.score = 0  # Inicializa o atributo score
        self.shot_delay = ENTITY_SHOT_DELAY.get(name, 0)  # Inicializa o shot_delay

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_UP] and pressed_key[
            pygame.K_RIGHT] and self.rect.top > 0 and self.rect.right < WIN_WIDTH:
            self.rect.centery -= ENTITY_SPEED[self.name]
            self.rect.centerx += ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.up_images)
            self.surf = self.up_images[self.current_image]
        elif pressed_key[pygame.K_DOWN] and pressed_key[
            pygame.K_RIGHT] and self.rect.bottom < WIN_HEIGHT and self.rect.right < WIN_WIDTH:
            self.rect.centery += ENTITY_SPEED[self.name]
            self.rect.centerx += ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.down_images)
            self.surf = self.down_images[self.current_image]
        elif pressed_key[pygame.K_UP] and pressed_key[pygame.K_LEFT] and self.rect.top > 0 and self.rect.left > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
            self.rect.centerx -= ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.up_images)
            self.surf = self.up_images[self.current_image]
        elif pressed_key[pygame.K_DOWN] and pressed_key[
            pygame.K_LEFT] and self.rect.bottom < WIN_HEIGHT and self.rect.left > 0:
            self.rect.centery += ENTITY_SPEED[self.name]
            self.rect.centerx -= ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.down_images)
            self.surf = self.down_images[self.current_image]
        elif pressed_key[pygame.K_UP] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.up_images)
            self.surf = self.up_images[self.current_image]
        elif pressed_key[pygame.K_DOWN] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.down_images)
            self.surf = self.down_images[self.current_image]
        elif pressed_key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.walk_images)
            self.surf = self.walk_images[self.current_image]
        elif pressed_key[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]
            self.current_image = (self.current_image + 1) % len(self.walk_images)
            self.surf = self.walk_images[self.current_image]
        else:
            self.surf = self.initial_image

    def shoot(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == PLAYER_KEY_SHOOT[self.name]:
                if self.shot_delay <= 0:
                    self.attacking = True
                    self.current_image = 0
                    # self.shot_delay = ENTITY_SHOT_DELAY[self.name]  # Reset the delay
                    return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        #      else:
        #  self.shot_delay -= 1

    def update(self):
        if self.attacking:
            self.current_image = (self.current_image + 1) % len(self.attack_images)
            self.surf = self.attack_images[self.current_image]
            if self.current_image == len(self.attack_images) - 1:
                self.attacking = False
                self.surf = self.initial_image


# Configuração da repetição de teclas
pygame.key.set_repeat(300, 300)
