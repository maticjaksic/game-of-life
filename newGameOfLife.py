
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
    global xyAlive
    xyAlive = []
    global boardArray
    global arrayWidth
    global arrayHeight
    arrayWidth = width
    arrayHeight = height
    boardArray= [ [0]*width for i in range(height)] 
    

def drawCell(surface,color,left,top,sideLength):
    pygame.draw.rect(surface, color, pygame.Rect(left,top,sideLength,sideLength))

def drawXY():
    # print(xyAlive)
    for i in xyAlive:      
        drawCell(screen,aliveRGB,i[0]*cellSize,i[1]*cellSize,cellSize)




# def updateBoardArray(array):
#     oldArray = [0]*arrayWidth
#     for x in range(arrayWidth):   
#         firstLineArray = [0]*arrayWidth
#         for y in range(arrayHeight):
#             if (y >= arrayWidth-1 or x >= arrayHeight-1) == False:               
#                 firstLineArray[y] = getState(x,y)

#         if x != 0:      
#             array[x-1] = oldArray
#         oldArray = firstLineArray

#     return array
def updateBoardArray(array):
    newArray = []
    for coords in array:
        # vse zive
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # vsi sosedje in celica
                coord = getState([dx + coords[0], dy + coords[1]])
                isInside = 0
                if coord != None:
                    for i in newArray:
                        if i == coord:
                            isInside = 1
                            break
                    if isInside == 0:
                        newArray.append(coord)

    return newArray

def getState(xy):
    
    counter = 0
    state = 0
    # found = False
    for i in xyAlive:
        if i == xy:
            state = 1
            break


    searchCoord = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if not(dx == 0 and dy == 0):
                searchCoord.append([dx + xy[0],dy + xy[1]])

    counter = len(list(filter(lambda x: x in xyAlive , searchCoord)))

    newState = 0

    if counter + state == 3:
        newState = 1
    if counter + state == 4:
        newState = state

    if newState == 1:
        return xy
    else: 
        return

# def writeState(x,y,state):
#     boardArray[x][y] = state

def writeState(x,y):
    xyAlive.append([x,y])
######################################################################################################################
def drawShape(x,y,array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 1:
                writeState(i+x,j+y)

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
setupArray(500,500)   #height,width
setupScreen(2)     #cell pixel size

# drawBlinker(20,20)

# drawGlider(5,5)
# drawLightWeightSpaceship(50,50)

# drawRPentomino(250,250)

drawGliderGun(50,50)

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
                  
        xyAlive = updateBoardArray(xyAlive)
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

    if generations % 30 == 1:
        dispFps = averageFps
        
    fpsText = font.render(str(round(dispFps,1))+" fps", True,(255,255,255))
    screen.blit(fpsText,(5,25))


    drawXY()
    pygame.display.update()
    
    clock.tick()    