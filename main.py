from pygame import surface
from classHolder import *
import pygame
import pygame.freetype

def quitButton():
    quit(0)

def revealCurrent(buttonID, buttonArr):
    buttonArr[buttonID[0]*10 + buttonID[1]].colDef = (0,0,0)
    buttonArr[buttonID[0]*10 + buttonID[1]] = buttonArr[buttonID[0]*10 + buttonID[1]]
    print(buttonID)


pygame.init()
myfont = pygame.freetype.SysFont('Courier New', 0)

screen = pygame.display.set_mode((700,700))

mainScreenButtons = list()

image = pygame.image.load("./test.png")

mainScreenButtons.append(Button((10,10), (100, 50), (10,10,10), (15,15,15), 10, ("Quit", (100,100,100), (100,100,100), myfont, 40), quitButton, ()))
mainScreenButtons.append(Button((10,110), (100, 50), (255,255,255), (200,200,200), 0, (image, 5), quitButton, ()))


mines = 40
boardSize = (16,16)

gameButtons = list()
for y in range(boardSize[1]):
    for x in range(boardSize[0]):
        gameButtons.append(Button((11 + x*30,176 + y*30), (28, 28), (255,255,255), (200,200,200), 2, ("", (100,100,100), (100,100,100), myfont, 30), revealCurrent, ((x,y),gameButtons)))

gameButtons[0].colDef = (0,0,0)

while 1:
    screen.fill((50,50,60))
    event = pygame.event.get()
    for ev in event:
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for x in mainScreenButtons:
                x.press()
            for x in gameButtons:
                x.press()

    for x in mainScreenButtons:
        x.draw(screen)
    for x in gameButtons:
        x.draw(screen)

    pygame.display.flip()