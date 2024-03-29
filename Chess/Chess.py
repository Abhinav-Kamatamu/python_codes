import pygame
import sys
import copy

pygame.init()

clock = pygame.time.Clock()

height = 800
width = 800

sqaureSize = height/10
indent = 8

black = (48, 48, 48)
backGround = (255, 217, 179)
highlightColor = (219, 77, 64)
chessBoardColors = [(255, 191, 128),(128, 43, 0)]

blackPawn = pygame.image.load("blackPawn.png")
blackBishop = pygame.image.load("blackBishop.png")
blackKnight = pygame.image.load("blackKnight.png")
blackRook = pygame.image.load("blackRook.png")
blackQueen = pygame.image.load("blackQueen.png")
blackKing = pygame.image.load("blackKing.png")
whitePawn = pygame.image.load("whitePawn.png")
whiteBishop = pygame.image.load("whiteBishop.png")
whiteKnight = pygame.image.load("whiteKnight.png")
whiteRook = pygame.image.load("whiteRook.png")
whiteQueen = pygame.image.load("whiteQueen.png")
whiteKing = pygame.image.load("whiteKing.png")

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("funi ches game")

chessBoard = []
gameOver = False

class position():

    def __init__(self,x,y):

        self.x = x
        self.y = y

    def rect(self, width, height):

        return (self.x, self.y, width, height)

    def position(self):

        return (self.x, self.y)

class piece():

    class pawn():

        def __init__(self, isWhite, x, y):

            self.isWhite = isWhite
            self.hasMoven = False
            self.position = position(x, y)
            self.moves = []

            self.image = blackPawn
            if self.isWhite:
                self.image = whitePawn

        def calculateMoves(self, board):

            self.moves.clear()

            if self.isWhite:

                if not self.hasMoven:

                    if board[self.position.y - 2][self.position.x - 1] is None:
                        if board[self.position.y - 3][self.position.x - 1] is None:
                            self.moves.append(position(self.position.x, self.position.y - 2))
                            self.moves.append(position(self.position.x, self.position.y - 1))

                        if board[self.position.y - 3][self.position.x - 1] is not None:
                            self.moves.append(position(self.position.x, self.position.y - 1))

                else:

                    if board[self.position.y - 2][self.position.x - 1] is None:
                        self.moves.append(position(self.position.x, self.position.y - 1))

                if -1 < self.position.x - 2 < 8:
                    if board[self.position.y - 2][self.position.x - 2] is not None:
                        if board[self.position.y - 2][self.position.x - 2].isWhite is not self.isWhite:
                            self.moves.append(position(self.position.x - 1, self.position.y - 1))
                if -1 < self.position.x < 8:
                    if board[self.position.y - 2][self.position.x] is not None:
                        if board[self.position.y - 2][self.position.x].isWhite is not self.isWhite:
                            self.moves.append(position(self.position.x + 1, self.position.y - 1))    
                    
            if not self.isWhite:

                if not self.hasMoven:

                    if board[self.position.y][self.position.x - 1] is None:
                        if board[self.position.y + 1][self.position.x - 1] is None:
                            self.moves.append(position(self.position.x, self.position.y + 1))
                            self.moves.append(position(self.position.x, self.position.y + 2))

                        if board[self.position.y + 1][self.position.x - 1] is not None:
                            self.moves.append(position(self.position.x, self.position.y + 1))

                else:

                    if board[self.position.y][self.position.x - 1] is None:
                        self.moves.append(position(self.position.x, self.position.y + 1))

                if -1 < self.position.x - 2 < 8:
                    if board[self.position.y][self.position.x - 2] is not None:
                        if board[self.position.y][self.position.x - 2].isWhite is not self.isWhite:
                            self.moves.append(position(self.position.x - 1, self.position.y + 1))
                if -1 < self.position.x < 8:        
                    if board[self.position.y][self.position.x ] is not None:
                        if board[self.position.y][self.position.x].isWhite is not self.isWhite:
                            self.moves.append(position(self.position.x + 1, self.position.y + 1))
                    
    class knight():

        def __init__(self, isWhite, x, y):

            self.isWhite = isWhite
            self.hasMoven = False
            self.position = position(x, y)
            self.moves = []

            self.image = blackKnight
            if self.isWhite:
                self.image = whiteKnight

        def calculateMoves(self, board):

            self.moves.clear()

            if self.position.y > 2 and self.position.x < 8:
                self.moves.append(position(self.position.x + 1, self.position.y - 2))
            if self.position.y > 1 and self.position.x < 7:
                self.moves.append(position(self.position.x + 2, self.position.y - 1))
            if self.position.y < 8 and self.position.x < 7:
                self.moves.append(position(self.position.x + 2, self.position.y + 1))
            if self.position.y < 7 and self.position.x < 8:
                self.moves.append(position(self.position.x + 1, self.position.y + 2))
            if self.position.y < 7 and self.position.x > 1:
                self.moves.append(position(self.position.x - 1, self.position.y + 2))
            if self.position.y < 8 and self.position.x > 2:
                self.moves.append(position(self.position.x - 2, self.position.y + 1))
            if self.position.y > 1 and self.position.x > 2:
                self.moves.append(position(self.position.x - 2, self.position.y - 1))
            if self.position.y > 2 and self.position.x > 1:
                self.moves.append(position(self.position.x - 1, self.position.y - 2))

            i = 0
            while i < len(self.moves):

                if board[self.moves[i].y - 1][self.moves[i].x - 1] is not None:
                    if board[self.moves[i].y - 1][self.moves[i].x - 1].isWhite == self.isWhite:
                        self.moves.pop(i)
                        i = -1

                i += 1        
                
    class bishop():

        def __init__(self, isWhite, x, y):

            self.isWhite = isWhite
            self.hasMoven = False
            self.position = position(x, y)
            self.moves = []

            self.image = blackBishop
            if self.isWhite:
                self.image = whiteBishop
                
        def calculateMoves(self, board):

            self.moves.clear()

            i = 1
            while i + self.position.x < 9 and i + self.position.y < 9:                
                if board[self.position.y + i - 1][self.position.x + i - 1] is not None:
                    if board[self.position.y + i - 1][self.position.x + i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x + i, self.position.y + i))
                    break
                else:
                    self.moves.append(position(self.position.x + i, self.position.y + i))
                i += 1                    
            i = 1
            while self.position.x - i > 0 and i + self.position.y < 9:                
                if board[self.position.y + i - 1][self.position.x - i - 1] is not None:
                    if board[self.position.y + i - 1][self.position.x - i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x - i, self.position.y + i))
                    break
                else:
                    self.moves.append(position(self.position.x - i, self.position.y + i))
                i += 1    
            i = 1
            while i + self.position.x < 9 and self.position.y - i > 0:                
                if board[self.position.y - i - 1][self.position.x + i - 1] is not None:
                    if board[self.position.y - i - 1][self.position.x + i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x + i, self.position.y - i))
                    break
                else:
                    self.moves.append(position(self.position.x + i, self.position.y - i))
                i += 1    
            i = 1
            while self.position.x - i > 0 and self.position.y - i > 0:                
                if board[self.position.y - i - 1][self.position.x - i - 1] is not None:
                    if board[self.position.y - i - 1][self.position.x - i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x - i, self.position.y - i))
                    break
                else:
                    self.moves.append(position(self.position.x - i, self.position.y - i))
                i += 1    
                        

    class rook():

        def __init__(self, isWhite, x, y):

            self.isWhite = isWhite
            self.hasMoven = False
            self.position = position(x, y)
            self.moves = []

            self.image = blackRook
            if self.isWhite:
                self.image = whiteRook

        def calculateMoves(self, board):

            self.moves.clear()

            i = 1
            while self.position.x + i < 9:
                if board[self.position.y - 1][self.position.x + i - 1] is not None:
                    if board[self.position.y - 1][self.position.x + i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x + i, self.position.y))
                    break    
                else:
                    self.moves.append(position(self.position.x + i, self.position.y))
                i += 1
            i = 1    
            while self.position.x - i > 0:
                if board[self.position.y - 1][self.position.x - i -1] is not None:
                    if board[self.position.y - 1][self.position.x - i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x - i, self.position.y))
                    break    
                else:
                    self.moves.append(position(self.position.x - i,self.position.y))
                i += 1
            i = 1    
            while self.position.y + i < 9:
                if board[self.position.y + i - 1][self.position.x - 1] is not None:
                    if board[self.position.y + i - 1][self.position.x - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x, self.position.y + i))
                    break
                else:
                    self.moves.append(position(self.position.x, self.position.y + i))
                i += 1
            i = 1    
            while self.position.y - i > 0:
                if board[self.position.y - i - 1][self.position.x - 1] is not None:
                    if board[self.position.y - i - 1][self.position.x - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x, self.position.y - i))
                    break
                else:
                    self.moves.append(position(self.position.x, self.position.y - i))
                i += 1    

    class queen():

        def __init__(self, isWhite, x, y):

            self.isWhite = isWhite
            self.hasMoven = False
            self.position = position(x, y)
            self.moves = []

            self.image = blackQueen
            if self.isWhite:
                self.image = whiteQueen

        def calculateMoves(self, board):

            self.moves.clear()

            i = 1
            while i + self.position.x < 9 and i + self.position.y < 9:                
                if board[self.position.y + i - 1][self.position.x + i - 1] is not None:
                    if board[self.position.y + i - 1][self.position.x + i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x + i, self.position.y + i))
                    break
                else:
                    self.moves.append(position(self.position.x + i, self.position.y + i))
                i += 1                    
            i = 1
            while self.position.x - i > 0 and i + self.position.y < 9:                
                if board[self.position.y + i - 1][self.position.x - i - 1] is not None:
                    if board[self.position.y + i - 1][self.position.x - i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x - i, self.position.y + i))
                    break
                else:
                    self.moves.append(position(self.position.x - i, self.position.y + i))
                i += 1    
            i = 1
            while i + self.position.x < 9 and self.position.y - i > 0:                
                if board[self.position.y - i - 1][self.position.x + i - 1] is not None:
                    if board[self.position.y - i - 1][self.position.x + i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x + i, self.position.y - i))
                    break
                else:
                    self.moves.append(position(self.position.x + i, self.position.y - i))
                i += 1    
            i = 1
            while self.position.x - i > 0 and self.position.y - i > 0:                
                if board[self.position.y - i - 1][self.position.x - i - 1] is not None:
                    if board[self.position.y - i - 1][self.position.x - i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x - i, self.position.y - i))
                    break
                else:
                    self.moves.append(position(self.position.x - i, self.position.y - i))
                i += 1
            i = 1
            while self.position.x + i < 9:
                if board[self.position.y - 1][self.position.x + i - 1] is not None:
                    if board[self.position.y - 1][self.position.x + i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x + i, self.position.y))
                    break    
                else:
                    self.moves.append(position(self.position.x + i, self.position.y))
                i += 1
            i = 1    
            while self.position.x - i > 0:
                if board[self.position.y - 1][self.position.x - i -1] is not None:
                    if board[self.position.y - 1][self.position.x - i - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x - i, self.position.y))
                    break    
                else:
                    self.moves.append(position(self.position.x - i,self.position.y))
                i += 1
            i = 1    
            while self.position.y + i < 9:
                if board[self.position.y + i - 1][self.position.x - 1] is not None:
                    if board[self.position.y + i - 1][self.position.x - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x, self.position.y + i))
                    break
                else:
                    self.moves.append(position(self.position.x, self.position.y + i))
                i += 1
            i = 1    
            while self.position.y - i > 0:
                if board[self.position.y - i - 1][self.position.x - 1] is not None:
                    if board[self.position.y - i - 1][self.position.x - 1].isWhite is not self.isWhite:
                        self.moves.append(position(self.position.x, self.position.y - i))
                    break
                else:
                    self.moves.append(position(self.position.x, self.position.y - i))
                i += 1      

    class king():

         def __init__(self, isWhite, x, y):

            self.isWhite = isWhite
            self.hasMoven = False
            self.position = position(x, y)
            self.moves = []

            self.image = blackKing
            if self.isWhite:
                self.image = whiteKing

         def calculateMoves(self, board):

            self.moves.clear()    

            directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

            for direction in directions:
                if (0 < self.position.x + direction[0] < 9) and (0 < self.position.y + direction[1] < 9):
                    self.moves.append(position(self.position.x + direction[0], self.position.y + direction[1]))

            i = 0

            while i < len(self.moves):

                if board[self.moves[i].y - 1][self.moves[i].x - 1] is not None:
                    if board[self.moves[i].y - 1][self.moves[i].x - 1].isWhite is self.isWhite:
                        self.moves.pop(i)
                    else:
                        i += 1
                else:
                    i += 1

            if (not self.hasMoven):
                
                if (board[self.position.y - 1][5] is None) and (board[self.position.y - 1][6] is None):
                    if board[self.position.y - 1][7] is not None:
                        if (not board[self.position.y - 1][7].hasMoven):
                            self.moves.append(position(7, self.position.y))
                                              
                if (board[self.position.y - 1][3] is None) and (board[self.position.y - 1][2] is None) and (board[self.position.y - 1][1] is None):
                    if board[self.position.y - 1][0] is not None:
                        if not board[self.position.y - 1][0].hasMoven:
                            self.moves.append(position(3, self.position.y))    

blackKing = piece.king(False,5,1)
whiteKing = piece.king(True,5,8)

chessBoard = [ [ piece.rook(False,1,1), piece.knight(False,2,1), piece.bishop(False,3,1), piece.queen(False,4,1), blackKing, piece.bishop(False,6,1), piece.knight(False,7,1), piece.rook(False,8,1) ],           
               [ piece.pawn(False,1,2), piece.pawn(False,2,2), piece.pawn(False,3,2), piece.pawn(False,4,2), piece.pawn(False,5,2), piece.pawn(False,6,2), piece.pawn(False,7,2), piece.pawn(False,8,2) ],
               [ None             , None             , None             , None             , None             , None             , None             , None              ],
               [ None             , None             , None             , None             , None             , None             , None             , None              ],
               [ None             , None             , None             , None             , None             , None             , None             , None              ],
               [ None             , None             , None             , None             , None             , None             , None             , None              ],
               [ piece.pawn(True,1,7), piece.pawn(True,2,7), piece.pawn(True,3,7), piece.pawn(True,4,7), piece.pawn(True,5,7), piece.pawn(True,6,7), piece.pawn(True,7,7), piece.pawn(True,8,7) ],
               [ piece.rook(True,1,8), piece.knight(True,2,8), piece.bishop(True,3,8), piece.queen(True,4,8), whiteKing, piece.bishop(True,6,8), piece.knight(True,7,8), piece.rook(True,8,8) ] ]

highlights = [ [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ],
               [ False, False, False, False, False, False, False, False, ], ]

whiteTurn = True

highlighted = False

selectedPiece = None
                     
def DrawScreen():
        
    if not gameOver:
        pygame.display.set_caption("[WHITE]'s Turn")
        if not whiteTurn:
            pygame.display.set_caption("[BLACK]'s Turn")

    pygame.draw.rect(screen, backGround, (0, 0, width, height))
    pygame.draw.rect(screen, black, (sqaureSize - 5, sqaureSize - 5, width - 2*sqaureSize + 10, height - 2*sqaureSize + 10), border_radius = 3)

    numberOfSquaresDrawn = 0
    currentPosition = position(width/10,height/10)
    coordinate = position(1,1)

    while numberOfSquaresDrawn < 71:

        pygame.draw.rect(screen, chessBoardColors[numberOfSquaresDrawn%2], (currentPosition.rect(sqaureSize, sqaureSize)))

        if highlights[coordinate.y - 1][coordinate.x - 1] is not False:
            pygame.draw.rect(screen, highlightColor, (currentPosition.rect(sqaureSize, sqaureSize)))

        if chessBoard[coordinate.y - 1][coordinate.x - 1] is not None:
            screen.blit(chessBoard[coordinate.y - 1][coordinate.x - 1].image, (currentPosition.x + indent, currentPosition.y + indent))

        numberOfSquaresDrawn += 1
        currentPosition.x += sqaureSize
        coordinate.x += 1
        if currentPosition.x > 8*sqaureSize:
            numberOfSquaresDrawn += 1
            currentPosition.x = width/10
            currentPosition.y += sqaureSize
            coordinate.x = 1
            coordinate.y += 1

    numberOfLinesDrawn = 0
    currentPosition = position(width/10,height/5)

    while numberOfLinesDrawn < 7:

        pygame.draw.line(screen, black, currentPosition.position(), (currentPosition.x + width - (2 * sqaureSize), currentPosition.y), width=5)

        numberOfLinesDrawn += 1
        currentPosition.y += sqaureSize

    numberOfLinesDrawn = 0
    currentPosition = position(width/5,height/10)

    while numberOfLinesDrawn < 7:

        pygame.draw.line(screen, black, currentPosition.position(), (currentPosition.x, currentPosition.y + height - (2 * sqaureSize)), width=5)

        numberOfLinesDrawn += 1
        currentPosition.x += sqaureSize

    pygame.display.update()        

def checkSpecialRules(board):

    global whiteKing, blackKing

    i = 0
    while i < 8:
        if type(board[0][i]) == piece.pawn:
            board[0][i] = piece.queen(board[0][i].isWhite,board[0][i].position.x,board[0][i].position.y)
            break
        i += 1    
    i = 0
    while i < 8:
        if type(board[7][i]) == piece.pawn:
            board[7][i] = piece.queen(board[7][i].isWhite,board[7][i].position.x,board[7][i].position.y)
            break
        i += 1

    if (not whiteKing.hasMoven):        
        if type(board[7][4]) != piece.king:            
            if (whiteKing.position.x == 7) and (whiteKing.position.y == 8):
                board[7][5] = piece.rook(True,6,8)
                board[7][7] = None
            elif (whiteKing.position.x == 3) and (whiteKing.position.y == 8):
                board[7][3] = piece.rook(True,4,8)
                board[7][0] = None
            whiteKing.hasMoven = True

    if (not blackKing.hasMoven):        
        if type(board[0][4]) != piece.king:            
            if (blackKing.position.x == 7) and (blackKing.position.y == 1): 
                board[0][5] = piece.rook(False,6,1)
                board[0][7] = None
            elif (blackKing.position.x == 3) and (blackKing.position.y == 1):
                board[0][3] = piece.rook(False,4,1)
                board[0][0] = None
            blackKing.hasMoven = True                 

def cloneChessBoard(board):

    clone = [[None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],]
    
    i = 0

    while i < len(clone):

        j = 0

        while j < len(clone[i]):

            if board[i][j] is not None:

                if type(board[i][j]) == piece.pawn:
                    clone[i][j] = piece.pawn(board[i][j].isWhite, board[i][j].position.x, board[i][j].position.y)
                if type(board[i][j]) == piece.knight:
                    clone[i][j] = piece.knight(board[i][j].isWhite, board[i][j].position.x, board[i][j].position.y) 
                if type(board[i][j]) == piece.bishop:
                    clone[i][j] = piece.bishop(board[i][j].isWhite, board[i][j].position.x, board[i][j].position.y)
                if type(board[i][j]) == piece.rook:
                    clone[i][j] = piece.rook(board[i][j].isWhite, board[i][j].position.x, board[i][j].position.y)
                if type(board[i][j]) == piece.queen:
                    clone[i][j] = piece.queen(board[i][j].isWhite, board[i][j].position.x, board[i][j].position.y)
                if type(board[i][j]) == piece.king:
                    clone[i][j] = piece.king(board[i][j].isWhite, board[i][j].position.x, board[i][j].position.y)                    
                
            j += 1

        i += 1

    return clone   

        
def filterLegalMoves(block, board):

    i = 0

    while i < len(block.moves):

        illegal = False
        futureChessBoard1 = cloneChessBoard(board)
        
        futureChessBoard1[block.moves[i].y - 1][block.moves[i].x - 1] = block
        futureChessBoard1[block.position.y - 1][block.position.x - 1] = None

        for row in futureChessBoard1:

            for ingot in row:

                if ingot is not None:
                    if ingot.isWhite is not block.isWhite:

                        ingot.calculateMoves(futureChessBoard1)

                        for move in ingot.moves:
                        
                            futureChessBoard2 = cloneChessBoard(futureChessBoard1)

                            futureChessBoard2[move.y - 1][move.x - 1] = ingot
                            futureChessBoard2[ingot.position.y - 1][ingot.position.x - 1] = None

                            kingFound = False

                            for line in futureChessBoard2:

                                if kingFound:

                                    continue
                                
                                for cube in line:

                                    if cube is not None:

                                        if type(cube) == piece.king and cube.isWhite == whiteTurn:

                                            kingFound = True

                            if not kingFound:
                                illegal = True

        if illegal:                                
            block.moves.pop(i)
        else:
            i += 1


def numberOfLegalMoves(team, board):

    NOLegalMoves = 0

    for row in board:
        for block in row:

            if block is not None:
                if block.isWhite == team:

                    block.calculateMoves(board)
                    filterLegalMoves(block, board)

                    NOLegalMoves += len(block.moves)

    return NOLegalMoves

def inCheck(board):

    illegal = False

    for row in chessBoard:

            for ingot in row:

                if ingot is not None:
                    if ingot.isWhite is not whiteTurn:

                        ingot.calculateMoves(chessBoard)

                        for move in ingot.moves:
                        
                            futureChessBoard2 = cloneChessBoard(chessBoard)

                            futureChessBoard2[move.y - 1][move.x - 1] = ingot
                            futureChessBoard2[ingot.position.y - 1][ingot.position.x - 1] = None

                            kingFound = False

                            for line in futureChessBoard2:

                                if kingFound:

                                    continue
                                
                                for cube in line:

                                    if cube is not None:

                                        if type(cube) == piece.king and cube.isWhite == whiteTurn:

                                            kingFound = True

                            if not kingFound:
                                illegal = True

    if illegal:
        return True
    else:
        return False

DrawScreen()

while not gameOver:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            
            mousePosition = pygame.mouse.get_pos()
            coordinate = position(int(mousePosition[0]//sqaureSize), int(mousePosition[1]//sqaureSize))

            if (highlighted) and (selectedPiece is not None):

                if (0 < coordinate.x < 9) and (0 < coordinate.y < 9):  

                    if highlights[coordinate.y - 1][coordinate.x - 1]:

                        chessBoard[coordinate.y - 1][coordinate.x - 1] = selectedPiece  
                        chessBoard[selectedPiece.position.y - 1][selectedPiece.position.x - 1] = None
                        selectedPiece.position = position(coordinate.x,coordinate.y)

                        if type(selectedPiece) != piece.king:
                            selectedPiece.hasMoven = True
                            
                        whiteTurn = not whiteTurn
                        highlighted = False
                        selectedPiece = None

            highlights = [ [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ],
                           [ False, False, False, False, False, False, False, False, ], ]

            if  (9 > coordinate.x > 0) and (9 > coordinate.y > 0):
                
                if chessBoard[coordinate.y - 1][coordinate.x - 1] is not None and chessBoard[coordinate.y - 1][coordinate.x - 1].isWhite == whiteTurn:

                    selectedPiece = chessBoard[coordinate.y - 1][coordinate.x - 1]
                    selectedPiece.calculateMoves(chessBoard)
                    filterLegalMoves(selectedPiece, chessBoard)

                    for move in selectedPiece.moves:

                        highlights[move.y - 1][move.x - 1] = True
                    
                    highlighted = True

                if chessBoard[coordinate.y - 1][coordinate.x - 1] is None:

                    selectedPiece = None
                    highlighted = False

            else:

                selectedPiece = None
                highlighted = False       

            checkSpecialRules(chessBoard)

            if numberOfLegalMoves(whiteTurn, chessBoard) == 0:

                if inCheck(chessBoard):

                    if whiteTurn:

                        pygame.display.set_caption("[BLACK] wins by checkmate")

                    else:

                        pygame.display.set_caption("[WHITE] wins by checkmate")

                else:

                    pygame.display.set_caption("1/2 - stalemate")
                    
                gameOver = True

            DrawScreen()    
