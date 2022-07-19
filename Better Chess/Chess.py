import pygame
import sys

pygame.init()

images = {

    "p" : pygame.image.load("blackPawn.png"),
    "n" : pygame.image.load("blackKnight.png"),
    "b" : pygame.image.load("blackBishop.png"),
    "r" : pygame.image.load("blackRook.png"),
    "q" : pygame.image.load("blackQueen.png"),
    "k" : pygame.image.load("blackKing.png"),

    "P" : pygame.image.load("whitePawn.png"),
    "N" : pygame.image.load("whiteKnight.png"),
    "B" : pygame.image.load("whiteBishop.png"),
    "R" : pygame.image.load("whiteRook.png"),
    "Q" : pygame.image.load("whiteQueen.png"),
    "K" : pygame.image.load("whiteKing.png"),

    "chessBoard" : pygame.transform.scale(pygame.image.load("chessBoard.png"), (1000, 1000))
    
    }

audio = {

        True : pygame.mixer.Sound("captureSound.mp3"),
        False : pygame.mixer.Sound("moveSound.mp3")

    }

width = 1000
height = 1000
indent = 72

highlightColors = {

                0 : (255, 255, 0),
                1 : (225, 225, 0)

                }

gameOver = False

selectedPiece = None
selectedPiece_position = (-1, -1)

screen = pygame.display.set_mode((width, height))

position = {

    "board" : [
        
                  ["r", "n", "b", "q", "k", "b", "n", "r"],
                  ["p", "p", "p", "p", "p", "p", "p", "p"],
                  ["-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-"],
                  ["-", "-", "-", "-", "-", "-", "-", "-"],
                  ["P", "P", "P", "P", "P", "P", "P", "P"],
                  ["R", "N", "B", "Q", "K", "B", "N", "R"]

              ],

    "en'pessant" : [ [False, False, False, False, False, False, False, False],
                     [False, False, False, False, False, False, False, False] ],

    "castling" : [ [True, True],
                   [True, True] ]
    
    }

highlights = [] 

def drawScreen(update):

    screen.blit(images["chessBoard"], (0, 0))

    y = 0
    
    while y < 8:
        
        x = 0
            
        while x < 8:

            piece = position["board"][y][x]

            if (x, y) in highlights:

                pygame.draw.rect(screen, highlightColors[(x + y)%2], (x * 125, y * 125, 125, 125))

            if piece != "-":

                if selectedPiece_position != (x, y):
                    
                    screen.blit(images[piece], (x * 125, y * 125))
            
            x += 1
            
        y += 1

    if update:
        pygame.display.update()

drawScreen(True)

def playMove(position, startingSquare, targetSquare, special):

    global highlights

    capture = False

    if position["board"][targetSquare[1]][targetSquare[0]] != "-":
        capture = True

    position["board"][targetSquare[1]][targetSquare[0]] = position["board"][startingSquare[1]][startingSquare[0]]
    position["board"][startingSquare[1]][startingSquare[0]] = "-"

    highlights = [startingSquare, targetSquare]

    return capture

while not gameOver:

    if selectedPiece is not None:

        mousePosition = pygame.mouse.get_pos()        

        drawScreen(False)

        screen.blit(images[selectedPiece], (mousePosition[0] - indent, mousePosition[1] - indent))
        pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mousePosition = pygame.mouse.get_pos()
            coordinate = (max(min(mousePosition[0]//125, 8), -1), max(min(mousePosition[1]//125, 8), -1))
            
            currentPiece = position["board"][coordinate[1]][coordinate[0]]

            if currentPiece != "-":

                selectedPiece = currentPiece
                selectedPiece_position = coordinate

        if event.type == pygame.MOUSEBUTTONUP:

            mousePosition = pygame.mouse.get_pos()
            coordinate = (max(min(mousePosition[0]//125, 8), -1), max(min(mousePosition[1]//125, 8), -1))

            if coordinate != selectedPiece_position and selectedPiece is not None:
                
                sound = playMove(position, selectedPiece_position, coordinate, False)

                audio[sound].play()

            selectedPiece = None
            selectedPiece_position = (-1, -1)

            drawScreen(True)

            




















