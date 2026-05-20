from Simulation.Classes import creatures as c, board as b, stations as s, champions as ch
from Simulation.Classes.stations import HackedState
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np
import time
import copy

pygame.init()

#################################################################################
# USER INPUT
# set small board size such as 2x2 and use grave to easily visualize high vs low discard method
board = b.Board(4, 4)
station = s.Portal(5, HackedState.NORMAL)
# resource is only used in High/Low discard
resource = 1e6
champion = ch.Rival()
#################################################################################

cellSize = 100
sidePanelWidth = 220
infoWidth = 220

width = board.columns*cellSize + sidePanelWidth + infoWidth
height = max(board.rows*cellSize, 5*cellSize)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

simulationGenerator = None
simulationMode = None
runningSimulation = False
lastStepTime = 0

# Delay between merge operations in milliseconds
mergeDelay = 500

def mergeOnce():
    global runningSimulation
    global simulationMode

    simulationMode = "instant"
    runningSimulation = True

def mergeContinuous():
    global runningSimulation
    global simulationMode

    simulationMode = "continuous"
    runningSimulation = True

def toggleSimulation():
    global runningSimulation
    runningSimulation = not runningSimulation

def fillBoard():
    for i in range(board.size):
        if c.Empty(0) in board.contents:
            board.generate(station)

def resetBoard():
    global runningSimulation
    global simulationGenerator
    global simulationMode

    runningSimulation = False
    simulationGenerator = None
    simulationMode = None

    board.reset()

def mergeHighDiscard():
    global simulationGenerator
    global runningSimulation
    global simulationMode

    simulationMode = "highDiscard"
    board.reset()
    simulationGenerator = board.highDiscardSim(station,resource,champion)

    runningSimulation = True

def mergeLowDiscard():
    global simulationGenerator
    global runningSimulation
    global simulationMode

    simulationMode = "lowDiscard"
    board.reset()
    simulationGenerator = board.lowDiscardSim(station, resource, champion)

    runningSimulation = True

mergeOnceButton = Button(
    screen,
    board.columns*cellSize + 10,
    20,
    200,
    50,
    text="Merge Once",fontSize=24,margin=20,inactiveColour="cadetblue2",
    hoverColour="chartreuse2",pressedColour="chartreuse2",onClick=mergeOnce
)

mergeContinuousButton = Button(
    screen,
    board.columns*cellSize + 10,
    90,
    200,
    50,
    text="Merge Continuous",fontSize=24,margin=20,inactiveColour="cadetblue2",
    hoverColour="chartreuse2",pressedColour="chartreuse2",onClick=mergeContinuous
)

pauseButton = Button(
    screen,
    board.columns*cellSize + 10,
    160,
    200,
    50,
    text="Pause",fontSize=24,margin=20,inactiveColour="cadetblue2",
    hoverColour="chartreuse2",pressedColour="chartreuse2",onClick=toggleSimulation
)

fillButton = Button(
screen,
    board.columns*cellSize + 10,
    230,
    95,
    50,
    text="Fill",fontSize=24,margin=20,inactiveColour="cadetblue2",
    hoverColour="orange",pressedColour="orange",onClick=fillBoard
)

resetButton = Button(
    screen,
    fillButton.getX() + 105,
    230,
    95,
    50,
    text="Reset",fontSize=24,margin=20,inactiveColour="cadetblue2",
    hoverColour="orange",pressedColour="orange",onClick=resetBoard
)

speedSlider = Slider(
    screen,
    board.columns*cellSize + 20,
    340,
    180,
    20,
    min=10,max=1000,step=10,initial=250
)

speedOutput = TextBox(
    screen,
    board.columns*cellSize + 60,
    370,
    100,
    40,
    fontSize=24
)

mergeHighDiscardButton = Button(
    screen,
    board.columns*cellSize + sidePanelWidth + 10,
    20,
    200,
    50,
    text="High Discard", fontSize=24, margin=20, inactiveColour="cadetblue2",
    hoverColour="chartreuse2", pressedColour="chartreuse2", onClick=mergeHighDiscard
)

mergeLowDiscardButton = Button(
    screen,
    board.columns*cellSize + sidePanelWidth + 10,
    90,
    200,
    50,
    text="Low Discard", fontSize=24, margin=20, inactiveColour="cadetblue2",
    hoverColour="chartreuse2", pressedColour="chartreuse2", onClick=mergeLowDiscard
)

boardInfo = TextBox(
    screen,
    board.columns*cellSize + sidePanelWidth + 10,
    160,
    200,
    250,
)

def draw_board():
    boardDisplay = np.array(board.contents).reshape(board.rows, board.columns)

    for row in range(board.rows):
        for col in range(board.columns):
            rect = pygame.Rect(col*cellSize,row*cellSize,cellSize,cellSize)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            creature = boardDisplay[row][col]
            if creature != c.Empty(0):
                image = pygame.image.load(creature.imagePath)
                image = pygame.transform.scale(image, (cellSize, cellSize))
                screen.blit(image, (col*cellSize, row*cellSize))

font = pygame.font.SysFont(None, 30)
def draw_text():
    speedLabel = font.render("Merge Delay (ms)", True, (255, 255, 255))
    screen.blit(speedLabel, (board.columns*cellSize + 25, 300))

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill("cadetblue4")

    mergeDelay = speedSlider.getValue()
    speedOutput.setText(str(mergeDelay))

    currentTime = pygame.time.get_ticks()

    if runningSimulation:
        if currentTime - lastStepTime > mergeDelay:
            info = ""

            if simulationGenerator is not None:
                try:
                    state = next(simulationGenerator)
                    currentBoard = state[0]
                    currentResources = state[2]
                    board.contents = currentBoard

                    info += f"Resources Left:\n{currentResources:,.0f}\n\n"
                except StopIteration:
                    runningSimulation = False
                    simulationGenerator = None
            elif simulationMode == "continuous":
                previousState = copy.deepcopy(board.contents)
                board.mergeOnce()

                if board.contents == previousState:
                    runningSimulation = False
            elif simulationMode == "instant":
                board.mergeOnce()
                runningSimulation = False

            currentChampionList = board.championList
            for champ in currentChampionList:
                info += f"{champ.name}: {champ.points / champ.spawnPoints:.3f}\n"
            boardInfo.setText(info)

            lastStepTime = currentTime

    draw_board()
    draw_text()

    pygame_widgets.update(events)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()