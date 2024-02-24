from const import *

class Clicker:
  
  def __init__(self) -> None:
    self.mouseX = 0
    self.mouseY = 0
    
    # move
    self.selected_piece = False
    self.initial_row = 0
    self.initial_col = 0
    self.piece = None
    
  
  def update_mouse(self, pos):
    self.mouseX, self.mouseY = pos
  
  def getRowCol(self):
    clicked_row = (self.mouseY-98)//SQ_SIZE
    clicked_col = (self.mouseX-31)//SQ_SIZE
    return clicked_row, clicked_col
  
  def save_initial(self, pos):
    self.initial_row = (pos[1] - 98) // SQ_SIZE
    self.initial_col = (pos[0] - 31) // SQ_SIZE
  
  def select_piece(self, piece):
    self.piece = piece
    self.selected_piece = True
    
  def unselect_piece(self):
    self.initial_row = 0
    self.initial_col = 0
    self.piece = None
    self.selected_piece = False