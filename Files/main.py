import numpy, pygame, sys, random
from enum import Enum
from Food import Food
from GameUI import GameUI
from Map import Map
from Snake import Snake, Position

# Initialize all the pygame module
pygame.init()

# Summary of pygame modules:
# 1) cdrom          - playback
# 2) cursors        - load cursor images, includes standard cursors
# 3) display        - control the display window or screen
# 4) draw           - draw simple shapes onto a Surface
# 5) event          - manage events and the event queue
# 6) font           - create and render TrueType fonts
# 7) image          - save and load images
# 8) joystick       - manage joystick devices
# 9) key            - manage the keyboard
# 10) mouse         - manage the mouse
# 11) sndarray      - manipulate sounds with numpy
# 12) surfarray     - manipulate images with numpy
# 13) time          - control timing
# 14) transform     - scale, rotate, and flip images

#Screen settings
screenWidth = 500
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

heightOffset = 100

#Class which contains the main game elements
class Main:

    startTimer = 250
    timer = startTimer

    def __init__(self):
        pygame.display.set_caption('First game - Snake')

        self.gameState = GameState.MainMenu

        self.setGame()
        
    
    #Setup game elements
    def setGame(self):

        self.win = False

        #Setup snake
        self.snake = Snake()

        #Setup map
        self.map = Map((int)(screenWidth), (int)(screenHeight - heightOffset))
        self.map.field[0,0] = 1
        self.map.field[0,1] = 1
        self.map.field[0,2] = 2

        self.InsertFood()

        #Setup UI
        self.UI = GameUI()

        #Setup timer
        self.clock = pygame.time.Clock()

    #Update game loop
    def Update(self):

        #Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #Check if game is done
        if self.win or not(self.snake.alive):
            self.Draw()
        elif self.snake.alive:

            #Update clock and timer
            self.clock.tick()
            self.timer -= self.clock.get_time()

            #Make a move when timer is 0
            if self.timer <= 0:
                self.Move()
                self.CheckWinCondition()
                self.Draw()              

            #Update Snake
            self.snake.Update()
            
        pygame.display.update()
        pygame.display.flip()

    #Method which contains elements of making a move
    def Move(self):
        self.timer = self.startTimer

        if self.snake.LegalMove(self.map.field):
            self.snake.Move(self.map.field, self.food)
            if self.snake.ateFood:
                self.InsertFood()
        else:
            self.snake.alive = False   

    def CheckWinCondition(self):

        emptySpaces = self.map.getFieldFree()
        if emptySpaces[0].size == 0:
            self.win = True

    #Method which is responsible for drawing all the elements
    def Draw(self):
            screen.fill((0, 0, 0))

            mapWidth = self.map.tileSizeX
            mapHeight = self.map.tileSizeY

            #Draw Food
            self.food.Draw(screen, self.map)

            #Draw Snake head
            headSnakePos = self.map.getFieldSnakeHead()
            pos = Position(headSnakePos[0][0] * mapWidth, headSnakePos[1][0] * mapHeight + heightOffset)
            self.snake.DrawHead(screen, pos)

            #Draw Snake Tail
            tailSnakePos = self.map.getFieldSnakeTail()
            count = (tailSnakePos[0].shape)[0]

            for x in range(count):
                self.snake.DrawTail(screen, Position(tailSnakePos[0][x] * mapWidth, tailSnakePos[1][x] * mapHeight + heightOffset))

            #Draw UI
            self.UI.DrawGame(screen, self.snake.alive)

    #Method responsible for putting food on the field
    def InsertFood(self):
        
        #Get empty spaces
        freeSpaces = self.map.getFieldFree()
        count = (freeSpaces[0].shape)[0]
        index = random.randint(0, count)
        
        self.map.field[freeSpaces[0][index], freeSpaces[1][index]] = 5

        self.food = Food(Position(freeSpaces[0][index], freeSpaces[1][index]))
        
class GameState(Enum):
    MainMenu = 1
    SnakeGame = 2

main = Main()

while 1:
    main.Update()


################################################################################################3

#Update loop
# while 1:
#     pygame.time.delay(10)


#     #Check for events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

    # keys = pygame.key.get_pressed()

    # if keys[pygame.K_LEFT]:
    #     x -= vel

    #     if x < 0:
    #         x = 0

    # if keys[pygame.K_RIGHT]:
    #     x += vel

    #     if x > screenWidth - playerWidth:
    #         x = screenWidth - playerWidth

    # if keys[pygame.K_UP]:
    #     y -= vel

    #     if y < 0:
    #         y = 0

    # if keys[pygame.K_DOWN]:
    #     y += vel

    #     if y > screenHeight - playerHeight:
    #         y = screenHeight - playerHeight

    # screen.fill((0, 0, 0))

    # Wordt getekend vanuit linker bovenhoek
    # pygame.draw.rect(screen, (255, 0, 0), (x, y, playerWidth, playerHeight))

    # pygame.display.update()

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         sys.exit()
    
#     screen.fill(black)
#     #screen.blit(...) - for drawing objects on the screen
#     pygame.display.flip()

