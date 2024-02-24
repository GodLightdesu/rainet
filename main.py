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
    board = self.game.board
    clicker = self.game.clicker
    
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
            clicker.update_mouse(event.pos)
            clicked_row, clicked_col = clicker.getRowCol()
            # print(clicked_row, clicked_col)
            
            # cancel use skill
            if clicked_col > 7 and game.useSkill == True:
              print('cancel use skill')
              game.whichSkill = None
              game.useSkill = False
            
            # skills' col -> check which skill is clicked
            elif clicked_col == 9:
              if game.player.color == 'yellow' and 5 <= clicked_row <= 8:
                game.whichSkill = YSKILLSROW[clicked_row]
              elif  game.player.color == 'blue' and 1 <= clicked_row <= 4:
                game.whichSkill = BSKILLSROW[clicked_row]
              
              if game.whichSkill is not None:  game.useSkill = True
              else: game.useSkill = False
              print(game.whichSkill)
            
            # use skill (which)
            elif clicked_col <= 7 and game.useSkill == True and game.moveMade == False:
              print('use skill')
            
            # if clicked square has a piece ?
            elif (clicked_col <= 7 and 
                  game.useSkill == False and game.skillUsed == False and
                  board.squares[clicked_row][clicked_col].has_ally_piece(game.player.color)):
              print('move')
            
            # no ally piece
            else: print('not ally piece')
            
        
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
      # game.message = 'test'
      game.DrawGameState(screen)
      game.drawText(screen, game.message)
      
      # check winner
      winner = game.checkGameOver()
      if winner is not None:
        game.message = winner + ' wins'
        game.gameOver = True
      
      self.clock.tick(MAX_FPS)
      py.display.flip()