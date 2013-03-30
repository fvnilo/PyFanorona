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
                return False
            
            self.black_board = Move.apply_attack_move(start, end, self.black_board)
            self.white_board = Move.apply_defense_move(start, end, self.white_board)
        else:
            if not Move.is_legal_move(start, end, self.white_board, self.black_board):
                return False
            
            self.white_board = Move.apply_attack_move(start, end, self.white_board)
            self.black_board = Move.apply_defense_move(start, end, self.black_board)
        
        return True
              
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
        for i in range(5):
            line = str(5-i) + " "
            for j in range(9):
                stone = self.check((4-i) * 9 + j)
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