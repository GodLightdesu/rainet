from .const import *

class Move:
  
  def __init__(self, startsq:object, endsq:object) -> None:
    '''
    - startsq -> (row, col)
    - endsq   -> (row, col)
    '''
    # handle input
    self.startsq = startsq
    self.endsq = endsq
    
    self.startRow = self.startsq.row
    self.startCol = self.startsq.col
    self.endRow = self.endsq.row
    self.endCol = self.endsq.col
    
    # store data
    self.pieceMoved = startsq.piece
    self.pieceCaptured = endsq.piece
    
    # generat a unique id move each move
    self.moveID = self.startRow * 1000 + self.startCol  * 100 + self.endRow * 10 + self.endCol
    
  def __eq__(self, other: object) -> bool:
    if isinstance(other, Move):
      return self.moveID == other.moveID
    return False
  
  def getNotation(self):
    return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
  
  def getRankFile(self, r, c):
    return COL2FILE[c] + ROW2RANK[r]