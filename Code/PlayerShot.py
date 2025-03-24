from Code.Entity import Entity
from Code.Const import ENTITY_SPEED


class PlayerShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):  # Indented correctly within the class
        self.rect.centerx += ENTITY_SPEED[self.name]
