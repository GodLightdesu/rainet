
from const import *
from square import *
from piece import *

class Board:
  
  def __init__(self) -> None:
    self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for row in range(ROWS)]
    self.moveLog = []
    self._create()
    self._add_Piece('yellow')
    self._add_Piece('blue')
    
  # private method (_methodName)
  def _create(self):
    # board
    for row in range(ROWS):
      for col in range(COLS):
        self.squares[row][col] = Square(row, col)
    
    # Exit
    for color in EXITPOS:
      for row, col in EXITPOS[color]:
        self.squares[row][col] = Square(row, col, exit=Exit(color))
        
    # Boundary
    for row, col in BOUNDARY_POS:
      self.squares[row][col].boundary = True
        
  def _add_Piece(self, color):
    for row, col in POS_INIT[color]:
      # init all pieces to unknown first
      self.squares[row][col] = Square(row, col, Unknown(color))