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

import pygame
import sys
from helpers import load_image
from pygame.locals import MOUSEBUTTONUP

class GUI:
    """This class represents the GUI of the game."""
    def __init__(self, board, width=800,height=431):
        """Ctor"""
        self.board = board
        self.width = width
        self.height = height
        self.background = pygame.image.load("data/images/board.png")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.space_dist = 45 
        self.stone_size = 47
        self.xOff = 5
        self.yOff = 5
        
        self.current_stone = None
            
    def start_main_loop(self):
        """Starts the main loop of the game which consists of capturing events
        and drawing sprites."""
        backgroundRect = self.background.get_rect()
        self.load_sprites()
        self.current_player = 1
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    self.handle_click()

            self.screen.blit(self.background, backgroundRect)
            self.one_stones.draw(self.screen)
            self.two_stones.draw(self.screen)
            self.empties.draw(self.screen)
            pygame.display.flip()
            
    def load_sprites(self):
        """Initializes the stones' sprites."""
        self.one_stones = pygame.sprite.Group()
        self.two_stones = pygame.sprite.Group()
        self.empties = pygame.sprite.Group()
        
        for y in range(5):
            for x in range(9):
                xPos = self.xOff + x*self.stone_size + x*self.space_dist
                yPos = self.yOff + y*self.stone_size + y*self.space_dist
                
                pos = (4-y) * 9 + x;
                stone = self.board.check(pos)
                
                if stone == 0:
                    self.empties.add(Stone(stone, x, 5-y, pygame.Rect(xPos, yPos, self.stone_size, self.stone_size)))
                    
                if stone == 1:
                    self.one_stones.add(Stone(stone, x, 5-y, pygame.Rect(xPos, yPos, self.stone_size, self.stone_size)))
                    
                if stone == 2:
                    self.two_stones.add(Stone(stone, x, 5-y, pygame.Rect(xPos, yPos, self.stone_size, self.stone_size)))
                    
    def handle_click(self):
        """Handles the click event on the board"""
        pos = pygame.mouse.get_pos()
        
        if not self.current_stone:
            self.pick_stone(pos)
        else:
            self.handle_movement(pos)
    
    def pick_stone(self, pos):
        """Picks up a stone when we click on it."""
        if self.current_player == 1:
            collisions = [s for s in self.one_stones if s.rect.collidepoint(pos)]
        else:
            collisions = [s for s in self.two_stones if s.rect.collidepoint(pos)]
        
        if len(collisions) > 0:
            self.current_stone = collisions[0]
            
    def handle_movement(self, pos):
        """Inits the movement of a stone"""
        collisions = [s for s in self.empties if s.rect.collidepoint(pos)]
    
        if len(collisions):
            empty = collisions[0]
            x, y = empty.getPos()
            empty.kill()
            start = self.current_stone.get_coordinates()
            end = empty.get_coordinates()
            print start, end
            if self.board.move_piece(start+end, self.current_player == 2):
                self.current_stone.move(x, y, empty.coord_x, empty.coord_y)
                self.update()
                
                if self.current_player == 1:
                    self.current_player = 2
                else:
                    self.current_player = 1
            
        self.current_stone = None
        
    def update(self):
        """Updates the sprites' state after a move"""
        for y in range(5):
            for x in range(9):
                xPos = self.xOff + x*self.stone_size + x*self.space_dist
                yPos = self.yOff + y*self.stone_size + y*self.space_dist
                
                pos = (4-y) * 9 + x;
                board_stone = self.board.check(pos)
                
                if board_stone == 0:
                    if self.current_player == 1:
                        stones = [s for s in self.two_stones if s.rect.collidepoint((xPos+1, yPos+1))]
                    else:
                        stones = [s for s in self.one_stones if s.rect.collidepoint((xPos+1, yPos+1))]
                    if not stones or (len(stones) == 1 and stones[0].player != 0):
                        self.empties.add(Stone(0, x, 5-y, pygame.Rect(xPos, yPos, self.stone_size, self.stone_size)))
                        
                    if len(stones) == 1 and stones[0].player != 0:
                        stones[0].kill()
                    

                 
class Stone(pygame.sprite.Sprite):
    """A game stone."""
    def __init__(self, player, coord_x, coord_y, rect=None):
        """Ctor"""
        pygame.sprite.Sprite.__init__(self)
        
        self.player = player
        self.coord_x = coord_x
        self.coord_y = coord_y
        
        if player == 1:
            img = 'one.png'
        elif player == 2:
            img = 'two.png'
        else:
            img = 'empty.png'
        
        self.image, self.rect = load_image(img, -1)
        
        if rect != None:
            self.rect = rect
            
    def getPos(self):
        """Gets the visual position of the stone"""
        return (self.rect.left, self.rect.top)
    
    def get_coordinates(self):
        """Gets the board coordinate of the stone"""
        return str(chr(65 + self.coord_x)) + str(self.coord_y)
    
    def move(self, x, y, coord_x, coord_y):
        """Move the stone to a new place"""
        xMove, yMove = x - self.rect.left, y - self.rect.top
        self.rect.move_ip(xMove, yMove)
        self.coord_x = coord_x
        self.coord_y = coord_y