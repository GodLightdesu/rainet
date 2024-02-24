from const import *

class Clicker:
  
  def __init__(self) -> None:
    self.mouseX = 0
    self.mouseY = 0
  
  def update_mouse(self, pos):
    self.mouseX, self.mouseY = pos
  
  def getRowCol(self):
    clicked_row = (self.mouseY-98)//SQ_SIZE
    clicked_col = (self.mouseX-31)//SQ_SIZE
    return clicked_row, clicked_col