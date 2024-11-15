import sys
import pygame

clock = pygame.time.Clock()

running = True
xyAlive = []

aliveRGB = (255,255,255)
deadRGB = (20,20,20)

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 16)

#####################################################################################################################

def setupScreen(x,y):
    global screen
    global screenX
    global screenY
    screenX = x
    screenY = y
    screen = pygame.display.set_mode((x, y))
    global playerX
    global playerY
    playerX = 0
    playerY = 0
    global cellSize
    cellSize = 5

def drawCell(surface,color,left,top,sideLength):
    pygame.draw.rect(surface, color, pygame.Rect(left,top,sideLength,sideLength))

def drawXY():
    for i in xyAlive:
        drawAtX = ((i[0]*cellSize)+playerX)*zoom+(screenX // 2)
        drawAtY = ((i[1]*cellSize)+playerY)*zoom+(screenY // 2)
        if not(drawAtX < cellSize*(-1) or drawAtY < cellSize*(-1) or drawAtX > screenX or drawAtY > screenY):
            drawCell(screen,aliveRGB,drawAtX,drawAtY,(cellSize*zoom)+1)
        

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

def writeState(x,y):
    xyAlive.append([x,y])

def swichCell(pos):
    x = int(((pos[0]-screenX // 2)/ zoom - playerX)/cellSize)
    y = int(((pos[1]-screenY // 2)/ zoom - playerY)/cellSize)

    if [x, y] in xyAlive:
        del xyAlive[xyAlive.index([x,y])]
    else:
        xyAlive.append([x, y])
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
setupScreen(500,500)
fps = 10
moveSpeed = 100
zoom = 1

# drawBlinker(0,0)

# drawGlider(10,10)
# drawLightWeightSpaceship(50,50)

# drawRPentomino(250,250)

#drawGliderGun(-20,-20)

simulating = True

averageFps = clock.get_fps()
generations = 0
gameFps = fps
dt = clock.tick() / 1000
while running:
    screen.fill((0,0,0))

    

    for event in pygame.event.get():######################################            INPUTS            #######################################
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keypressed = pygame.key.get_pressed()

    if keypressed[pygame.K_UP]:
        playerY += moveSpeed*dt
    elif keypressed[pygame.K_DOWN]:
        playerY -= moveSpeed*dt
    if keypressed[pygame.K_LEFT]:
        playerX += moveSpeed*dt
    elif keypressed[pygame.K_RIGHT]:
        playerX -= moveSpeed*dt
    if keypressed[pygame.K_c]:
        playerX = 0
        playerY = 0
        zoom = 1
    if keypressed[pygame.K_f]:
        gameFps = fps
    if keypressed[pygame.K_s]:
        gameFps = 0
    if zoom < 5:
        if keypressed[pygame.K_z]:
            zoom += 0.8*zoom*dt
            moveSpeed -= 0.9*moveSpeed*dt
    if zoom > 0.2:
        if keypressed[pygame.K_x]:
            zoom -= 0.8*zoom*dt
            moveSpeed += 0.9*moveSpeed*dt


    if simulating:######################################            SIMULATING             #######################################
        if keypressed[pygame.K_SPACE]:
            if wasPressed == 0:
                simulating = False
                wasPressed = 1
        else:
            wasPressed = 0        
                  
        xyAlive = updateBoardArray(xyAlive)
        generations += 1
        averageFps = (clock.get_fps() + averageFps)/2

        if generations % 10 == 1:
            dispFps = averageFps

        dt = clock.tick(gameFps) / 1000
    else:###############################################              EDITING              #######################################
        if keypressed[pygame.K_SPACE]:
            if wasPressed == 0:
                simulating = True
                averageFps = clock.get_fps()
                wasPressed = 1
        else:
            wasPressed = 0

        if keypressed[pygame.K_m]:
            if wasPressedRight == 0:
                xyAlive = updateBoardArray(xyAlive)
                wasPressedRight = 1
                generations += 1
        else:
            wasPressedRight = 0
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not clicking:
                clicking = True
                swichCell(event.pos)
        else:
            clicking = False


        averageFps = (clock.get_fps() + averageFps)/2
        dispFps = averageFps
        dt = clock.tick() / 1000
        ###########################################################################################################################

    genText = font.render(str(generations)+" gen", True,(255,255,255))
    screen.blit(genText,(5,5))
    fpsText = font.render(str(round(dispFps,1))+" fps", True,(255,255,255))
    screen.blit(fpsText,(5,25))
    liveText = font.render(str(len(xyAlive))+" living", True,(255,255,255))
    screen.blit(liveText,(5,45))

    drawXY()
    pygame.display.update()
    
        