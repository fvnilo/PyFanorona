from move import Move
import math

class AIDifficulty:
    EASY = 1
    MEDIUM = 3
    HARD = 5
    
class AI:
    def __init__(self, difficulty):
        self._difficulty = difficulty
    
    def play(self, board, opponent, depth):
        for i in range(0, 45):
            if board & (1 << i) == (1 << i):
                for k, v in Move.legal_moves.iteritems():
                    if Move.is_legal_move(i, i+v, board, opponent):
                         move = str(chr(65 + (i % 9)))
                         move += str((i / 9) + 1)
                         move += str(chr(65 + ((i+v) % 9)))
                         move += str(((i+v) / 9) + 1)
                         
                         print move
                         return move