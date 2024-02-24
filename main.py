import pygame as py
from pygame.locals import *

from const import *
from game import Game
from move import Move
import skill

import sys

class Main:
  def __init__(self, yellowInit:str, blueInit:str, yellowID:str=None, blueID:str=None) -> None:
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

  def checkPieceInit(self, pieceInit:str):
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
            print(clicked_row, clicked_col)
            
            # cancel use skill
            if clicked_col > 7 and game.useSkill == True and game.skillUsed == False:
              print('cancel use skill')
              game.whichSkill = None
              game.useSkill = False
            
            # skills' col -> check which skill is clicked
            elif clicked_col == 9 and game.moveMade == False:
              if game.player.color == 'yellow' and 5 <= clicked_row <= 8:
                game.whichSkill = YSKILLSROW[clicked_row]
              elif  game.player.color == 'blue' and 1 <= clicked_row <= 4:
                game.whichSkill = BSKILLSROW[clicked_row]
              
              if game.whichSkill is not None:  game.useSkill = True
              else: game.useSkill = False
              print(game.whichSkill)
            
            # use skill (which)
            elif board.onBoard(clicked_row, clicked_col) and game.useSkill == True and game.moveMade == False:
              print('use skill')
              # clicker.save_initial(event.pos)
              
              # # need two click
              # if game.whichSkill == '404':
              #   target0 = (clicker.initial_col, clicker.initial_row)
              #   target1 = (clicked_row, clicked_col)
              #   game.skillUsed = skill.use(game.board, game.player, game.whichSkill, target0, target1)
              
              # # only need one click
              # else:
              #   target0 = (clicker.initial_col, clicker.initial_row)
              #   game.skillUsed = skill.use(game.board, game.player, game.whichSkill, target0)
            
            
            
            # after selected piece and clicked square to move
            elif game.useSkill == False and clicker.selected_piece and board.onBoard(clicked_row, clicked_col):
              
              startsq = game.board.squares[clicker.initial_row][clicker.initial_col]
              endsq = game.board.squares[clicked_row][clicked_col]
              
              move = Move(startsq, endsq)
              if board.validMove(clicker.piece, move):
                
                board.move(game.player, game.enemy, clicker.piece, move)
                game.moveMade = True
              
              # else: print('Invalid move')
              clicker.unselect_piece()  # unselect piece either moved or not
            
            # if clicked square has a piece ? -> move
            elif (board.onBoard(clicked_row, clicked_col) and 
                  game.useSkill == False and game.skillUsed == False and 
                  board.squares[clicked_row][clicked_col].has_ally_piece(game.player.color)):
              
              # clicked the same piece twice
              if (clicked_row, clicked_col) == (clicker.initial_row, clicker.initial_col):
                print('clicked twice')
                clicker.unselect_piece()
              
              # select piece
              else:
                piece = board.squares[clicked_row][clicked_col].piece   
                board.calc_moves(piece, clicked_row, clicked_col)
                clicker.save_initial(event.pos)
                clicker.select_piece(piece)
        
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
        
        # human
        if game.moveMade:
          game.message = f'Moved: {move.getNotation()}'
          game.switchPlayer()
          
        elif game.skillUsed:
          game.message = f'Used: {game.whichSkill}'
          game.switchPlayer()
          
      
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