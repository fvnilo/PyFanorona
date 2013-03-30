# Copyright (c) 2013, Ny Fanilo Andrianjafy
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies, 
# either expressed or implied, of the FreeBSD Project.

class Move:
    """This class contains the class methods that validates and apply the move on a board"""
    
    # From the white pieces perspective
    UP = 9
    DOWN = -9
    LEFT = -1
    RIGHT = 1
    
    # Legal move dictionary
    LEGAL_MOVES = { "UL" : UP + LEFT, "U" : UP, "UR" : UP + RIGHT, "DL" : DOWN + LEFT, "D" : DOWN, "DR" : DOWN + RIGHT, "R" : RIGHT, "L" : LEFT }
    
    # Constants
    BOARD_LOW_LIMIT = 0
    BOARD_UP_LIMIT = 44

    @classmethod
    def is_legal_move(cls, start, end, attack, defense):
        """Checks whether a move is legal or not"""
        
        if end < cls.BOARD_LOW_LIMIT or end > cls.BOARD_UP_LIMIT:
            return False;
        
        move = end - start # The length of the move
        correct_move = True
        
        legal_move = move in cls.LEGAL_MOVES.values() # Verify that the move is legal.
        piece_placed = attack & 1 << start == (1 << start) # Player did select a piece from his side.
        
        # Mathematically speaking, from a zero-index position, only even pieces can move diagonally    
        if move not in [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]:
            correct_move = start % 2 == 0
        
        # There is no piece on the spot the player wants to go to.
        end_free = attack & 1 << end == 0 and defense & 1 << end == 0
        
        return legal_move and piece_placed and end_free and correct_move
    
    @classmethod
    def apply_attack_move(cls, start, end, board):
        """Applies the offensive move"""
        
        # Toggling bits
        board ^= 1 << start
        board ^= 1 << end
            
        return board
        
    @classmethod
    def apply_defense_move(cls, start, end, board):
        """Applies the defensive move"""
        mult = 2 # First round, multiply by two in the direction
        move = end - start
        withdrawal = False
        shift = cls._calc_shift(start, move, mult)
            
        # Is it a withdrawal move ? 
        if not board & 1 << shift == (1 << shift):
            withdrawal = True
            move = -move
            shift = cls._calc_shift(end, move, mult)
        
        # As long as there is a piece in the line of attack and that we can virtually continue.
        while board & 1 << shift == (1 << shift) and cls.must_continue(start, shift, move):
            board ^= 1 << shift # Toggle bit
            mult += 1 # Next round, check one step further.
            if withdrawal:
                shift = cls._calc_shift(end, move, mult)
            else:
                shift = cls._calc_shift(start, move, mult)
        
        return board
    
    @classmethod
    def must_continue(cls, start, shift, move):
        """Check whether captures can continue or not from a bitmap point of view"""
        if move == cls.UP or move == cls.DOWN:
            return True

        if move == cls.LEFT or move == cls.RIGHT:
            return start // 9 == shift // 9 # Check that we are still in the same row
        
        # When moving diagonally (UR or DL), you could be toggling the bit on index 0
        # otherwise the move might have come back to the bit 0 and should not toggle it.
        return (shift == 0 and start % 10 == 0) or shift != 0
        
    
    @classmethod
    def _calc_shift(cls, start, move, mult):
        """Calculates the shift for applying the defensive move"""
        shift = start + (move * mult)

        # Reverse the shift
        if shift < 0: 
            shift = cls.BOARD_UP_LIMIT - shift
            
        return shift