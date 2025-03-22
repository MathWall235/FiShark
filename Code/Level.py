import pygame
from typing import List
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory

class Level:
    def __init__(self, window, name, menu_option):
        self.window = window
        self.name = name
        self.menu_option = menu_option
        self.entity_list: List[Entity] = []  # Correção: declaração com hint de tipo
        self.entity_list.extend(EntityFactory.get_entity('Level1Back'))

    def run(self):
        while True:
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            pygame.display.flip()
        pass