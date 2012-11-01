# This program is a simple Python implementation of a traditional Malagasy
# strategy board game.
# Copyright (C) 2012  Nylo Gavins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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