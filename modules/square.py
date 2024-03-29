class Square:
  
  def __init__(self, row:int, col:int, piece:object=None, fw:object=None, exit:object=None) -> None:
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
  def has_ally_piece(self, color:str) -> bool:
    return self.has_piece() and self.piece.color == color
  
  def has_enemy_piece(self, color:str) -> bool:
    return self.has_piece() and self.piece.color != color
  
  # fire wall
  def has_ally_fw(self, color:str) -> bool:
    return self.has_fw() and self.fw.color == color
  
  def has_enemy_fw(self, color:str) -> bool:
    return self.has_fw() and self.fw.color != color
  
  # exit
  def is_ally_exit(self, color:str) -> bool:
    return self.exit is not None and self.exit.color == color
  
  def is_enemy_exit(self, color:str) -> bool:
    return self.exit is not None and self.exit.color != color
    
  def can_pass(self, color) -> bool:
    return (not self.has_ally_piece(color) and 
            not self.has_enemy_fw(color) and 
            not self.is_enemy_exit(color) and 
            not self.boundary) 
    
  def isBlocked(self, color) -> bool:
    return self.has_enemy_fw(color) or self.has_piece() or self.boundary == True or self.is_enemy_exit(color)
    
class Exit:
  def __init__(self, color:str) -> None:
    self.color = color