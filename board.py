from move import Move

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
    
  def move(self):
    pass
  
  def calc_moves(self, piece: object, startRow: int, startCol: int):
    '''
    Calculate all the possible (valid) moves of an specific piece on a specific position
    '''
    
    def isValidMove(endRow: int, endCol: int) -> bool:
      '''
      True
      - empty square -> True
      - enenmy piece -> True  -> capture piece
      - server       -> True  -> enter server
      
      False
      - self piece   -> False
      - enemy FW     -> False
      - boundary     -> False
      - enemy server -> False
      '''
      if 0 <= endRow < 10 and 0 <= endCol < 8:
        if self.squares[endRow][endCol].can_pass(piece.color): valid = True
        else: valid = False
      else: valid = False
      return valid
    
    def nonLB_move():
      possible_moves = [
        (startRow -1, startCol), 
        (startRow +1, startCol), 
        (startRow, startCol -1), 
        (startRow, startCol +1)
      ]
      
      for possible_move in possible_moves:
        endRow, endCol = possible_move
        if isValidMove(endRow, endCol):
          # create asquares for the new move
          startSq = Square(startRow, startCol)
          endSq = Square(endRow, endCol)
          # create new move
          move = Move(startSq, endSq)
          # apeend new valid move
          piece.add_move(move)
    
    def LB_move():
      pass    
    
    # lb piece
    if piece.lb: LB_move()
    # non lb piece
    else: nonLB_move()
    
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
        
  def _add_Piece(self, color: str):
    for row, col in POS_INIT[color]:
      # init all pieces to unknown first
      self.squares[row][col] = Square(row, col, Unknown(color))