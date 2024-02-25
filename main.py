import pygame as py
from pygame.locals import *

from const import *
from game import Game
from move import Move
from skill import Skill

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
    
    self.skill = Skill()
    
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
    skill = self.skill
    
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
            clicker.updateMouse(event.pos)
            clicked_row, clicked_col = clicker.getRowCol()
            # print(clicked_row, clicked_col)
            
            # cancel use skill only when player choosed to use skill but not used
            if clicked_col > 7 and game.useSkill == True and game.skillUsed == False:
              print('cancel use skill')
              game.whichSkill = None
              game.useSkill = False
            
            # skills' col -> check which skill is clicked when player not choosed to use skill
            elif clicked_col == 9 and game.moveMade == False and game.useSkill == False:
              # not display the valid moves of selected piece if skill selected
              if clicker.selected_piece:
                clicker.piece.clear_moves()
              
              if game.player.color == 'yellow' and 5 <= clicked_row <= 8:
                game.whichSkill = YSKILLSROW[clicked_row]
              elif  game.player.color == 'blue' and 1 <= clicked_row <= 4:
                game.whichSkill = BSKILLSROW[clicked_row]
              
              # not clicked in skills
              if game.whichSkill is None:  game.useSkill = False
              else: game.useSkill = True
              print(game.whichSkill)
            
            # use skill (which) when player choosed to use skill
            elif board.onBoard(clicked_row, clicked_col) and game.useSkill == True and game.moveMade == False:
              print('use skill')
              clicker.savePlayerClicks(clicked_row, clicked_col)
              
              # need two clicks
              if game.whichSkill == '404':
                if len(clicker.playerClicks) == 2:
                  target0 = clicker.playerClicks[0]
                  target1 = clicker.playerClicks[1]
                  game.skillUsed = skill.use(game.board, game.player, game.whichSkill, target0, target1)
                  clicker.claerPlayerClicks()
                
                  # not valid target
                  if not game.skillUsed:
                    clicker.claerPlayerClicks()
                    game.whichSkill = None
                    game.useSkill = False
              
              # only need one click
              else:
                target0 = (clicked_row, clicked_col)
                game.skillUsed = skill.use(game.board, game.player, game.whichSkill, target0)
                clicker.claerPlayerClicks()
                
                # not valid target
                if not game.skillUsed:
                  clicker.claerPlayerClicks()
                  game.whichSkill = None
                  game.useSkill = False

            
            # after selected piece and clicked square to move
            elif game.useSkill == False and clicker.selected_piece and board.onBoard(clicked_row, clicked_col):
              
              startsq = game.board.squares[clicker.initial_row][clicker.initial_col]
              endsq = game.board.squares[clicked_row][clicked_col]
              
              game.move = Move(startsq, endsq)
              if board.validMove(clicker.piece, game.move):
                
                board.move(game.player, game.enemy, clicker.piece, game.move)
                game.moveMade = True
              
              # else: print('Invalid move')
              
              # not display the valid moves of selected piece
              clicker.piece.clear_moves()
              clicker.unselectPiece()  # unselect piece either moved or not
            
            # if clicked square has a piece ? -> move
            elif (board.onBoard(clicked_row, clicked_col) and 
                  game.useSkill == False and game.skillUsed == False and 
                  board.squares[clicked_row][clicked_col].has_ally_piece(game.player.color)):
              
              # select piece
              piece = board.squares[clicked_row][clicked_col].piece   
              board.calc_moves(piece, clicked_row, clicked_col)
              clicker.saveInitial(event.pos)
              clicker.selectPiece(piece)
                
            # debug
            # print(game.useSkill, game.skillUsed, game.moveMade)
        
        # key handler
        elif event.type == py.KEYDOWN:
          # undo when 'z' is pressed
          if event.key == py.K_z: 
            if len(game.gamelog) != 0:
              # undo move
              if list(game.gamelog)[-1] not in SKILLS:
                board.undoMove(game)
                game.message = 'Undo move'
                
                moveMade = True
                gameOver = False
              
          
          # reset the game when 'r' pressed
          if event.key == py.K_r:
            pass
          
          # primt console board when 'b' pressed
          if event.key == py.K_b:
            board.printBoard()
      
      # game logic
      if not game.gameOver:
        
        # human
        if game.moveMade:
          game.message = f'Moved: {game.move.getNotation()}'
          game.movelog[game.turn] = game.move
          game.gamelog[game.turn] = game.move
          game.switchPlayer()
        
        # used skill
        elif game.skillUsed:
          game.message = f'Used: {game.whichSkill}'
          game.skillLog[game.turn] = game.whichSkill
          game.gamelog[game.turn] = game.whichSkill
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