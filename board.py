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

from move import Move

class Board:
    """This class represents the board of the game"""
    def __init__(self):
        """Ctor"""
        self.white_board = self._init_white_board()
        self.black_board = self._init_black_board()
            
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
      
    def check(self, pos):
        """Check what is on the board at a given position"""
        val = 1 << pos
        if self.white_board & val == val:
            return 1
        elif self.black_board & val == val:
            return 2
        else:
            return 0
          
    def game_is_finished(self):
        """Returns whether the game is finished or not"""
        return self.white_board == 0 or self.black_board == 0
    
    def print_board(self):
        """Prints the current state board"""
        print "  A B C D E F G H I"
        for i in range(5, 0, -1):
            line = str(i) + " "
            for j in range(0, 9):
                stone = self.check(i * 9 + j - 9)
                if stone == 1:
                    line += "O "
                elif stone == 2:
                    line += "X "
                else:
                    line += ". "
                    
            print line
            
        print ""
                
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