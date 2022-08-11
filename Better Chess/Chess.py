import pygame
import sys
import copy

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

turnCaption = {

    True : "WHITE",
    False : "BLACK"

    }

castlingDictionary = {

    (6,7): ((5,7),(7,7)),
    (2,7): ((3,7),(0,7)),

    (6,0): ((5,0),(7,0)),
    (2,0): ((3,0),(0,0))

    }

width = 1000
height = 1000
indent = 72

highlightColors = {

                0 : (255, 255, 0),
                1 : (225, 225, 0)

                }

selectedPiece = None
selectedPiece_position = (-1, -1)
currentLegalMoves = []

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("white's turn")

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

    "en'pessant" : [] ,

    "castling" : [ [True, True],
                   [True, True] ],

    "turn" : True,

    "gameOver": False
     
    }

highlights = []




def checkTeam(piece):

    if piece.upper() != piece:

        return False
    
    return True


def checkControlledSquares(position, team):

    controlledSquares = []
    clone = {}

    #making clone without king--
    breaked = False
    i = 0
    while i < len(position["board"]):

        j = 0

        while j < len(position["board"][i]):

            piece = position["board"][i][j]

            if piece != "-":

                if piece.upper() == "K" and checkTeam(piece) is not team:

                    clone = copy.deepcopy(position)
                    clone["board"][i][j] = "-"

                    breaked = True
                    break

            j += 1

        if breaked:
            break
        i += 1

    #checking controlled squares--
    i = 0
    while i < len(clone["board"]):

        j = 0
        while j < len(clone["board"][i]):

            piece = clone["board"][i][j]

            if piece != "-":

                if checkTeam(piece) is team:

                    moves = calculateMoves(clone, piece, j, i, True)

                    for move in moves:

                        if not (move in controlledSquares): 

                            controlledSquares.append(move)

            j += 1

        i += 1    
            
    return controlledSquares


def calculateSlidingPieces(currentPosition, team, x, y, directions, control):

    moves = []

    for direction in directions:

            i = 1

            while True:

                if not ((-1 < x + (direction[0] * i) < 8) and (-1 < y + (direction[1] * i) < 8)):

                    break

                if currentPosition["board"][y + (direction[1] * i)][x + (direction[0] * i)] != "-":

                    targetTeam = checkTeam(currentPosition["board"][y + (direction[1] * i)][x + (direction[0] * i)])

                    if targetTeam is not team or control:

                        moves.append((x + (direction[0] * i), y + (direction[1] * i)))

                    break

                moves.append((x + (direction[0] * i), y + (direction[1] * i)))
                i += 1

    return moves




def caclulateStaticPieces(currentPosition, team, x, y, directions, control):

    moves = []

    for direction in directions:

            if (-1 < x + direction[0] < 8) and (-1 < y + direction[1] < 8):

                if currentPosition["board"][y + direction[1]][x + direction[0]] != "-":

                    if checkTeam(currentPosition["board"][y + direction[1]][x + direction[0]]) is team and (not control):

                        continue

                moves.append((x + direction[0], y + direction[1]))

    return moves




def calculateMoves(currentPosition, piece, x, y, control):

    moves = []
    team = checkTeam(piece)

    #pawn--
    if piece.upper() == "P":

        i = -1

        if not team:

            i = 1

        #regularMovement
        if currentPosition["board"][y + i][x] == "-" and not control:

            moves.append((x, y + i))
                
            if y == int(3.5 + (-i * 2.5)) and currentPosition["board"][y + (2 * i)][x] == "-":

                moves.append((x, y + (2 * i)))

        #capturingMovement
        directions = [(-1, i), (1, i)]

        for direction in directions:

            if not (-1 < x + direction[0] < 8):

                continue

            targetSquare = currentPosition["board"][y + direction[1]][x + direction[0]]
        
            if targetSquare != "-" or control:

                targetTeam = checkTeam(targetSquare)

                if targetTeam is not team or control:

                    moves.append((x + direction[0], y + direction[1]))

            #en'pessant
            if (x + direction[0], y + direction[1]) in currentPosition["en'pessant"]:

                if (team and (y + direction[1]) == 2) or (not team and (y + direction[1]) == 5):

                    moves.append((x + direction[0], y + direction[1]))     


    #knight--
    if piece.upper() == "N":

        #knight l shapes
        directions = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]
        moves = caclulateStaticPieces(currentPosition, team, x, y, directions, control)
                

    #queen--
    if piece.upper() == "Q":

        #queen directions
        directions = [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (-1,0), (0,-1), (0,1)]
        moves = calculateSlidingPieces(currentPosition, team, x, y, directions, control)


    #bishop--
    if piece.upper() == "B":

        #bishop directions
        directions = [(1,1), (-1,1), (1,-1), (-1,-1)]
        moves = calculateSlidingPieces(currentPosition, team, x, y, directions, control)


    #rook--
    if piece.upper() == "R":

        # directions
        directions = [(1,0), (-1,0), (0,-1), (0,1)]
        moves = calculateSlidingPieces(currentPosition, team, x, y, directions, control)
                

    #king--
    if piece.upper() == "K":

        #king directions
        directions = [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (-1,0), (0,-1), (0,1)]
        moves = caclulateStaticPieces(currentPosition, team, x, y, directions, control)

        #castling
        dict_ = {False: 0, True: 1}

        if not control:

            controlledSquares = checkControlledSquares(currentPosition, not currentPosition["turn"])

            if currentPosition["castling"][dict_[team]][1]:

                if (currentPosition["board"][dict_[team] * 7][5] == "-") and (currentPosition["board"][dict_[team] * 7][6] == "-") and not ((5, dict_[team] * 7) in controlledSquares):
                    moves.append((6, dict_[team] * 7))

            if currentPosition["castling"][dict_[team]][0]:

                if (currentPosition["board"][dict_[team] * 7][3] == "-") and (currentPosition["board"][dict_[team] * 7][2] == "-") and (currentPosition["board"][dict_[team] * 7][1] == "-") and not ((3, dict_[team] * 7) in controlledSquares) and not ((1, dict_[team] * 7) in controlledSquares):
                    moves.append((2, dict_[team] * 7))     

            
                        
    return moves


def checkNumberOfLegalMoves(position, team):

    numberOfLegalMoves = 0

    i = 0
    while i < len(position["board"]):
        j = 0
        while j < len(position["board"][i]):

            piece = position["board"][i][j]

            if piece != "-":

                if checkTeam(piece) is team:

                    moves = calculateMoves(position, piece, j, i, False)
                    filterLegalMoves(position, moves, (j, i))

                    numberOfLegalMoves += len(moves)

            j += 1

        i += 1

    return numberOfLegalMoves

def inCheck(position, team):

    check = False

    controlledSquares = checkControlledSquares(position, not team)

    i = 0
    while i < len(position["board"]):
        j = 0
        while j < len(position["board"][i]):

            piece = position["board"][i][j]

            if piece.upper() == "K" and checkTeam(piece) == team:

                if (j, i) in controlledSquares:

                    check = True
                    
                break
    
            j += 1

        if check:
            break
        i += 1

    return check     

def filterLegalMoves(position, moves, startingSquare): 

    k = 0

    while k < len(moves):

        move = moves[k]

        illegal = False
        clone = copy.deepcopy(position)

        playMove(clone, startingSquare, move, False)

        controlledSquares = checkControlledSquares(clone, not position["turn"])

        i = 0
        while i < len(clone["board"]):
            j = 0
            while j < len(clone["board"][i]):

                piece = clone["board"][i][j]

                if piece != "-":

                    team = checkTeam(piece)

                    if piece.upper() == "K" and team is position["turn"]:

                        if (j, i) in controlledSquares:
                        
                            illegal = True
                            break

                j += 1
                
            if illegal:
                break
            
            i += 1

        if illegal:
            moves.remove(move)
            continue

        k += 1

def drawScreen(update):

    screen.blit(images["chessBoard"], (0, 0))

    y = 0
    
    while y < 8:
        
        x = 0
            
        while x < 8:

            piece = position["board"][y][x]

            if (x, y) in highlights:

                pygame.draw.rect(screen, highlightColors[(x + y)%2], (x * 125, y * 125, 125, 125))

            #only for testing moves lmao
            #if (x, y) in currentLegalMoves:
                #pygame.draw.rect(screen, highlightColors[(x + y)%2], (x * 125, y * 125, 125, 125))

            if piece != "-":

                if selectedPiece_position != (x, y):
                    
                    screen.blit(images[piece], (x * 125, y * 125))
            
            x += 1
            
        y += 1

    if update:
        pygame.display.update()

drawScreen(True)




def enPessant(position, startingSquare, targetSquare, team):

    capture = False

    if position["board"][startingSquare[1]][startingSquare[0]].upper() == "P":

        if targetSquare in position["en'pessant"]:

            if team and targetSquare[1] == 2:
                position["board"][targetSquare[1] + 1][targetSquare[0]] = "-"
                capture = True

            elif not team and targetSquare[1] == 5:
                position["board"][targetSquare[1] - 1][targetSquare[0]] = "-"
                capture = True

    position["en'pessant"].clear()
        
    if position["board"][startingSquare[1]][startingSquare[0]].upper() == "P":

        if abs(targetSquare[1] - startingSquare[1]) == 2:
          
            if team:

                position["en'pessant"].append((targetSquare[0], targetSquare[1] + 1))

            else:

                position["en'pessant"].append((targetSquare[0], targetSquare[1] - 1))

    return capture




def promotePawn(position, startingSquare, targetSquare, team, capture_):

    capture = capture_

    if position["board"][targetSquare[1]][targetSquare[0]].upper() == "P":

        if (targetSquare[1] == 7) or (targetSquare[1] == 0):

            capture = True

            if team:

                position["board"][targetSquare[1]][targetSquare[0]] = "Q"

            else:

                position["board"][targetSquare[1]][targetSquare[0]] = "q"

    return capture


def castling(position, startingSquare, targetSquare, team, capture_):

    capture = capture_

    if position["board"][startingSquare[1]][startingSquare[0]].upper() == "K":

        i = 0
        if team:
            i = 1

        position["castling"][i][0] = False
        position["castling"][i][1] = False

        if abs(startingSquare[0] - targetSquare[0]) == 2:

            rook_ = position["board"][castlingDictionary[targetSquare][1][1]][castlingDictionary[targetSquare][1][0]]

            position["board"][castlingDictionary[targetSquare][0][1]][castlingDictionary[targetSquare][0][0]] = rook_
            position["board"][castlingDictionary[targetSquare][1][1]][castlingDictionary[targetSquare][1][0]] = "-"

            capture = True

    elif position["board"][startingSquare[1]][startingSquare[0]].upper() == "R":

        startingPositions = [(0,0), (0,7), (7,0), (7,7)]

        if startingSquare in startingPositions:

            position["castling"][startingSquare[1]//7][startingSquare[0]//7] = False

    return capture         
                    

def playMove(position, startingSquare, targetSquare, main):

    global highlights

    capture = False
    team = checkTeam(position["board"][startingSquare[1]][startingSquare[0]])

    capture = enPessant(position, startingSquare, targetSquare, team)
    capture = castling(position, startingSquare, targetSquare, team, capture)

    if position["board"][targetSquare[1]][targetSquare[0]] != "-":
        capture = True

    position["board"][targetSquare[1]][targetSquare[0]] = position["board"][startingSquare[1]][startingSquare[0]]
    position["board"][startingSquare[1]][startingSquare[0]] = "-"

    capture = promotePawn(position, startingSquare, targetSquare, team, capture)

    if main:
        
        highlights = [startingSquare, targetSquare]

        position["turn"] = not position["turn"]
        pygame.display.set_caption(turnCaption[position["turn"]] + "'s turn")

    return capture


def endGame():

    global position
    
    if checkNumberOfLegalMoves(position, position["turn"]) == 0:

        if inCheck(position, position["turn"]):

            pygame.display.set_caption(turnCaption[not position["turn"]] + " wins by Checkmate")

        else:

            pygame.display.set_caption("Stalemate ;-;")


        position["gameOver"] = True    

            
#main loop--
while not position["gameOver"]:

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

            if currentPiece != "-" and checkTeam(currentPiece) == position["turn"]:

                selectedPiece = currentPiece
                selectedPiece_position = coordinate

                currentLegalMoves = calculateMoves(position, selectedPiece, coordinate[0], coordinate[1], False)
                filterLegalMoves(position, currentLegalMoves, (coordinate[0], coordinate[1]))

        if event.type == pygame.MOUSEBUTTONUP:

            mousePosition = pygame.mouse.get_pos()
            coordinate = (max(min(mousePosition[0]//125, 8), -1), max(min(mousePosition[1]//125, 8), -1))

            if coordinate in currentLegalMoves and selectedPiece is not None:
                
                sound = playMove(position, selectedPiece_position, coordinate, True)

                audio[sound].play()

                endGame()

            selectedPiece = None
            selectedPiece_position = (-1, -1)
            currentLegalMoves.clear()

            drawScreen(True)

            
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()
