import sys, os
import pygame as py
from typing import Literal
from pygame.locals import *

from .const import *
from .game import Game
from .move import Move

class Main:
  def __init__(self, yellow: object, blue: object,
               view: Literal['god', 'yellow', 'blue']='god', cheat=False) -> None:
    if yellow is None or blue is None or yellow.color == blue.color:
      raise ValueError('Invalid Player, please try again')
    
    py.init()
    self.screen = py.display.set_mode((750, 960), RESIZABLE)
    py.display.set_caption('Rai-Net')
    self.clock = py.time.Clock()
    
    getcontext().prec = 6
    
    self.view = view
    self.cheat = cheat
    
    self.game = Game(yellow, blue, view)
    
    # True if yellow is human, elif yellow is AI -> False
    self.humanOne = yellow.isHuman if yellow.color == 'yellow' else blue.isHuman
    # same as above but for blue
    self.humanTwo = blue.isHuman if blue.color == 'blue' else yellow.isHuman
    
    # only do this once, before the while loop
    self.game.loadImages()
  
  def Gback(self):
    '''
    for god view or yellow view
    '''
    
    game = self.game
    board = self.game.board
    clicker = self.game.clicker
    skill = self.game.skill
    screen = self.screen
    
    # clear screen before game run
    os.system('clear')
    
    while True:
      humanTurn = (self.humanOne and game.yellowToMove()) or (self.humanTwo and not game.yellowToMove())
      
      # handle human input data
      for event in py.event.get():
        
        # quit game
        if event.type == py.QUIT:
          py.quit()
          sys.exit()

        # mouse handler
        elif event.type == py.MOUSEBUTTONDOWN:
          
          # human decision
          if not game.gameOver and humanTurn:
            # view 'god' and 'yellow' use same board
            if self.view == 'god' or self.view == 'yellow':
              clicker.updateMouse(event.pos)
              clicked_row, clicked_col = clicker.getRowCol()
            elif self.view == 'blue':
              clicker.updateMouse(event.pos)
              brow, bcol = clicker.getRowCol()
              clicked_row, clicked_col = clicker.convertBlueRow(brow), bcol

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
              
              # get which skill use
              if game.player.color == 'yellow' and 5 <= clicked_row <= 8:
                game.whichSkill = YSKILLSROW[clicked_row]
              elif  game.player.color == 'blue' and 1 <= clicked_row <= 4:
                game.whichSkill = BSKILLSROW[clicked_row]
              
              # check clicked in skills
              if game.whichSkill is None:  game.useSkill = False
              else:
                # Show description when click skills
                if game.whichSkill == 'lb': game.message = 'Select a ally piece to use LineBoost'
                elif game.whichSkill == 'fw': game.message = 'Select a square to use FireWall'
                elif game.whichSkill == 'vc': game.message = 'Select a enemy piece to check'
                elif game.whichSkill == '404': game.message = 'Select 2 ally pieces to swap'
                game.useSkill = True
              # print('Used -> ', game.whichSkill)
            
            # use skill (which) when player choosed to use skill
            elif board.onBoard(clicked_row, clicked_col) and game.useSkill == True and game.moveMade == False:
              # print('use skill')
              clicker.savePlayerClicks(clicked_row, clicked_col)
              
              # need two clicks
              if game.whichSkill == '404':
                # display option of either swap or not after selected two piece
                if len(clicker.playerClicks) == 2:
                  target0 = clicker.playerClicks[0]
                  target1 = clicker.playerClicks[1]
                  row0, col0 = target0
                  row1, col1 = target1
                  targetSq0 = board.squares[row0][col0]
                  targetSq1 = board.squares[row1][col1]
                  if targetSq0.has_ally_piece(game.player.color) and targetSq1.has_ally_piece(game.player.color):
                    game.displayOption = True
                  else: 
                    game.whichSkill = None
                    game.useSkill = False
              
                # use skill
                elif len(clicker.playerClicks) == 3:
                  target0 = clicker.playerClicks[0]
                  target1 = clicker.playerClicks[1]
                  row, col = clicker.playerClicks[2]
                  if self.view == 'blue': row = game.clicker.convertBlueRow(row)
                  
                  if row == 5 and col == 3: skill.swap = True
                  elif row == 5 and col == 4: skill.swap = False
                  else:
                    print('cancel use skill')
                    game.displayOption = False
                    game.whichSkill = None
                    game.useSkill = False
                    continue
                  
                  # after choose pieces and either swap or not
                  game.displayOption = False
                  game.skillUsed = skill.use(game, game.whichSkill, target0, target1, skill.swap)
                  clicker.claerPlayerClicks()
                  
                  # not valid target
                  if not game.skillUsed:
                    # clicker.claerPlayerClicks()
                    game.whichSkill = None
                    game.useSkill = False
                    
              # only need one click
              else:
                target0 = (clicked_row, clicked_col)
                game.skillUsed = skill.use(game, game.whichSkill, target0)
                clicker.claerPlayerClicks()
                
                # not valid target
                if not game.skillUsed:
                  clicker.claerPlayerClicks()
                  game.displayOption = False
                  game.whichSkill = None
                  game.useSkill = False



            # after selected piece and clicked square to move
            elif game.useSkill == False and clicker.selected_piece and board.onBoard(clicked_row, clicked_col):
              
              # get another ally piece
              if board.squares[clicked_row][clicked_col].has_ally_piece(game.player.color):               
                # different pieces
                if (clicked_row, clicked_col) != (clicker.initial_row, clicker.initial_col):
                  clicker.piece.clear_moves()
                  clicker.unselectPiece()
                  
                  piece = board.squares[clicked_row][clicked_col].piece   
                  board.calc_moves(piece, clicked_row, clicked_col)
                  clicker.saveInitial(clicked_row, clicked_col)
                  clicker.selectPiece(piece)
                
                # clicked same piece
                else:
                  clicker.piece.clear_moves()
                  clicker.unselectPiece()
              
              # square to move
              else:
                startsq = game.board.squares[clicker.initial_row][clicker.initial_col]
                endsq = game.board.squares[clicked_row][clicked_col]
                
                game.move = Move(startsq, endsq)
                if board.validMove(clicker.piece, game.move):
                  
                  board.move(game, clicker.piece, game.move)
                  game.animate = True
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
              clicker.saveInitial(clicked_row, clicked_col)
              clicker.selectPiece(piece)
                
            # debug
            # print(game.useSkill, game.skillUsed, game.moveMade)
              
        # key handler
        elif event.type == py.KEYDOWN:
          # undo when 'z' is pressed
          if event.key == py.K_z: 
            if not game.Yellow.isHuman or not game.Blue.isHuman:
              # undo for both that there is one is AI
              game.undo()
              game.undo()
            else: game.undo()
            game.animate = False
       
          # reset the game when 'r' pressed
          if event.key == py.K_r:
            game.reset(game.Yellow, game.Blue, self.view)
            game = self.game
            board = self.game.board
            clicker = self.game.clicker
            skill = self.game.skill
            screen = self.screen
            humanTurn = (self.humanOne and game.yellowToMove()) or (self.humanTwo and not game.yellowToMove())
            os.system('clear')
          
          # change game mode (cheat / normal) when 'c' pressed
          if event.key == py.K_c:
            self.cheat = not self.cheat
            print('Game mode ->', 'cheat' if self.cheat else 'normal')
            
            # normal does not have god view
            if not self.cheat and self.view == 'god':
              self.view = game.nextView(VIEWS, self.view)
              game.view = game.nextView(VIEWS, game.view)
          
          # change view of board when 'v' pressed
          if event.key == py.K_v:
            if self.view == 'god' and not self.cheat:
              self.view = game.nextView(VIEWS, self.view)
              game.view = game.nextView(VIEWS, game.view)
            elif self.cheat:
              self.view = game.nextView(VIEWS, self.view)
              game.view = game.nextView(VIEWS, game.view)
            else:
              self.view = game.nextView(AVIEWS, self.view)
              game.view = game.nextView(AVIEWS, game.view)
          
          # clear the terminal output when 'space' pressed 
          if event.key == py.K_SPACE:
            os.system('clear')
          
          # print console board when 'b' pressed
          if event.key == py.K_b:
            board.printBoard(game.Yellow, game.Blue, self.view)
          
          # print detail game info when 'i' pressed
          if event.key == py.K_i:
            print('-------------------------------------')
            print('Turn', game.turn, '| player:', game.player.name, '| enemy:', game.enemy.name)
            print('Game log:')
            if len(game.gamelog) != 0:
              for key in game.gamelog:
                if game.gamelog[key] not in SKILLS:
                  print(f'{key}.{game.gamelog[key].moveID}', end = '\n' if key % 5 == 0 else " ")
                else: print(f'{key}.{game.gamelog[key]}', end = '\n' if key % 5 == 0 else " ")
            print()
              
            print(game.player.name, ':', game.player.skills['lb']['log'])
            print(game.enemy.name, ':', game.enemy.skills['lb']['log'])
            print('-------------------------------------')
            
      # game logic
      if not game.gameOver:
        # AI decision
        if not humanTurn and not game.moveMade and not game.skillUsed:
          game.animate = True

          game.player.Search(game, 2)
          if game.player.bestMove is None:
            validMoves = game.getValidMoves()
            game.move = game.player.findRandomMove(validMoves)
            game.clearValidMoves()
          else:
            print('bestMove:', game.player.bestMove.moveID)
            game.move = game.player.bestMove
          
          piece = game.move.pieceMoved
          board.move(game, piece, game.move)
          game.moveMade = True
          
          # # collect information for AI decision
          # validMoves = game.getValidMoves()
          # allyPieces = game.board.getAllyPieces(game.player.color)

          # # make decision
          # decisions = game.player.decision(game, validMoves, allyPieces)
          
          # # skill
          # if decisions['skill'] is not None:
          #   game.whichSkill = decisions['skill'][0]
          #   piece = decisions['skill'][1]
          #   target0 = game.board.findPiecePos(piece)
          #   game.skillUsed = skill.use(game, game.whichSkill, target0)
          
          # # move
          # elif decisions['move'] is not None:
          #   game.move = decisions['move']
          #   piece = game.move.pieceMoved
          #   board.move(game.player, game.enemy, piece, game.move)
          #   validMoves = None
          #   game.moveMade = True
          
          # # reset
          # game.clearValidMoves()
          
        
        # moved
        if game.moveMade:
          if game.animate:  game.animateMove(screen, game.move)
          # print(game.enemy.name, game.Blue.scoreBoard(game))
          
          game.move = None
          game.animate = False
          game.moveMade = False
        
        # used skill
        elif game.skillUsed:
          game.whichSkill = None
          game.useSkill = False
          game.undoSkill = False
          game.skillUsed = False

      # render game
      game.DrawGameState(screen)
      game.drawText(screen, game.message)
      
      # check winner
      winner = game.checkGameOver()
      if winner is not None:
        game.message = winner + ' wins'
        game.gameOver = True
      
      self.clock.tick(MAX_FPS)
      py.display.flip()