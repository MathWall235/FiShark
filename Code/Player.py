import pygame
import pygame.key
from Code.Entity import Entity
from Code.Const import WIN_HEIGHT, ENTITY_SPEED, WIN_WIDTH, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from Code.PlayerShot import PlayerShot

pygame.init()


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        try:
            self.walk_images = [
                pygame.image.load('./asset/walk1.png'),
                pygame.image.load('./asset/walk2.png'),
                pygame.image.load('./asset/walk3.png'),
                pygame.image.load('./asset/walk4.png')
            ]
            self.up_images = [
                pygame.image.load('./asset/up1.png'),
                pygame.image.load('./asset/up2.png'),
                pygame.image.load('./asset/up3.png'),
                pygame.image.load('./asset/up4.png')
            ]
            self.down_images = [
                pygame.image.load('./asset/down1.png'),
                pygame.image.load('./asset/down2.png'),
                pygame.image.load('./asset/down3.png'),
                pygame.image.load('./asset/down4.png')
            ]
            self.attack_images = [
                pygame.image.load('./asset/attack1.png'),
                pygame.image.load('./asset/attack2.png'),
                pygame.image.load('./asset/attack3.png'),
                pygame.image.load('./asset/attack4.png'),
                pygame.image.load('./asset/attack5.png')
            ]
            self.initial_image = pygame.image.load('./asset/Player.png')
            self.hurt_image = pygame.image.load('./asset/hurt.png')
            self.death_images = [
                pygame.image.load(f'./asset/death{i}.png') for i in range(1, 7)
            ]
        except FileNotFoundError as e:
            print(f"Erro ao carregar imagens: {e}")
            self.walk_images = [pygame.Surface((50, 50)) for _ in range(4)]
            self.up_images = [pygame.Surface((50, 50)) for _ in range(4)]
            self.down_images = [pygame.Surface((50, 50)) for _ in range(4)]
            self.attack_images = [pygame.Surface((50, 50)) for _ in range(5)]
            self.initial_image = pygame.Surface((50, 50))
            self.hurt_image = pygame.Surface((50, 50))
            self.death_images = [pygame.Surface((50, 50)) for _ in range(6)]

        self.current_image = 0
        self.surf = self.initial_image
        self.attacking = False
        self.score = 0
        self.shot_delay = ENTITY_SHOT_DELAY.get(name, 0)
        self.death_animation_speed = 5

        # Estados de dano e morte
        self.is_hurt = False
        self.hurt_duration = 15
        self.hurt_timer = 0
        self.is_dead = False
        self.death_animation_index = 0
        self.death_animation_speed = 8
        self.death_animation_counter = 0
        self.death_animation_done = False

    def move(self):
        if self.is_dead:
            return  # Não permite movimento se estiver morto

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
            if not self.is_hurt:
                self.surf = self.initial_image

    def shoot(self, event):
        if self.is_dead:
            return None  # Não permite atirar se estiver morto

        if event.type == pygame.KEYDOWN:
            if event.key == PLAYER_KEY_SHOOT[self.name]:
                if self.shot_delay <= 0:
                    self.attacking = True
                    self.current_image = 0
                    return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        return None

    def on_hit(self):
        if not self.is_dead:
            self.is_hurt = True
            self.hurt_timer = self.hurt_duration

    def update(self):
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.death_animation_index = 0
            self.death_animation_counter = 0

        if self.is_dead:
            self.handle_death_animation()
            return

        # Animação de ataque
        if self.attacking:
            self.current_image = (self.current_image + 1) % len(self.attack_images)
            self.surf = self.attack_images[self.current_image]
            if self.current_image == len(self.attack_images) - 1:
                self.attacking = False
                self.surf = self.initial_image

        # Animação de dano
        if self.is_hurt:
            self.surf = self.hurt_image
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.is_hurt = False
                if not self.attacking:
                    self.surf = self.initial_image

    def handle_death_animation(self):
        if not self.death_animation_done:
            self.death_animation_counter += 1
            if self.death_animation_counter >= self.death_animation_speed:
                self.death_animation_index += 1
                self.death_animation_counter = 0

                if self.death_animation_index >= len(self.death_images):
                    self.death_animation_done = True
                    self.surf = self.death_images[-1]  # Mantém a última imagem
                else:
                    self.surf = self.death_images[self.death_animation_index]


pygame.key.set_repeat(300, 300)