import pygame.key
from Code.Entity import Entity
from Code.Const import WIN_HEIGHT, ENTITY_SPEED, WIN_WIDTH, PLAYER_KEY_SHOOT #ENTITY_SHOT_DELAY
from Code.PlayerShot import PlayerShot


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        #self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self, ):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_UP] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_DOWN] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]
        pass

    def shoot(self, event):
      #  self.shot_delay -= 1
       # if self.shot_delay == 0:
        #    self.shot_delay = ENTITY_SHOT_DELAY[self.name]
          if event.type == pygame.KEYDOWN:
              if event.key == PLAYER_KEY_SHOOT[self.name]:
                  return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
