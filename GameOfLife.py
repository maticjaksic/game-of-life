import pygame

clock = pygame.time.Clock()
fps = 480

running = True

aliveRGB = (255,255,255)
deadRGB = (20,20,20)
pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 16)

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
                drawCell(screen,aliveRGB,x*cellSize,y*cellSize,cellSize)


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

    counter = boardArray[x-1][y-1] + boardArray[x][y-1] + boardArray[x+1][y-1] + boardArray[x-1][y] + boardArray[x+1][y] + boardArray[x-1][y+1] + boardArray[x][y+1] + boardArray[x+1][y+1] + state
    newState = 0
    
    if counter == 3:
        newState = 1
    if counter == 4:
        newState = state

    return newState

def writeState(x,y,state):
    boardArray[x][y] = state
######################################################################################################################
def drawShape(x,y,array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            writeState(i+x,j+y,array[i][j])

def drawBlinker(x,y):
    drawShape(x,y,[[1,1,1]])

def drawGliderGun(x,y):
    drawShape(x,y,[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],[1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

def drawGlider(x,y):
    drawShape(x,y,[[1,0,1],[0,1,1],[0,1,0]])


def drawLightWeightSpaceship(x,y):
    drawShape(x,y,[[0,1,1,1,1,1],[1,0,0,0,0,1],[0,0,0,0,0,1],[1,0,0,0,1,0],[0,0,1,0,0,0]])

def drawRPentomino(x,y):
    drawShape(x,y,[[0,1,1],[1,1,0],[0,1,0]])
#####################################################################################################################
setupArray(50,50)#height,width
setupScreen(20)#cell pixel size

# drawBlinker(50,50)
# drawGlider(5,5)
# drawLightWeightSpaceship(50,50)

# drawRPentomino(100,100)

drawGliderGun(0,0)

simulating = True

averageFps = clock.get_fps()
generations = 0
while running:
    screen.fill((0,0,0))

    generations += 1

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
        averageFps = (clock.get_fps() + averageFps)/2 
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
 
        ###########################################################################################################################

    genText = font.render(str(generations)+" gen", True,(255,255,255))
    screen.blit(genText,(5,5))

    if generations % 100 == 1:
        dispFps = averageFps
        
    fpsText = font.render(str(round(dispFps,0))+" fps", True,(255,255,255))
    screen.blit(fpsText,(5,25))

    drawArray()
    pygame.display.update()
    
    clock.tick()  