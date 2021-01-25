import pygame
from Snake import Position

pygame.init()
myfont = pygame.font.SysFont(pygame.font.get_default_font(), 50)
colourGameOver = (200, 200, 200)
gameoverText = 'Game Over'
text = myfont.render(gameoverText, 1, colourGameOver)

class GameUI:

    #BaseUI stats
    posUI = Position(0,0)

    widthUI = 500
    heightUI = 100
    borderWidth = 3

    UIPoints = [
     (0,1),
     (0, heightUI - borderWidth + 2),
     (widthUI - borderWidth + 2, heightUI - borderWidth + 2),
     (widthUI - borderWidth + 2, 1)
     ]

    colourUI = (0, 0, 200)
    colourUIBorder = (200, 200, 200)

    def __init__(self):
        self.score = 0

    def Update(self, gotFood):
        
        if gotFood:
            self.score += 10

    def DrawGame(self, screen, snakeAlive):
        
        #Draw base
        pygame.draw.polygon(screen, self.colourUI, self.UIPoints)
        pygame.draw.lines(screen, self.colourUIBorder, True, self.UIPoints, self.borderWidth)

        #Draw game over if snake is dead
        if not(snakeAlive):
            screen.blit(text, (250 - text.get_rect().width / 2, 350 - text.get_rect().height / 2))
