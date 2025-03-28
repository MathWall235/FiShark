import pygame
from Code.Entity import Entity
from Code.Const import WIN_HEIGHT, ENTITY_SPEED, WIN_WIDTH, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from Code.PlayerShot import PlayerShot


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        try:
            # Carregamento de imagens
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
            self._create_fallback_surfaces()

        # Configurações iniciais
        self.current_image = 0
        self.surf = self.initial_image
        self.attacking = False
        self.score = 0
        self.shot_delay = ENTITY_SHOT_DELAY.get(name, 0)

        # Controles de animação
        self.attack_animation_speed = 2
        self.attack_animation_counter = 0
        self.walk_animation_speed = 8
        self.death_animation_speed = 15

        # Estados de dano/morte
        self.is_hurt = False
        self.hurt_duration = 10
        self.hurt_timer = 0
        self.is_dead = False
        self.death_animation_index = 0
        self.death_animation_counter = 0
        self.death_animation_done = False

    def _create_fallback_surfaces(self):
        """Cria surfaces básicas como fallback"""
        default_size = (50, 50)
        self.walk_images = [pygame.Surface(default_size) for _ in range(4)]
        self.up_images = [pygame.Surface(default_size) for _ in range(4)]
        self.down_images = [pygame.Surface(default_size) for _ in range(4)]
        self.attack_images = [pygame.Surface(default_size) for _ in range(5)]
        self.initial_image = pygame.Surface(default_size)
        self.hurt_image = pygame.Surface(default_size)
        self.death_images = [pygame.Surface(default_size) for _ in range(6)]

    def move(self):
        if self.is_dead:
            return

        dx, dy = 0, 0
        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_UP] and self.rect.top > 0:
            dy -= ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_DOWN] and self.rect.bottom < WIN_HEIGHT:
            dy += ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_LEFT] and self.rect.left > 0:
            dx -= ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            dx += ENTITY_SPEED[self.name]

        if dx != 0 or dy != 0:
            self.rect.move_ip(dx, dy)
            self._update_movement_animation(dx, dy)
        else:
            if not self.is_hurt and not self.attacking:
                self.surf = self.initial_image

    def _update_movement_animation(self, dx, dy):
        if dy < 0:
            self._animate(self.up_images, self.walk_animation_speed)
        elif dy > 0:
            self._animate(self.down_images, self.walk_animation_speed)
        else:
            self._animate(self.walk_images, self.walk_animation_speed)

    def _animate(self, image_list, speed):
        if pygame.time.get_ticks() % speed == 0:
            self.current_image = (self.current_image + 1) % len(image_list)
            self.surf = image_list[self.current_image]

    def shoot(self, event):
        if self.is_dead:
            return None

        if event.type == pygame.KEYDOWN and event.key == PLAYER_KEY_SHOOT[self.name]:
            if self.shot_delay <= 0:
                self._start_attack_animation()
                return PlayerShot(
                    name=f'{self.name}Shot',
                    position=(self.rect.centerx, self.rect.centery)
                )
        return None

    def _start_attack_animation(self):
        self.attacking = True
        self.current_image = 0
        self.attack_animation_counter = 0
        self.surf = self.attack_images[0]

    def update(self):
        if self.health <= 0 and not self.is_dead:
            self._start_death_animation()

        if self.is_dead:
            self.handle_death_animation()
            return

        if self.attacking:
            self._update_attack_animation()

        if self.is_hurt:
            self._update_hurt_animation()

    def _update_attack_animation(self):
        self.attack_animation_counter += 1
        if self.attack_animation_counter >= self.attack_animation_speed:
            self.current_image += 1
            self.attack_animation_counter = 0

            if self.current_image >= len(self.attack_images):
                self.attacking = False
                self.surf = self.initial_image
            else:
                self.surf = self.attack_images[self.current_image]

    def _update_hurt_animation(self):
        self.hurt_timer -= 1
        self.surf = self.hurt_image if self.hurt_timer % 4 < 2 else self.initial_image
        if self.hurt_timer <= 0:
            self.is_hurt = False
            self.surf = self.initial_image

    def _start_death_animation(self):
        self.is_dead = True
        self.death_animation_index = 0
        self.death_animation_counter = 0
        self.surf = self.death_images[0]

    def handle_death_animation(self):
        if not self.death_animation_done:
            self.death_animation_counter += 1
            if self.death_animation_counter >= self.death_animation_speed:
                self.death_animation_index += 1
                self.death_animation_counter = 0

                if self.death_animation_index >= len(self.death_images):
                    self.death_animation_done = True
                    self.surf = self.death_images[-1]
                    self.trigger_game_over()
                else:
                    self.surf = self.death_images[self.death_animation_index]

    def trigger_game_over(self):
        from Code.GameState import GameState
        GameState.game_over = True

    def on_hit(self):
        if not self.is_dead:
            self.is_hurt = True
            self.hurt_timer = self.hurt_duration