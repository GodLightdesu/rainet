import os
from .const import *
class Piece:
  
  def __init__(self, name:str, color:str, value:float, lb=False, checked=False, texture=None, texture_rect=None) -> None:
    self.name = name
    self.color = color
    # value_sign = 1 if color == 'yellow' else -1
    # self.value = value * value_sign
    self.value = value
    self.lb = lb
    self.checked = checked
    self.moves = []
    # self.moved = False
    self.texture = texture
    self.set_texture()
    self.texture_rect = texture_rect
    
  def set_texture(self):
    self.texture = os.path.join(
      f'assets/images/{self.color}_{self.name}.png')
    
  def add_move(self, move:object):
    self.moves.append(move)
  
  def clear_moves(self):
    self.moves = []
  
class Link(Piece):
  
  def __init__(self, color:str, lb=False, checked=False) -> None:
    super().__init__('link', color, PIECEVALUE['link'], lb, checked)
    
class Virus(Piece):
  
  def __init__(self, color:str, lb=False, checked=False) -> None:
    super().__init__('virus', color, PIECEVALUE['virus'], lb, checked)
    
class Unknown(Piece):
  
  def __init__(self, color:str, lb=False, checked=False) -> None:
    super().__init__('unknown', color, PIECEVALUE['unknown'], lb, checked)