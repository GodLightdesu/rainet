class Square:
  
  def __init__(self, row, col, piece=None, fw=None, exit=None) -> None:
    self.row = row
    self.col = col
    self.piece = piece
    # fire wall
    self.fw = fw

    self.exit = exit
    self.boundary = False
    
  # square
  def has_piece(self) -> bool:
    return self.piece != None
  
  def has_fw(self) -> bool:
    return self.fw != None
  
  # piece
  def has_ally_piece(self, color) -> bool:
    return self.has_piece() and self.piece.color == color
  
  def has_enemy_piece(self, color) -> bool:
    return self.has_piece() and self.piece.color != color
  
  # fire wall
  def has_ally_fw(self, color) -> bool:
    return self.has_fw() and self.fw.color == color
  
  def has_enemy_fw(self, color) -> bool:
    return self.has_fw() and self.fw.color != color
  
  # exit
  def is_ally_exit(self, color) -> bool:
    if self.exit is None:
      return False
    elif self.exit.color == color:
      return True
    else:
      return False
  
  def is_enemy_exit(self, color) -> bool:
    if self.exit is None:
      return False
    elif self.exit.color != color:
      return True
    else:
      return False
    
class Exit:
  def __init__(self, color) -> None:
    self.color = color