import pygame
import sys
from helpers import load_image

class GUI:
    def __init__(self, game, width=800,height=431):
        self.game = game
        self.width = width
        self.height = height
        self.background = pygame.image.load("data/images/board.png")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.space_dist = 45 
        self.stone_size = 47
            
    def start_main_loop(self):
        backgroundRect = self.background.get_rect()
        self.load_sprites()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            self.screen.blit(self.background, backgroundRect)
            self.one_stones.draw(self.screen)
            pygame.display.flip()
            
    def load_sprites(self):
        self.one_stones = pygame.sprite.Group()
        self.two_stones = pygame.sprite.Group()
        
        xOff = 5
        yOff = 5
        
        """Create all of the pellets and add them to the 
        pellet_sprites group"""
        for y in range(5):
            for x in range(9):
                xPos = xOff + x*self.stone_size + x*self.space_dist
                yPos = yOff + y*self.stone_size + y*self.space_dist
                
                pos = (4-y) * 9 + x;
                stone = self.game.board.check(pos)
                
                if stone != 0:
                    self.one_stones.add(Stone(stone, pygame.Rect(xPos, yPos, self.stone_size, self.stone_size)))
    
class Stone(pygame.sprite.Sprite):
    """A game stone."""
    def __init__(self, player, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        
        if player == 1:
            img = 'one.png'
        elif player == 2:
            img = 'two.png'
        
        self.image, self.rect = load_image(img, -1)
        
        if rect != None:
            self.rect = rect