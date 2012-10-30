class Move:
    """This class contains the class methods that validates and apply the move on a board"""
    
    # From the white pieces perspective
    UP = 9
    DOWN = -9
    LEFT = -1
    RIGHT = 1
    
    # Legal move dictionary
    legal_moves = { "UL" : UP + LEFT, "U" : UP, "UR" : UP + RIGHT, "DL" : DOWN + LEFT, "D" : DOWN, "DR" : DOWN + RIGHT, "R" : RIGHT, "L" : LEFT }
    
    @classmethod
    def is_legal_move(cls, start, end, attack, defense):
        """Checks whether a move is legal or not"""
        
        if end < 0 or end >= 45:
            return False;
        
        move = end - start
        legal_move = False
        piece_placed = False
        end_free = False
        correct_move = True
        
        legal_move = move in cls.legal_moves.values()
        piece_placed = attack & 1 << start == (1 << start)
        
        # Mathematically speaking, from a zero-index position, only even pieces can move diagonally    
        if move not in [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]:
            correct_move = start % 2 == 0
            
        end_free = attack & 1 << end == 0 and defense & 1 << end == 0
        
        return legal_move and piece_placed and end_free and correct_move
    
    @classmethod
    def apply_attack_move(cls, start, end, board):
        """Applies the offensive move"""
        
        board ^= 1 << start
        board ^= 1 << end
            
        return board
        
    @classmethod
    def apply_defense_move(cls, start, end, board):
        """Applies the defensive move"""
        mult = 2
        move = end - start
        withdrawal = False
        shift = cls._calc_shift(start, move, mult)
            
        if not board & 1 << shift == (1 << shift): # withdrawal move
            withdrawal = True
            move = -move
            shift = cls._calc_shift(end, move, mult)
        
    
        while board & 1 << shift == (1 << shift):
            board ^= 1 << shift
            mult +=1
            if withdrawal:
                shift = cls._calc_shift(end, move, mult)
            else:
                shift = cls._calc_shift(start, move, mult)
        
        return board
    
    @classmethod
    def _calc_shift(cls, start, move, mult):
        """Calculates the shift for applying the defensive move"""
        shift = start + (move * mult)
        if shift < 0: 
            shift = 44 - shift
            
        return shift