import pygame as py
from pygame.locals import *

from const import *
from game import Game

import sys

class Main:
  def __init__(self, yellowInit, blueInit, yellowID=None, blueID=None) -> None:
    if (self.checkPieceInit(yellowInit) == False or 
        self.checkPieceInit(blueInit) == False):
      raise ValueError('Invalid piece init, please try again')
  
    py.init()
    self.screen = py.display.set_mode((750, 960), RESIZABLE)
    py.display.set_caption('Rai-Net')
    self.clock = py.time.Clock()
    
    self.game = Game(yellowInit, blueInit, yellowID, blueID)
    self.yellowInit = yellowInit
    self.blueInit = blueInit
    self.yellowID = yellowID
    self.blueID = blueID
    
    # only do this once, before the while loop
    self.game.loadImages()

  def checkPieceInit(self, pieceInit):
    v, l = 0, 0
    for piece in pieceInit:
      if piece == 'v':  v += 1
      elif piece == 'l': l += 1
    
    if v != 4 or l != 4:  return False
    else: return True
  
  
  def Gback(self):
    screen = self.screen
    game = self.game
    
    while True:
      # handle human input data
      for event in py.event.get():
        
        # quit game
        if event.type == py.QUIT:
          py.quit()
          sys.exit()

         # mouse handler
       
        elif event.type == py.MOUSEBUTTONDOWN:
          if not game.gameOver:
            pass
        
        # key handler
        elif event.type == py.KEYDOWN:
          # undo when 'z' is pressed
          if event.key == py.K_z: 
            pass
          
          # reset the game when 'r' pressed
          if event.key == py.K_r:
            pass
      
      # game logic
      if not game.gameOver:
        pass
      
      # render game
      game.message = 'test'
      game.DrawGameState(screen)
      game.drawText(screen, game.message)
      
      self.clock.tick(MAX_FPS)
      py.display.flip()