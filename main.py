import pygame
from pygame import *
import random

init()

screenSize = [1280, 720]
squareSize = 21
gridSize = 10
gapSize = 1
screen = display.set_mode(screenSize)
hintFontSize = 16
hintFont = pygame.font.SysFont("consolas", hintFontSize)
# fnt instead of font because font is taken. truly unfortunate
fps = 144
clock = time.Clock()
backgroundColor = (175, 175, 175)
hoverColor = (150, 150, 150)
activeColor = (0, 0, 0)
ruledOutColor = (255, 0, 0)
defaultSquareColor = (255, 255, 255)


class Square:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = Rect(x, y, w, h)
        self.drawnRect = Rect(x + gapSize + 1, y + gapSize + 1, w * 0.85, h * 0.85)
        # it would probably be a good idea to replace 1 with a variable that makes the distance from the side even on
        # all sides
        self.state = 0
        # rect is the actual square you click on, while drawnRect is the smaller one that appears when you click rect
        # state 0 is inactive, 1 is active (player thinks there is a block there), 2 is disabled (player thinks there
        # is not a block there)

    def drawX(self, surf, squareColor):
        draw.line(surf, squareColor, (self.x + (2 * gapSize) + 1, self.y + (2 * gapSize)),
                    (self.x + (2 * gapSize) + (self.w * 0.85) - 3, self.y + (2 * gapSize) + (self.h * 0.85) - 2),
                  width = int(squareSize / 7))
        draw.line(surf, squareColor, (self.x + self.w - (2 * gapSize) - 1, self.y + (2 * gapSize)),
                    (self.x + (2 * gapSize), self.y + (2 * gapSize) + (self.h * 0.85) - 2),
                  width = int(squareSize / 7))
        # i tried so so hard not to have magic numbers but the added 2s and 3s work and i don't know what number i
        # could possibly derive them from


class Puzzle:
    def __init__(self, size):
        xOffset = (screenSize[0] / 2) - ((size * (squareSize + 5) - 5) / 2)
        yOffset = (screenSize[1] / 2) - 200  # needs to change based on the puzzle numbers :)
        self.grid = [[Square((i * (squareSize + gapSize)) + xOffset, j * (squareSize + gapSize) + yOffset,
                             squareSize, squareSize) for i in range(size)] for j in range(size)]
        self.toggledSquares = [[False for i in range(size)] for j in range(size)]
        self.background = Rect(xOffset, yOffset, gridSize * (squareSize + gapSize), gridSize * (squareSize + gapSize))
        self.solution = [[random.randrange(2) for i in range(size)] for j in range(size)]
        print(self.solution)
        self.columnHints = [[] for i in range(size)]
        self.rowHints = [[] for i in range(size)]
        for i, row in enumerate(self.solution):  # create rowHints
            currentRowHint = 0
            for j, column in enumerate(row):
                if row[j]:
                    currentRowHint += 1
                elif currentRowHint:
                    self.rowHints[i].append(currentRowHint)
                    currentRowHint = 0
            if currentRowHint:
                self.rowHints[i].append(currentRowHint)
        for i in range(size):  # create columnHints
            currentColumnHint = 0
            for j in range(size):
                if self.solution[j][i]:
                    currentColumnHint += 1
                elif currentColumnHint:
                    self.columnHints[i].append(currentColumnHint)
                    currentColumnHint = 0
            if currentColumnHint:
                self.columnHints[i].append(currentColumnHint)

    def update(self, surf, dragging, squareClickedIsActive, mouseButton):
        # surf = surface
        mouseX, mouseY = mouse.get_pos()

        for row in self.grid:  # graphics for user interaction (filled square, hover color, X drawing)
            for square in row:
                squareColor = defaultSquareColor
                draw.rect(surf, (255, 255, 255), square.rect)

                if square.rect.collidepoint(mouseX, mouseY):
                    if dragging:
                        if mouseButton == 1:
                                square.state = 0 if squareClickedIsActive else 1
                        elif mouseButton == 3:
                                square.state = 0 if squareClickedIsActive else 2
                    else:
                        squareColor = hoverColor
                        draw.rect(surf, squareColor, square.rect)

                if not square.state == 2:
                    if square.state == 1:
                        squareColor = activeColor
                    draw.rect(surf, squareColor, square.drawnRect)
                elif square.state == 2:
                    squareColor = (255, 0, 0)
                    square.drawX(surf, squareColor)

        for i, hintRow in enumerate(self.rowHints):  # place rowHint text on the screen
            offset = (squareSize / 2) + 10
            for j in reversed(hintRow):
                newText = hintFont.render(str(j), True, (0, 0, 0))
                newTextRect = newText.get_rect()
                newTextRect.center = self.grid[i][0].rect.center
                screen.blit(newText, (newTextRect[0] - offset, newTextRect[1]))
                offset += 16

        for i, hintColumn in enumerate(self.columnHints):  # place rowColumn text on the screen
            offset = (squareSize / 2) + 10
            for j in reversed(hintColumn):
                newText = hintFont.render(str(j), True, (0, 0, 0))
                newTextRect = newText.get_rect()
                newTextRect.center = self.grid[0][i].rect.center
                screen.blit(newText, (newTextRect[0], newTextRect[1] - offset))
                offset += 16


def main():
    puzzle = Puzzle(gridSize)
    #gameIcon = image.load(r"stuff\susface.png")
    #display.set_icon(gameIcon)
    dragging = False
    squareClickedIsActive = False
    mouseButton = 0
    clickedOnSquare = False

    # game loop
    running = True
    while running:
        #display.set_caption(f"\"Picross\" (el scary edition)          FPS: {clock.get_fps():.0f}")

        clickedOnSquare = False

        for e in event.get():
            if e.type == QUIT:
                running = False
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                for row in puzzle.grid:
                    for square in row:
                        if square.rect.collidepoint(e.pos):
                            squareClickedIsActive = square.state if square.state == 1 else 0
                            clickedOnSquare = True
                            break
                    if clickedOnSquare:
                        break
                dragging = True
                mouseButton = 1
            elif e.type == MOUSEBUTTONUP and e.button == 1:
                dragging = False
                mouseButton = 0
            elif e.type == MOUSEBUTTONDOWN and e.button == 3:
                for row in puzzle.grid:
                    for square in row:
                        if square.rect.collidepoint(e.pos):
                            squareClickedIsActive = square.state if square.state == 2 else 0
                            clickedOnSquare = True
                            break
                    if clickedOnSquare:
                        break
                dragging = True
                mouseButton = 3
            elif e.type == MOUSEBUTTONUP and e.button == 3:
                dragging = False
                mouseButton = 0

        screen.fill(backgroundColor)
        draw.rect(screen, (0, 0, 0), puzzle.background)
        puzzle.update(screen, dragging, squareClickedIsActive, mouseButton)

        display.update()

        clock.tick(fps)


main()
pygame.quit()
