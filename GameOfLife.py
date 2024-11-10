import pygame
import random

clock = pygame.time.Clock()
fps = 480

running = True

aliveRGB = (255,255,255)
deadRGB = (20,20,20)
#####################################################################################################################

def setupScreen(size):
    global screen
    global cellSize
    cellSize = size
    (width, height) = (cellSize*arrayHeight, cellSize*arrayWidth)
    screen = pygame.display.set_mode((width, height))

def setupArray(width, height):
    global boardArray
    global arrayWidth
    global arrayHeight
    arrayWidth = width
    arrayHeight = height
    boardArray= [ [0]*width for i in range(height)] 

def drawCell(surface,color,left,top,sideLength):
    pygame.draw.rect(surface, color, pygame.Rect(left,top,sideLength,sideLength))

def drawArray():
    for x in range(arrayHeight):
        for y in range(arrayWidth):
            if boardArray[x][y] == 1:
                drawCell(screen,aliveRGB,x*cellSize+1,y*cellSize+1,cellSize-2)
            else:
                drawCell(screen,deadRGB,x*cellSize+1,y*cellSize+1,cellSize-2)

# def updateBoardArray(array):
#     newBoardArray = [ [0]*arrayWidth for i in range(arrayHeight)]
#     for x in range(arrayWidth):
#         for y in range(arrayHeight):
#             if (x == 0 or y >= arrayWidth-1 or y == 0 or x >= arrayHeight-1) == False:
                
#                 newBoardArray[x][y] = getState(x,y)
#     if array == newBoardArray:
#         global simulating
#         simulating = False
#     array = []
#     array = newBoardArray
#     return array

def updateBoardArray(array):
    oldArray = [0]*arrayWidth
    for x in range(arrayWidth):   
        firstLineArray = [0]*arrayWidth
        for y in range(arrayHeight):
            if (y >= arrayWidth-1 or x >= arrayHeight-1) == False:               
                firstLineArray[y] = getState(x,y)

        if x != 0:      
            array[x-1] = oldArray
        oldArray = firstLineArray

    return array
                
            
def getState(x,y):
   
    state = boardArray[x][y]

    counter = 0

    # if boardArray[x-1][y-1] == 1:
    #     counter += 1
    # if boardArray[x][y-1] == 1:
    #     counter += 1
    # if boardArray[x+1][y-1] == 1:
    #     counter += 1
    # if boardArray[x-1][y] == 1:
    #     counter += 1
    # if boardArray[x+1][y] == 1:
    #     counter += 1
    # if boardArray[x-1][y+1] == 1:
    #     counter += 1
    # if boardArray[x][y+1] == 1:
    #     counter += 1
    # if boardArray[x+1][y+1] == 1:
    #     counter += 1

    counter = boardArray[x-1][y-1] + boardArray[x][y-1] + boardArray[x+1][y-1] + boardArray[x-1][y] + boardArray[x+1][y] + boardArray[x-1][y+1] + boardArray[x][y+1] + boardArray[x+1][y+1]

    newState = 0
    # if state == 1 and (counter == 2 or counter == 3):
    #     newState = 1
    # elif state == 1:
    #     newState = 0
    # if state == 0 and counter == 3:
    #     newState = 1
    # elif state == 0:
    #     newState = 0
    if state + counter == 3:
        newState = 1
    if state + counter == 4:
        newState = state

    return newState

def writeState(x,y,state):
    boardArray[x][y] = state
######################################################################################################################
def drawBlinker(x,y):
    writeState(x,y,1)
    writeState(x,y+1,1)
    writeState(x,y+2,1)

def drawGlider(x,y):
    writeState(x,y,1)
    writeState(x+2,y,1)
    writeState(x+1,y+1,1)
    writeState(x+2,y+1,1)
    writeState(x+1,y+2,1)

def drawLightWeightSpaceship(x,y):
    writeState(x+1,y,1)
    writeState(x+2,y,1)
    writeState(x+3,y,1)
    writeState(x+4,y,1)
    writeState(x+5,y,1)
    writeState(x,y+1,1)
    writeState(x+5,y+1,1)
    writeState(x+5,y+2,1)
    writeState(x+4,y+3,1)
    writeState(x,y+3,1)
    writeState(x+2,y+4,1)

def drawRPentomino(x,y):
    writeState(x+1,y,1)
    writeState(x+2,y,1)
    writeState(x+1,y+1,1)
    writeState(x,y+1,1)
    writeState(x+1,y+2,1)
            
#####################################################################################################################
setupArray(100,100)#height,width
setupScreen(5)#cell pixel size

# drawBlinker(4,4)
# drawGlider(5,5)
# drawLightWeightSpaceship(10,180)

drawRPentomino(50,50)

simulating = True
pygame.init()
FPS = clock.get_fps()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keypressed = pygame.key.get_pressed()

    if simulating:######################################            SIMULATING             #######################################
        if keypressed[pygame.K_SPACE]:
            if wasPressed == 0:
                simulating = False
                wasPressed = 1
        else:
            wasPressed = 0        
                  
        boardArray = updateBoardArray(boardArray)
        FPS = (clock.get_fps() + FPS)/2 
    else:###############################################              EDITING              #######################################
        if keypressed[pygame.K_SPACE]:
            if wasPressed == 0:
                simulating = True
                wasPressed = 1
        else:
            wasPressed = 0

        if keypressed[pygame.K_RIGHT]:
            if wasPressedRight == 0:
                boardArray = updateBoardArray(boardArray)
                wasPressedRight = 1
        else:
            wasPressedRight = 0

        
        print(pygame.time.get_ticks())
        print(clock.get_fps(), FPS)
        running = False 
        ###########################################################################################################################
    drawArray()
    pygame.display.update()
    
    clock.tick()    