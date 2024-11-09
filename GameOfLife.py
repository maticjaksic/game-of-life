import pygame 
clock = pygame.time.Clock()
fps = 8

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

def updateBoardArray(array):
    newBoardArray = [ [0]*arrayWidth for i in range(arrayHeight)]
    for x in range(arrayWidth):
        for y in range(arrayHeight):
            if (x == 0 or y >= arrayWidth-1 or y == 0 or x >= arrayHeight-1) == False:
                
                newBoardArray[x][y] = getState(x,y)
    array = []
    array = newBoardArray
    return array
                
            
def getState(x,y):
   
    state = boardArray[x][y]

    counter = 0

    if boardArray[x-1][y-1] == 1:
        counter += 1
    if boardArray[x][y-1] == 1:
        counter += 1
    if boardArray[x+1][y-1] == 1:
        counter += 1
    if boardArray[x-1][y] == 1:
        counter += 1
    if boardArray[x+1][y] == 1:
        counter += 1
    if boardArray[x-1][y+1] == 1:
        counter += 1
    if boardArray[x][y+1] == 1:
        counter += 1
    if boardArray[x+1][y+1] == 1:
        counter += 1

    
    if state == 1 and (counter == 2 or counter == 3):
        newState = 1
    elif state == 1:
        newState = 0
    if state == 0 and counter == 3:
        newState = 1
    elif state == 0:
        newState = 0

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

            
#####################################################################################################################
setupArray(200,300)#height,width
setupScreen(5)#cell pixel size

# drawBlinker(20,20)
drawGlider(20,10)
drawLightWeightSpaceship(10,20)

simulating = True

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
    else:###############################################              EDITING              #######################################
        if keypressed[pygame.K_SPACE]:
            if wasPressed == 0:
                simulating = True
                wasPressed = 1
        else:
            wasPressed = 0
        ###########################################################################################################################
    drawArray()
    pygame.display.update()
    clock.tick(fps)    