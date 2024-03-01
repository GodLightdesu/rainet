from decimal import *

MAX_FPS = 15
IMAGES = {}
SKILLS = ['lb', 'fw', 'vc', '404']

VIEWS = ['god', 'yellow', 'blue']
AVIEWS = ['yellow', 'blue']

WIDTH = 615
HEIGHT = 960
COLS = 8
ROWS = 10

WINNINGSCORE = 1000

SQ_SIZE = 70    # 68x68
PIECE_SIZE = 63 # 63x63

DIS = 10

POS_INIT = {
  # bottom
  'yellow' : [(8, 0), (8, 1), (8, 2), (7, 3), (7, 4), (8, 5), (8, 6), (8, 7)],
  # top
  'blue' : [(1, 0), (1, 1), (1, 2), (2, 3), (2, 4), (1, 5), (1, 6), (1, 7)]
}

YSERVERROL = 0
BSERVERROL = 9

BOUNDARY_POS = [(0, 0), (0, 1), (0, 2), (0, 5), (0, 6), (0, 7), (9, 0), (9, 1), (9, 2), (9, 5), (9, 6), (9, 7)]

EXITPOS = {
  'yellow': [(0, 3), (0, 4)],
  'blue': [(9, 3), (9, 4)]
}

NONFWPOS = [
  (0, 0), (0, 1), (0, 2), (0, 5), (0, 6), (0, 7), (9, 0), (9, 1), (9, 2), (9, 5), (9, 6), (9, 7),
  (0, 3), (0, 4), (9, 3), (9, 4), 
  (1, 3), (1, 4), (8, 3), (8, 4)
]

FILE2COL = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h':7}
COL2FILE = {v: k for k, v in FILE2COL.items()}

RANK2ROW = {'0': 9, '1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 1, '9': 0}
ROW2RANK = ({v: k for k, v in RANK2ROW.items()})

YSKILLSROW = {
  5 : 'lb',
  6 : 'fw',
  7 : 'vc',
  8 : '404'
}

BSKILLSROW = {
  4 : 'lb',
  3 : 'fw',
  2 : 'vc',
  1 : '404'
}

ROW = [row for row in range(ROWS)]
COL = [col for col in range(COLS)]

BROW = ROW
BROW.reverse()

BCOL = COL
BCOL.reverse()

PIECEVALUE = {
  # 'link' : Decimal(2.0),
  # 'virus' : Decimal(1.0),
  # 'unknown' : Decimal(1.5)
  'link' : 10,
  'virus' : 10,
  'unknown' : 10
}