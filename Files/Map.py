import numpy as np

class Map():

    tileSizeX = 25
    tileSizeY = 25

    #Width and Height is amount of tiles, not amount of pixels
    def __init__(self, width, height):

        self.width = (int)(width / self.tileSizeX)
        self.height = (int)(height / self.tileSizeY)

        #Create 1 list with proper width
        oneList = []
        for i in range(0, self.width, 1):
            oneList.append(0)
        
        #Now create 1 giant list with the proper width lists
        allLists = []
        for i in range(0, self.height, 1):
            allLists.append(oneList)

        self.field = np.array(allLists)
    
    def getFieldFree(self):

        return np.where(self.field == 0)
    
    def getFieldSnakeHead(self):

        return np.where(self.field == 2)
    
    def getFieldSnakeTail(self):

        return np.where(self.field == 1)
    
    def getFieldFood(self):
        return np.where(self.field == 5)