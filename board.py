from move import Move

class Board:
    """This class represents the board of the game"""
    def __init__(self):
        """Ctor"""
        self.white_board = self._init_white_board()
        self.black_board = self._init_black_board()
    
    def draw_board(self):
        """Prints the current state board"""
        print "  A B C D E F G H I"
        for i in range(5, 0, -1):
            line = str(i) + " "
            for j in range(0, 9):
                val = 1 << (i * 9 + j - 9)
                if self.white_board & val == val:
                    line += "O "
                elif self.black_board & val == val:
                    line += "X "
                else:
                    line += ". "
                    
            print line
            
        print ""
            
    def move_piece(self, play, black):
        """Moves piece that was selected"""
        A = 65 #The letter A in ASCII
        x1 = ord(play[0].strip().upper()) - A
        y1 = int(play[1]) - 1
        x2 = ord(play[2].strip().upper()) - A
        y2 = int(play[3]) - 1
        
        start = x1 + (y1 * 9)
        end = x2 + (y2 * 9)
        
       
        
        if black:
            if not Move.is_legal_move(start, end, self.black_board, self.white_board):
                raise ValueError("Invalid move")
            
            self.black_board = Move.apply_attack_move(start, end, self.black_board)
            self.white_board = Move.apply_defense_move(start, end, self.white_board)
        else:
            if not Move.is_legal_move(start, end, self.white_board, self.black_board):
                raise ValueError("Invalid move")
            
            self.white_board = Move.apply_attack_move(start, end, self.white_board)
            self.black_board = Move.apply_defense_move(start, end, self.black_board)
            
    def game_is_finished(self):
        """Returns whether the game is finished or not"""
        return self.white_board == 0 or self.black_board == 0 
                
    def _init_white_board(self):
        """Initializes the white board"""
        white_board = 0L
        for i in range(26, -1, -1):
            white_board = white_board << 1 
        
            if not i in [18, 20, 22, 23, 25]:
                white_board |= 1
            
        return white_board
    
    def _init_black_board(self):
        """Initializes the black board"""
        black_board = 1L << 44
        
        for i in range(18, 44):
            if not i in [19, 21, 22, 24, 26]:
                black_board |= 1 << i
                
        return black_board