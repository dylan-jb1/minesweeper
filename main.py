from pygame import PixelArray, surface
from classHolder import *
import pygame
import pygame.freetype
import random
import time

pygame.init()
myfont = pygame.freetype.SysFont('Arial B', 0)

# screen size

boardSize = (30,24) # max x = 30 max y = 24 for stability

if boardSize[0] > 30:
    boardSize = (30,boardSize[1])
elif boardSize[1] > 24:
    boardSize = (boardSize[0],24)

mineNum = 150 # max 1 less than total squares on board

boardSquaresMinOne = (boardSize[0]*boardSize[1]) - 1

mineCount = mineNum if mineNum < boardSquaresMinOne else boardSquaresMinOne
screen = None

revealed = list()
revealedMines = list()
flagged = list()
gameState = "playing"
firstTime = None

mainScreenButtons = list()
gameButtons = dict()
setSum = dict()
mines = list()

mine = pygame.image.load("./assets/mine.png")
quitImage = pygame.image.load("./assets/quit.png")
refreshImage = pygame.image.load("./assets/refresh.png")
flagImage = pygame.image.load("./assets/flag.png")
crown = pygame.image.load("./assets/crown.png")

mineColours = [(100,100,255), (0,120,0), (255,100,100), (255,100,255), (40,120,120), (200,200,100), (100,100,100), (255,180,180)]

def quitButton():
    quit(0)

def reset(buttons):
    global gameState,screen,firstTime

    screenWidth = 30*boardSize[0] + 20

    firstTime = None

    del(screen)
    screen = pygame.display.set_mode((screenWidth if screenWidth >= 350 else 350, 30*boardSize[1] + 81))


    mainScreenButtons.clear()
    mainScreenButtons.append(Button(((screen.get_rect().width)/2 - 165,10), (100, 50), (10,10,10), (10,10,10), 10, (mineCount, (255,255,255), (255,255,255), (myfont), 20), {1: (lambda : 1, ())}))
    mainScreenButtons.append(Button(((screen.get_rect().width)/2 - 55,10), (50, 50), (10,10,10), (15,15,15), 10, (quitImage, 10), {1: (quitButton, ())}))
    mainScreenButtons.append(Button(((screen.get_rect().width)/2 + 5,10), (50, 50), (10,10,10), (15,15,15), 10, (refreshImage, 5), {1: (reset, (gameButtons,))}))
    mainScreenButtons.append(Button(((screen.get_rect().width)/2 + 65,10), (100, 50), (10,10,10), (10,10,10), 10, ("0", (255,255,255), (255,255,255), (myfont), 30), {1: (lambda : 1, ())}))

    buttons.clear()
    gameButtons.clear()
    for y in range(boardSize[1]):
        for x in range(boardSize[0]):
            buttons[(x,y)] = Button((11 + x*30 + ((350/2) - (15*boardSize[0]) - 10 if 30*boardSize[0] < 350 else 0),71 + y*30), (28, 28), (120,120,120), (80,80,80), 2, ("", (100,100,100), (100,100,100), myfont, 30), {1: (revealCurrent, ((x,y),gameButtons, setSum, mines)), 3: (flag, ((x,y),gameButtons))})
            setSum[(x,y)] = 0
    
    mines.clear()
    for mine in range(mineCount):

        x,y = random.randrange(0,boardSize[0]),random.randrange(boardSize[1])
        while (x,y) in mines:
            x,y = random.randrange(0,boardSize[0]),random.randrange(boardSize[1])
        mines.append((x,y))

        for j in range(-1,2):
            for k in range(-1,2):
                if (x+j >= 0 and y+k >= 0) and (x+j < boardSize[0] and y+k < boardSize[1]):
                    if not (j== 0 and k == 0):
                        setSum[(x+j,y+k)] +=1

    revealedMines.clear()
    revealed.clear()
    for x in flagged:
        flag(x,buttons)
    flagged.clear()
    gameState = "playing"

def flag(buttonID, buttonSet):
    if buttonID not in revealed:
        if buttonID in flagged:
            flagged.remove(buttonID)

            buttonSet[buttonID].dataType = "text"

            buttonSet[buttonID].text = ""
            buttonSet[buttonID].textCol = (255,255,255)
            buttonSet[buttonID].textHovCol = (255,255,255)
            buttonSet[buttonID].textFont = myfont
            buttonSet[buttonID].fontSize = 10
        else:
            flagged.append(buttonID)

            buttonSet[buttonID].dataType = "image"
            buttonSet[buttonID].image = flagImage
            buttonSet[buttonID].padding = 0

def revealCurrent(buttonID, buttonSet, sumSet, mineList):
    global gameState, masterButton, firstTime

    if firstTime == None:
        firstTime = time.time()

    if buttonID not in revealed and buttonID not in flagged:
        if buttonID not in mineList:

            buttonSet[buttonID].colourDefault = (200,200,200)
            buttonSet[buttonID].colourHover = (200,200,200)

            revealed.append(buttonID)

            mineVal = sumSet[buttonID]

            if mineVal != 0:
                buttonSet[buttonID].dataType = "text"
                buttonSet[buttonID].text = str(mineVal)
                buttonSet[buttonID].textCol = mineColours[mineVal-1]
                buttonSet[buttonID].textHovCol = mineColours[mineVal-1]
                buttonSet[buttonID].textFont = myfont
                buttonSet[buttonID].fontSize = 30
            else:
                for j in range(-1,2):
                    for k in range(-1,2):
                        if (buttonID[0]+j >= 0 and buttonID[1]+k >= 0) and (buttonID[0]+j < boardSize[0] and buttonID[1]+k < boardSize[1]):
                            if not (j== 0 and k == 0) and (buttonID[0]+j, buttonID[1]+k) not in revealed:
                                revealCurrent((buttonID[0]+j, buttonID[1]+k), buttonSet, sumSet, mineList)

            #win condition
            if len(revealed) >= ((boardSize[0]*boardSize[1]) - mineCount):
                gameState = "won"
        else:
            buttonSet[buttonID].colourDefault = (255,0,0)
            buttonSet[buttonID].colourHover = (255,0,0)

            buttonSet[buttonID].dataType = "image"
            buttonSet[buttonID].image = mine
            buttonSet[buttonID].padding = 0

            if buttonID not in revealedMines:
                gameState = "lost"
                for x in mineList:
                    if x != buttonID:
                        revealedMines.append(x)
                        revealCurrent(x, buttonSet, sumSet, mineList)

            revealedMines.append(buttonID)

reset(gameButtons)

while 1:
    screen.fill((50,50,60))
    event = pygame.event.get()
    for ev in event:
        for x in mainScreenButtons:
            x.press(ev)
        if gameState == "playing":
            for x in gameButtons:
                gameButtons[x].press(ev)

    if gameState == "won" and mainScreenButtons[0].dataType == "text":
        mainScreenButtons[0].dataType = "image"
        mainScreenButtons[0].image = crown
        mainScreenButtons[0].padding = 15
    else:
        mainScreenButtons[0].text = "Mines:" + str(mineCount - len(flagged)).rjust(3)

    if gameState != "lost" and gameState != "won":
        mainScreenButtons[3].text = "{:02d}:{:02d}".format(round(time.time() - firstTime) // 60, round(time.time() - firstTime) % 60) if firstTime != None else "00:00"
    elif gameState == "lost":
        mainScreenButtons[3].textCol = (255,0,0)
        mainScreenButtons[0].textCol = (255,0,0)
        mainScreenButtons[3].textHovCol = (255,0,0)
        mainScreenButtons[0].textHovCol = (255,0,0)
    else:
        mainScreenButtons[3].textCol = (0,255,0)
        mainScreenButtons[0].textCol = (0,255,0)
        mainScreenButtons[3].textHovCol = (0,255,0)
        mainScreenButtons[0].textHovCol = (0,255,0)

    for x in mainScreenButtons:
        x.draw(screen)
    for x in gameButtons:
        gameButtons[x].draw(screen)

    pygame.display.flip()