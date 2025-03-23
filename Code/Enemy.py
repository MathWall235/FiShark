from Code.Entity import Entity
from Code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED, ENTITY_SHOT_DELAY
from Code.EnemyShot import EnemyShot

class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Initialize shot_delay based on ENTITY_SHOT_DELAY
        self.shot_delay = ENTITY_SHOT_DELAY.get(name, 0)  # Default to 0 if name is not found

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay <= 0:  # When the delay reaches 0 or below, the enemy can shoot
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]  # Reset the delay
            print(f"{self.name} disparou!")  # Apenas para verificar
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        return None