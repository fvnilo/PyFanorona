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

from board import Board
from gui import GUI

class FanoronaGame:
    """This class represents the game as is it."""
    def __init__(self):
        """Ctor"""
        self.board = Board()
        
    def start(self):
        """Starts the game with GUI"""
        gui = GUI(self.board)
        gui.start_main_loop()
    
    def start_text(self):
        """Starts the game in text mode"""
        black = False # white begin the game
        while not self.board.game_is_finished():
            self.board.print_board()
            
            if black:
                prompt = "black> "
            else:
                prompt = "white> "
            
            move = raw_input(prompt)
            self.board.move_piece(move, black)
            black = not black