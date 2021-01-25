import pygame
from Map import Map
from Snake import Position

class Food:

    colourFood = (255, 255, 255)
    offsetCenterPos = Position(12, 12)
    offsetUI = 100
    foodRadius = 10

    def __init__(self, pos):
        self.position = pos

    def Draw(self, screen, gameMap):
        
        #Position of food
        xValue = self.position.X * gameMap.tileSizeX  + self.offsetCenterPos.X
        yValue = self.position.Y * gameMap.tileSizeY + self.offsetCenterPos.Y + self.offsetUI

        pygame.draw.circle(screen, self.colourFood, (xValue, yValue),self.foodRadius)
