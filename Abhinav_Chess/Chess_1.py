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


class Board:
    def __init__(self):
        self.grid = [
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']
        ]
        self.turn = WHITE
        self.selected = None


