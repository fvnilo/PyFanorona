from game import FanoronaGame
from ai import AI, AIDifficulty

g = FanoronaGame(AI(AIDifficulty.EASY), AI(AIDifficulty.EASY))
g.start()