import queue
import pygame

from enum import Enum

pygame.init()

#Class for the player object - Snake
class Snake:

    #Body part stats
    offsetBorder = 1
    sizeX = 25 - offsetBorder * 2
    sizeY = 25 - offsetBorder * 2
    colour = (255,0,0)

    #Eye stats
    eyeOffsetX = 3
    eyeOffsetY = 3
    eyeSizeX = 8
    eyeSizeY = 8
    colourEye = (255,255,255)

    #Pupil stats
    pupilOffsetX = 2
    pupilOffsetY = 2
    pupilX = 4
    pupilY = 4
    colourPupil = (0,0,0)
    
    #For food purposes
    ateFood = False

    def __init__(self):
        self.SetupSnake()
        
    #Setting up start of game
    def SetupSnake(self):
        self.alive = True
        self.ateFood = False
        self.direction = Direction.Down
        self.previousDirection = self.direction
        self.position = Position(0, 2)

        #Queue which contains the tail, used for manipulating where the tail is and how to change that in the map
        #The element to pop = end of tail
        #The element to push = start tail after head
        self.tailQueue = queue.Queue()
        self.tailQueue.put(Tail(Position(0, 0)))
        self.tailQueue.put(Tail(Position(0, 1)))

    #Update snake
    def Update(self):

        #If dead, do not update
        if not(self.alive):
            return

        #Check key input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not(self.previousDirection == Direction.Right):
            self.direction = Direction.Left

        if keys[pygame.K_RIGHT] and not(self.previousDirection == Direction.Left):
            self.direction = Direction.Right

        if keys[pygame.K_UP] and not(self.previousDirection == Direction.Down):
            self.direction = Direction.Up

        if keys[pygame.K_DOWN] and not(self.previousDirection == Direction.Up):
            self.direction = Direction.Down
    
    def LegalMove(self, gameMap):
        
        if self.direction == Direction.Up:
            if self.position.Y - 1 < 0:
                return False
            elif gameMap[self.position.X][self.position.Y - 1] == 1:
                return False
            else:
                return True
        elif self.direction == Direction.Down:
            if self.position.Y + 1 >= gameMap.shape[1]:
                return False
            elif gameMap[self.position.X][self.position.Y + 1] == 1:
                return False
            else:
                return True
        elif self.direction == Direction.Left:
            if self.position.X - 1 < 0:
                return False
            elif gameMap[self.position.X - 1][self.position.Y] == 1:
                return False
            else:
                return True
        else: #Direction.Right
            if self.position.X + 1 >= gameMap.shape[0]:
                return False
            elif gameMap[self.position.X + 1][self.position.Y] == 1:
                return False
            else:
                return True

    def OnTopOfFood(self, foodPos):

        # print('SnakePos: ' + str(self.position.X) + ' ' + str(self.position.Y))
        # print('foodPos: ' + str(foodPos.X) + ' ' + str(foodPos.Y))
        if foodPos.X == self.position.X and foodPos.Y == self.position.Y:
            self.ateFood = True
            return
        else:        
            self.ateFood = False

    def Move(self, gameMap, food):
        

        #Change current position of head to tail
        self.tailQueue.put(Tail(Position(self.position.X, self.position.Y)))
        gameMap[self.position.X][self.position.Y] = 1

        self.previousDirection = self.direction

        #Move head part of snake
        if self.direction == Direction.Up:
            self.position.Y -= 1
        elif self.direction == Direction.Down:
            self.position.Y += 1
        elif self.direction == Direction.Left:
            self.position.X -= 1
        else:
            self.position.X += 1

        self.OnTopOfFood(food.position)
        #Move last part of tail if the snake did not eat the food
        if not(self.ateFood):
            end = self.tailQueue.get()
            gameMap[end.position.X][end.position.Y] = 0           
        else:
            self.ateFood = True


        gameMap[self.position.X][self.position.Y] = 2
        

    def DrawHead(self, screen, position):

        #Head
        pygame.draw.rect(screen, self.colour, (position.X + self.offsetBorder, position.Y + self.offsetBorder, self.sizeX, self.sizeY))

        if(self.direction == Direction.Up):

            #Eye left + pupil
            eyeLeftPosX = position.X + self.offsetBorder + self.eyeOffsetX
            eyeLeftPosY = position.Y + self.offsetBorder + self.eyeOffsetY
            pupilLeftPosX = eyeLeftPosX + self.pupilOffsetX
            pupilLeftPosY = eyeLeftPosY


            pygame.draw.rect(screen, self.colourEye, (eyeLeftPosX, eyeLeftPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilLeftPosX, pupilLeftPosY, self.pupilX, self.pupilY))
            
            #Eye right + pupil
            eyeRightPosX = position.X + self.offsetBorder + self.sizeX - self.eyeOffsetX - self.eyeSizeX
            eyeRightPosY = position.Y + self.offsetBorder + self.eyeOffsetY
            pupilRightPosX = eyeRightPosX + self.pupilOffsetX
            pupilRightPosY = eyeRightPosY

            pygame.draw.rect(screen, self.colourEye, (eyeRightPosX, eyeRightPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilRightPosX, pupilRightPosY, self.pupilX, self.pupilY))

        elif self.direction == Direction.Down:
            #Eye left + pupil
            eyeLeftPosX = position.X + self.offsetBorder + self.sizeX - self.eyeOffsetX - self.eyeSizeX
            eyeLeftPosY = position.Y + self.offsetBorder + self.sizeY - self.eyeOffsetY - self.eyeSizeY
            pupilLeftPosX = eyeLeftPosX + self.pupilOffsetX
            pupilLeftPosY = eyeLeftPosY + self.eyeSizeY - self.pupilY

            pygame.draw.rect(screen, self.colourEye, (eyeLeftPosX, eyeLeftPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilLeftPosX, pupilLeftPosY, self.pupilX, self.pupilY))

            #Eye right + pupil
            eyeRightPosX = position.X + self.offsetBorder + self.eyeOffsetX
            eyeRightPosY = position.Y + self.offsetBorder + self.sizeY - self.eyeOffsetY - self.eyeSizeY
            pupilRightPosX = eyeRightPosX + self.pupilOffsetX
            pupilRightPosY = eyeRightPosY + self.eyeSizeY - self.pupilY

            pygame.draw.rect(screen, self.colourEye, (eyeRightPosX, eyeRightPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilRightPosX, pupilRightPosY, self.pupilX, self.pupilY))
        
        elif self.direction == Direction.Left:
            #Eye left + pupil
            eyeLeftPosX = position.X + self.offsetBorder + self.eyeOffsetX
            eyeLeftPosY = position.Y + self.offsetBorder + self.sizeY - self.eyeOffsetY - self.eyeSizeY
            pupilLeftPosX = eyeLeftPosX
            pupilLeftPosY = eyeLeftPosY + self.pupilOffsetY

            pygame.draw.rect(screen, self.colourEye, (eyeLeftPosX, eyeLeftPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilLeftPosX, pupilLeftPosY, self.pupilX, self.pupilY))

            #Eye right + pupil
            eyeRightPosX = position.X + self.offsetBorder + self.eyeOffsetX
            eyeRightPosY = position.Y + self.offsetBorder + self.eyeOffsetY
            pupilRightPosX = eyeRightPosX
            pupilRightPosY = eyeRightPosY + self.pupilOffsetY

            pygame.draw.rect(screen, self.colourEye, (eyeRightPosX, eyeRightPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilRightPosX, pupilRightPosY, self.pupilX, self.pupilY))
        
        #Direction is Right
        else:
            #Eye left + pupil
            eyeLeftPosX = position.X + self.offsetBorder + self.sizeX - self.eyeOffsetX - self.eyeSizeX
            eyeLeftPosY = position.Y + self.offsetBorder + self.eyeOffsetY
            pupilLeftPosX = eyeLeftPosX + self.eyeSizeX - self.pupilX
            pupilLeftPosY = eyeLeftPosY + self.pupilOffsetY

            pygame.draw.rect(screen, self.colourEye, (eyeLeftPosX, eyeLeftPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilLeftPosX, pupilLeftPosY, self.pupilX, self.pupilY))

            #Eye right + pupil
            eyeRightPosX = position.X + self.offsetBorder + self.sizeX - self.eyeOffsetX - self.eyeSizeX
            eyeRightPosY = position.Y + self.offsetBorder + self.sizeY - self.eyeOffsetY - self.eyeSizeY
            pupilRightPosX = eyeRightPosX + self.eyeSizeX - self.pupilX
            pupilRightPosY = eyeRightPosY + self.pupilOffsetY

            pygame.draw.rect(screen, self.colourEye, (eyeRightPosX, eyeRightPosY, self.eyeSizeX, self.eyeSizeY))
            pygame.draw.rect(screen, self.colourPupil, (pupilRightPosX, pupilRightPosY, self.pupilX, self.pupilY))
    

    def DrawTail(self, screen, position):
        pygame.draw.rect(screen, self.colour, (position.X + self.offsetBorder, position.Y + self.offsetBorder, self.sizeX, self.sizeY))

#Class which saves the X and Y values of an object
class Position:

    def __init__(self, posX = 0, posY = 0):
        self.X = posX
        self.Y = posY

class Direction(Enum):
 
    Left = 1
    Right = 2
    Up = 3
    Down = 4

class Tail:

    def __init__(self, pos):

        #Coordinates is in indices
        self.position = pos

