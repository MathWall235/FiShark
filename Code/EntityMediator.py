from Code.Entity import Entity
from Code.Enemy import Enemy
from Code.PlayerShot import PlayerShot
from Code.Const import WIN_WIDTH
from Code.EnemyShot import EnemyShot
from Code.Player import Player
from Code.GameState import GameState


class EntityMediator:
    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right < 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):

                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

                # Nova parte para triggerar a animação de dano
                if isinstance(ent1, Player):
                    ent1.on_hit()
                if isinstance(ent2, Player):
                    ent2.on_hit()

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'PlayerShot':
            for ent in entity_list:
                if isinstance(ent, Player):
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        to_remove = []
        game_over_triggered = False

        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Player):
                    if ent.death_animation_done:
                        to_remove.append(ent)
                        game_over_triggered = True
                else:
                    if isinstance(ent, Enemy):
                        EntityMediator.__give_score(ent, entity_list)
                    to_remove.append(ent)

        for ent in to_remove:
            if ent in entity_list:
                entity_list.remove(ent)

        if game_over_triggered:
            GameState.game_over = True
