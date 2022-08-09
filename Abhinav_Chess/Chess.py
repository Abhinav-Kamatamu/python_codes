import pygame
from pygame.locals import *

pygame.init()
# ---------Important Variables --------
width = 800
height = 800
chesswidth = 600
chessheight = 600
piecesize = 75
boardStartPoint = (100, 100)
PAWN = 'PAWN'
ROOK = 'ROOK'
KNIGHT = 'KNIGHT'
BISHOP = 'BISHOP'
QUEEN = 'QUEEN'
KING = 'KING'
BLACK = 'BLACK'
WHITE = 'WHITE'
# ----------- Image Importing ---------
chessboard = pygame.image.load('Board.png')
wp = pygame.image.load('wp.png')
wr = pygame.image.load('wr.png')
wn = pygame.image.load('wn.png')
wb = pygame.image.load('wb.png')
wk = pygame.image.load('wk.png')
wq = pygame.image.load('wq.png')
bp = pygame.image.load('bp.png')
br = pygame.image.load('br.png')
bn = pygame.image.load('bn.png')
bb = pygame.image.load('bb.png')
bk = pygame.image.load('bk.png')
bq = pygame.image.load('bq.png')
selected = pygame.image.load('Selected.png')

chessboard = pygame.transform.scale(chessboard, (chesswidth, chessheight))
wp = pygame.transform.scale(wp, (piecesize, piecesize))
wr = pygame.transform.scale(wr, (piecesize, piecesize))
wn = pygame.transform.scale(wn, (piecesize, piecesize))
wb = pygame.transform.scale(wb, (piecesize, piecesize))
wk = pygame.transform.scale(wk, (piecesize, piecesize))
wq = pygame.transform.scale(wq, (piecesize, piecesize))
bp = pygame.transform.scale(bp, (piecesize, piecesize))
br = pygame.transform.scale(br, (piecesize, piecesize))
bn = pygame.transform.scale(bn, (piecesize, piecesize))
bb = pygame.transform.scale(bb, (piecesize, piecesize))
bk = pygame.transform.scale(bk, (piecesize, piecesize))
bq = pygame.transform.scale(bq, (piecesize, piecesize))
selected = pygame.transform.scale(selected, (piecesize, piecesize))


# -------------- Classes----------------

class Piece:
    def __init__(self):
        pass

    class Pawn:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = PAWN

    class Rook:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = ROOK

    class Knight:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = KNIGHT

    class Bishop:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = BISHOP

    class Queen:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = QUEEN

    class King:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = KING

        def check_castle(self):
            return True


class Board:
    def __init__(self, boardwidth, boardheight):
        self.width = boardwidth
        self.height = boardheight
        self.grid = [
            [Piece.Rook(BLACK, 1, 1), Piece.Knight(BLACK, 2, 1), Piece.Bishop(BLACK, 3, 1),
             Piece.Queen(BLACK, 4, 1), Piece.King(BLACK, 5, 1), Piece.Bishop(BLACK, 6, 1),
             Piece.Knight(BLACK, 7, 1), Piece.Rook(BLACK, 8, 1)],
            [Piece.Pawn(BLACK, 1, 2), Piece.Pawn(BLACK, 2, 2), Piece.Pawn(BLACK, 3, 2), Piece.Pawn(BLACK, 4, 2),
             Piece.Pawn(BLACK, 5, 2), Piece.Pawn(BLACK, 6, 2), Piece.Pawn(BLACK, 7, 2), Piece.Pawn(BLACK, 8, 2)],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [Piece.Pawn(WHITE, 1, 7), Piece.Pawn(WHITE, 2, 7), Piece.Pawn(WHITE, 3, 7),
             Piece.Pawn(WHITE, 4, 7), Piece.Pawn(WHITE, 5, 7), Piece.Pawn(WHITE, 6, 7),
             Piece.Pawn(WHITE, 7, 7), Piece.Pawn(WHITE, 8, 7)],
            [Piece.Rook(WHITE, 1, 8), Piece.Knight(WHITE, 2, 8), Piece.Bishop(WHITE, 3, 8), Piece.Queen(WHITE, 4, 8),
             Piece.King(WHITE, 5, 8), Piece.Bishop(WHITE, 6, 8), Piece.Knight(WHITE, 7, 8), Piece.Rook(WHITE, 8, 8)]

        ]
        self.blackDict = {
            PAWN: bp,
            ROOK: br,
            KNIGHT: bn,
            BISHOP: bb,
            QUEEN: bq,
            KING: bk
        }
        self.whiteDict = {
            PAWN: wp,
            ROOK: wr,
            KNIGHT: wn,
            BISHOP: wb,
            QUEEN: wq,
            KING: wk
        }
        self.win = None
        self.turn = WHITE
        self.clicx = 0
        self.clicky = 0
        self.show_possibility = False

    def startup(self):
        self.win = pygame.display.set_mode((self.width, self.height))
        self.win.blit(chessboard, boardStartPoint)
        pygame.display.update()
        pygame.display.set_caption("CHESS")


    def render_direction_white(self):
        self.win.blit(chessboard, boardStartPoint)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.grid[i][j] != 0:
                    if self.grid[i][j].colour == WHITE:
                        self.win.blit(self.whiteDict[self.grid[i][j].piece_type], (
                            (self.grid[i][j].position[0] - 1) * piecesize + boardStartPoint[0],
                            (self.grid[i][j].position[1] - 1) * piecesize + boardStartPoint[1]))
                    if self.grid[i][j].colour == BLACK:
                        self.win.blit(self.blackDict[self.grid[i][j].piece_type], (
                            (self.grid[i][j].position[0] - 1) * piecesize + boardStartPoint[0],
                            (self.grid[i][j].position[1] - 1) * piecesize + boardStartPoint[1]))
        pygame.display.update()

    def detect_click(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                return event.pos
        return [-1,-1]

    def potential_moves(self, x, y, piece_type, colour):
        possible_moves = []
        if piece_type == PAWN:
            if colour == WHITE:
                possible_moves = [(x - 1, y - 2), (x - 1, y - 3), (x, y - 2), (x - 2, y - 2)]
                if y != 7:
                    possible_moves.remove(possible_moves[1])
                for i in possible_moves:
                    if i[1] < 0:
                        possible_moves.remove(i)
                    if i[0] < 0:
                        possible_moves.remove(i)
                    if i[0] > 7:
                        possible_moves.remove(i)
                for i in possible_moves:
                    if self.grid[i[1]][i[0]] != 0:
                        if self.grid[i[1]][i[0]].colour == WHITE:
                            possible_moves.remove(i)
            if colour == BLACK:
                possible_moves = [(x - 1, y), (x - 1, y + 1), (x, y), (x - 2, y)]
                if y != 2:
                    possible_moves.remove(possible_moves[1])
                for i in possible_moves:
                    if i[1] > 7:
                        possible_moves.remove(i)
                    if i[0] < 0:
                        possible_moves.remove(i)
                    if i[0] > 7:
                        possible_moves.remove(i)
                for i in possible_moves:
                    if self.grid[i[1]][i[0]] != 0:
                        if self.grid[i[1]][i[0]].colour == BLACK:
                            possible_moves.remove(i)
        if piece_type == BISHOP:
            possible_moves = []
            for j in range(0, 4):
                for i in range(1, 9):
                    if j == 0:
                        direction_coordinate = (x - 1 - i, y - 1 - i)
                    elif j == 1:
                        direction_coordinate = (x - 1 + i, y - 1 + i)
                    elif j == 2:
                        direction_coordinate = (x - 1 - i, y - 1 + i)
                    else:
                        direction_coordinate = (x - 1 + i, y - 1 - i)
                    if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                        break
                    elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                        break
                    elif self.grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                        if self.grid[direction_coordinate[1]][direction_coordinate[0]].colour == colour:
                            break
                        else:
                            possible_moves.append(direction_coordinate)
                            break
                    else:
                        possible_moves.append(direction_coordinate)
        if piece_type == ROOK:
            possible_moves = []
            for j in range(0, 4):
                for i in range(1, 9):
                    if j == 0:
                        direction_coordinate = (x - 1 - i, y - 1)
                    elif j == 1:
                        direction_coordinate = (x - 1 + i, y - 1)
                    elif j == 2:
                        direction_coordinate = (x - 1, y - 1 + i)
                    else:
                        direction_coordinate = (x - 1, y - 1 - i)
                    if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                        break
                    elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                        break
                    elif self.grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                        if self.grid[direction_coordinate[1]][direction_coordinate[0]].colour == colour:
                            break
                        else:
                            possible_moves.append(direction_coordinate)
                            break
                    else:
                        possible_moves.append(direction_coordinate)
        if piece_type == QUEEN:
            possible_moves = []
            for j in range(0, 8):
                for i in range(1, 9):
                    if j == 0:
                        direction_coordinate = (x - 1 - i, y - 1)
                    elif j == 1:
                        direction_coordinate = (x - 1 + i, y - 1)
                    elif j == 2:
                        direction_coordinate = (x - 1, y - 1 + i)
                    elif j == 3:
                        direction_coordinate = (x - 1, y - 1 - i)
                    elif j == 4:
                        direction_coordinate = (x - 1 - i, y - 1)
                    elif j == 5:
                        direction_coordinate = (x - 1 + i, y - 1)
                    elif j == 6:
                        direction_coordinate = (x - 1, y - 1 + i)
                    else:
                        direction_coordinate = (x - 1, y - 1 - i)
                    if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                        break
                    elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                        break
                    elif self.grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                        if self.grid[direction_coordinate[1]][direction_coordinate[0]].colour == colour:
                            break
                        else:
                            possible_moves.append(direction_coordinate)
                            break
                    else:
                        possible_moves.append(direction_coordinate)
        if piece_type == KNIGHT:
            pass
        if piece_type == KING:
            possible_moves = [(x + 1, y - 1), (x + 3, y - 1), (x - 2, y - 2), (x - 1, y - 2), (x, y - 2),
                              (x + 2, y - 1), (x - 2, y), (x, y - 1), (x, y), (x - 1, y)]
            if not self.grid[y - 1][x - 1].check_castle():
                possible_moves.remove(possible_moves[0])
                possible_moves.remove(possible_moves[1])
            for i in possible_moves:
                if ((i[0] > 7) or (i[0] < 0)) or ((i[1] > 7) or (i[1] < 0)):
                    possible_moves.remove(i)
                if self.grid[i[1]][i[0]] != 0:
                    if self.grid[i[1]][i[0]].colour == colour:
                        possible_moves.remove(i)
        return possible_moves

    def get_pressed_block(self):
        click_detected = self.detect_click()
        x = click_detected[0]
        y = click_detected[1]
        if (x, y) != (-1,-1):
            x = ((x - 100) // piecesize) + 1
            y = ((y - 100) // piecesize) + 1
            if ((x > 7) or (x < 0)) or ((y > 7) or (y < 0)):
                clickedblock = [-1, -1]
                return clickedblock
            else:
                clickedblock = [x, y]
                return clickedblock
        else:
            return [-1, -1]

    def show_peice_possibility(self, board_start_point):

    def king_possibilies(self, position, colour):  # this is to check which square the king is safe
        if (self.grid[position[1] - 1][position[0] + 1].piece_type == PAWN) or (
                self.grid[position[1] - 1][position[0] - 1].piece_type == PAWN):
            if (self.grid[position[1] - 1][position[0] + 1].colour != colour) or (
                    self.grid[position[1] - 1][position[0] - 1].colour != colour):
                return False
        (x, y) = position
        threats = []
        for j in range(0, 4):
            for i in range(1, 9):
                if j == 0:
                    direction_coordinate = (x - i, y - i)
                elif j == 1:
                    direction_coordinate = (x + i, y + i)
                elif j == 2:
                    direction_coordinate = (x - i, y + i)
                else:
                    direction_coordinate = (x + i, y - i)
                if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                    break
                elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                    break
                elif self.grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                    if self.grid[direction_coordinate[1]][direction_coordinate[0]].colour != colour:
                        if (self.grid[direction_coordinate[1]][direction_coordinate[0]].piece_type == BISHOP) or (
                                self.grid[direction_coordinate[1]][direction_coordinate[0]].piece_type == QUEEN):
                            threats.append(direction_coordinate)
                    else:
                        break
                else:
                    pass
        for j in range(0, 4):
            for i in range(1, 9):
                if j == 0:
                    direction_coordinate = (x - i, y)
                elif j == 1:
                    direction_coordinate = (x + i, y)
                elif j == 2:
                    direction_coordinate = (x, y + i)
                else:
                    direction_coordinate = (x, y - i)
                if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                    break
                elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                    break
                elif self.grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                    if self.grid[direction_coordinate[1]][direction_coordinate[0]].colour != colour:
                        if (self.grid[direction_coordinate[1]][direction_coordinate[0]].piece_type == ROOK) or (
                                self.grid[direction_coordinate[1]][direction_coordinate[0]].piece_type == QUEEN):
                            threats.append(direction_coordinate)
                    else:
                        break
                else:
                    pass


board = Board(width, height)
board.startup()
board.render_direction_white()
while True:
    board.show_peice_possibility(boardStartPoint)

