class GameState:
    game_over = False
    current_level = 'Level1'
    player_score = [0]

    @classmethod
    def reset(cls):
        cls.game_over = False
        cls.current_level = 'Level1'
        cls.player_score = [0]