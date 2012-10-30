from board import Board

class FanoronaGame:
    """This class represents the game as is it."""
    def __init__(self, white_ai = None, black_ai = None):
        """Ctor"""
        self._board = Board()
        self._white_ai = white_ai
        self._black_ai = black_ai
        
    def start(self):
        """Starts the game"""
        black = False # white begin the game
        while not self._board.game_is_finished():
            self._board.draw_board()
            move = ""
            prompt = ""
            
            if black and self._black_ai == None:
                prompt = "black> "
            elif not black and self._white_ai == None:
                prompt = "white> "
            
            if prompt != "":
                move = raw_input(prompt)
            else:
                if black:
                    move = self._black_ai.play(self._board.black_board, self._board.white_board, 0)
                else:
                    move = self._white_ai.play(self._board.white_board, self._board.black_board, 0)
                
            self._board.move_piece(move, black)
            black = not black