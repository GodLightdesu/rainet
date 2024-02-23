class Square:
  
  def __init__(self, row, col, piece=None, fw=None, exit=None) -> None:
    self.row = row
    self.col = col
    self.piece = piece
    # fire wall
    self.fw = fw

    self.exit = exit
    self.boundary = False
    
class Exit:
  def __init__(self, color) -> None:
    self.color = color