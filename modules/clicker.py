from .const import *

class Clicker:
  
  def __init__(self) -> None:
    self.mouseX = 0
    self.mouseY = 0
    
    self.initial_row = 0
    self.initial_col = 0
    
    self.sqSelected = ()
    self.playerClicks = []
    
    self.selected_piece = False
    self.piece = None
    
  
  def updateMouse(self, pos):
    self.mouseX, self.mouseY = pos
  
  def getRowCol(self):
    clicked_row = (self.mouseY-98)//SQ_SIZE
    clicked_col = (self.mouseX-31)//SQ_SIZE
    return clicked_row, clicked_col
  
  def convertBlueRow(self, row):
    return BROW[row]
  
  def convertBlueCol(self, col):
    return BCOL[col]
  
  def saveInitial(self, row, col):
    self.initial_row = row
    self.initial_col = col
  
  def selectPiece(self, piece):
    self.piece = piece
    self.selected_piece = True
    
  def unselectPiece(self):
    self.initial_row = 0
    self.initial_col = 0
    self.piece = None
    self.selected_piece = False
  
  def savePlayerClicks(self, clicked_row, clicked_col):
    self.sqSelected = (clicked_row, clicked_col)
    self.playerClicks.append(self.sqSelected)
  
  def claerPlayerClicks(self):
    self.sqSelected = ()
    self.playerClicks = []