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


class Piece:
    def __init__(self):
        pass

    class Pawn:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = PAWN

        def get_possibility(self, grid):
            (x, y) = self.position
            possibility_dict = {
                BLACK: [(x, y + 1), (x, y + 2), (x - 1, y + 1), (x + 1, y + 1)],
                WHITE: [(x, y - 1), (x, y - 2), (x - 1, y - 1), (x + 1, y - 1)]
            }
            if self.colour == BLACK:
                if y != 2:
                    if grid[y + 1][x] != 0:
                        possibility_dict[self.colour].remove(possibility_dict[self.colour][1])
                        possibility_dict[self.colour].remove(possibility_dict[self.colour][2])
            if self.colour == WHITE:
                if y != 7:
                    if grid[y - 1][x] != 0:
                        possibility_dict[self.colour].remove(possibility_dict[self.colour][1])
                        possibility_dict[self.colour].remove(possibility_dict[self.colour][2])
            for i in possibility_dict[self.colour]:
                if (i[0] < 0 or i[0] > 7) or (i[1] < 0 or i[1] > 7):
                    possibility_dict[self.colour].remove(i)
            for i in possibility_dict[self.colour]:
                if i == (x - 1, y + 1) or (x + 1, y + 1) or (x - 1, y - 1) or (x + 1, y - 1):
                    if grid[i[1]][i[0]] == 0:
                        possibility_dict[self.colour].remove(i)
                        break
                    if grid[i[1]][i[0]].colour == self.colour:
                        possibility_dict[self.colour].remove(i)

            give_grid(grid)
            for i in range(0, 8):
                for j in range(0, 8):
                    if grid[j][i] != 0:
                        if grid[j][i].piece_type == KING:
                            if grid[j][i].colour == self.colour:
                                king_coordinate = (i, j)
            for move in possibility_dict[self.colour]:
                fake_grid = grid
                fake_grid[move[1]][move[0]] = self
                fake_grid[y][x] = 0
                if grid[king_coordinate[1]][king_coordinate[0]].if_in_danger(move[0], move[1], fake_grid):
                    possibility_dict[self.colour].remove(move)

            return possibility_dict[self.colour]

    class Rook:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = ROOK

        def get_possibility(self, grid):
            (x, y) = self.position
            possible_moves = []
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
                    elif grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                        if grid[direction_coordinate[1]][direction_coordinate[0]].colour == self.colour:
                            break
                        else:
                            possible_moves.append(direction_coordinate)
                            break
                    else:
                        possible_moves.append(direction_coordinate)
            for i in range(0, 8):
                for j in range(0, 8):
                    if grid[j][i] != 0:
                        if grid[j][i].piece_type == KING:
                            if grid[j][i].colour == self.colour:
                                king_coordinate = (i, j)
            for move in possible_moves:
                fake_grid = grid
                fake_grid[move[1]][move[0]] = self
                fake_grid[y][x] = 0
                if grid[king_coordinate[1]][king_coordinate[0]].if_in_danger(move[0], move[1], fake_grid):
                    possible_moves.remove(move)
            return possible_moves

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

        def get_possibility(self, grid):
            (x, y) = self.position
            possible_moves = []
            for j in range(0, 8):
                for i in range(1, 9):
                    if j == 0:
                        direction_coordinate = (x - i, y + i)
                    elif j == 1:
                        direction_coordinate = (x + i, y - i)
                    elif j == 2:
                        direction_coordinate = (x + i, y + i)
                    else:
                        direction_coordinate = (x - i, y - i)
                    if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                        break
                    elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                        break
                    elif grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                        if grid[direction_coordinate[1]][direction_coordinate[0]].colour == self.colour:
                            break
                        else:
                            possible_moves.append(direction_coordinate)
                            break
                    else:
                        possible_moves.append(direction_coordinate)
            for i in range(0, 8):
                for j in range(0, 8):
                    if grid[j][i] != 0:
                        if grid[j][i].piece_type == KING:
                            if grid[j][i].colour == self.colour:
                                king_coordinate = (i, j)
            for move in possible_moves:
                fake_grid = grid
                fake_grid[move[1]][move[0]] = self
                fake_grid[y][x] = 0
                if grid[king_coordinate[1]][king_coordinate[0]].if_in_danger(move[0], move[1], fake_grid):
                    possible_moves.remove(move)
            return possible_moves

    class Queen:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = QUEEN

        def get_possibility(self, grid):
            (x, y) = self.position
            possible_moves = []
            for j in range(0, 4):
                for i in range(1, 9):
                    if j == 0:
                        direction_coordinate = (x - i, y)
                    elif j == 1:
                        direction_coordinate = (x + i, y)
                    elif j == 2:
                        direction_coordinate = (x, y + i)
                    elif j == 3:
                        direction_coordinate = (x, y - i)
                    elif j == 4:
                        direction_coordinate = (x - i, y + i)
                    elif j == 5:
                        direction_coordinate = (x + i, y - i)
                    elif j == 6:
                        direction_coordinate = (x + i, y + i)
                    else:
                        direction_coordinate = (x - i, y - i)
                    if direction_coordinate[1] > 7 or direction_coordinate[1] < 0:
                        break
                    elif direction_coordinate[0] > 7 or direction_coordinate[0] < 0:
                        break
                    elif grid[direction_coordinate[1]][direction_coordinate[0]] != 0:
                        if grid[direction_coordinate[1]][direction_coordinate[0]].colour == self.colour:
                            break
                        else:
                            possible_moves.append(direction_coordinate)
                            break
                    else:
                        possible_moves.append(direction_coordinate)
            for i in range(0, 8):
                for j in range(0, 8):
                    if grid[j][i] != 0:
                        if grid[j][i].piece_type == KING:
                            if grid[j][i].colour == self.colour:
                                king_coordinate = (i, j)
            for move in possible_moves:
                fake_grid = grid
                fake_grid[move[1]][move[0]] = self
                fake_grid[y][x] = 0
                if grid[king_coordinate[1]][king_coordinate[0]].if_in_danger(move[0], move[1], fake_grid):
                    possible_moves.remove(move)
            return possible_moves

    class King:
        def __init__(self, colour, x, y):
            self.colour = colour
            self.position = [x, y]
            self.piece_type = KING

        def if_in_danger(self, x, y, grid):
            pass


class Board:
    def __init__(self):
        self.grid = [
            [Piece.Rook(BLACK, 0, 0), Piece.Knight(BLACK, 1, 0), Piece.Bishop(BLACK, 2, 0),
             Piece.Queen(BLACK, 3, 0), Piece.King(BLACK, 4, 0), Piece.Bishop(BLACK, 5, 0),
             Piece.Knight(BLACK, 6, 0), Piece.Rook(BLACK, 7, 0)],
            [Piece.Pawn(BLACK, 0, 1), Piece.Pawn(BLACK, 1, 1), Piece.Pawn(BLACK, 2, 1), Piece.Pawn(BLACK, 3, 1),
             Piece.Pawn(BLACK, 4, 1), Piece.Pawn(BLACK, 5, 1), Piece.Pawn(BLACK, 6, 1), Piece.Pawn(BLACK, 7, 1)],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [Piece.Pawn(WHITE, 0, 6), Piece.Pawn(WHITE, 1, 6), Piece.Pawn(WHITE, 2, 6),
             # Piece.Pawn(WHITE, 3, 6),
             0, Piece.Pawn(WHITE, 4, 6), Piece.Pawn(WHITE, 5, 6),
             Piece.Pawn(WHITE, 6, 6), Piece.Pawn(WHITE, 7, 6)],
            [Piece.Rook(WHITE, 0, 7), Piece.Knight(WHITE, 1, 7), Piece.Bishop(WHITE, 2, 7), Piece.Queen(WHITE, 3, 7),
             Piece.King(WHITE, 4, 7), Piece.Bishop(WHITE, 5, 7), Piece.Knight(WHITE, 6, 7), Piece.Rook(WHITE, 7, 7)]
        ]
        self.active_block = (None, None)
        self.turn = WHITE
        self.active_block_possibilities = []
        self.win = None
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

    def calculate_piece_possibility(self):
        clicked_block = detect_player_click()
        self.active_block_possibilities = []
        if clicked_block is not None:
            if clicked_block != self.active_block:
                if clicked_block != 0:
                    if self.grid[clicked_block[1]][clicked_block[0]].colour == self.turn:
                        self.active_block_possibilities = self.grid[clicked_block[1]][clicked_block[0]].get_possibility(
                            self.grid)
                        self.active_block = clicked_block
                else:
                    self.active_block == (None, None)
            else:
                self.active_block == (None, None)

    def render_piece_possibility_white(self):
        if self.active_block != (None, None):
            for i in self.active_block_possibilities:
                self.win.blit(selected, [int((piecesize * (i[0])) + boardStartPoint[0]),
                                         int((piecesize * (i[1])) + boardStartPoint[1])])
            pygame.display.update()
        pygame.display.update()

    def initiate(self):
        self.win = pygame.display.set_mode((width, height))
        self.win.blit(chessboard, boardStartPoint)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.grid[i][j] != 0:
                    if self.grid[i][j].colour == WHITE:
                        self.win.blit(self.whiteDict[self.grid[i][j].piece_type], (
                            (self.grid[i][j].position[0]) * piecesize + boardStartPoint[0],
                            (self.grid[i][j].position[1]) * piecesize + boardStartPoint[1]))
                    if self.grid[i][j].colour == BLACK:
                        self.win.blit(self.blackDict[self.grid[i][j].piece_type], (
                            (self.grid[i][j].position[0]) * piecesize + boardStartPoint[0],
                            (self.grid[i][j].position[1]) * piecesize + boardStartPoint[1]))
        pygame.display.update()


# functions
def detect_player_click():
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            clicked_block = (
                (event.pos[0] - boardStartPoint[0]) // piecesize, (event.pos[1] - boardStartPoint[1]) // piecesize)
            return clicked_block
        else:
            return None


def generate_fake_grid(grid):
    fake_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    black_dict = {
        PAWN: 'bp',
        ROOK: 'br',
        KNIGHT: 'bn',
        BISHOP: 'bb',
        QUEEN: 'bq',
        KING: 'bk'
    }
    white_dict = {
        PAWN: 'wp',
        ROOK: 'wr',
        KNIGHT: 'wn',
        BISHOP: 'wb',
        QUEEN: 'wq',
        KING: 'wk'
    }

    for row in range(0, 8):
        for row_element in range(0, 8):
            if grid[row][row_element] != 0:
                if grid[row][row_element].colour == BLACK:
                    fake_grid[row][row_element] = black_dict[grid[row][row_element].type]
                if grid[row][row_element].colour == WHITE:
                    fake_grid[row][row_element] = white_dict[grid[row][row_element].type]
    return fake_grid


def give_grid(grid):
    for i in grid:
        for j in grid:
            print(j, '\n')


board = Board()
board.initiate()
while True:
    board.calculate_piece_possibility()
    board.render_piece_possibility_white()
