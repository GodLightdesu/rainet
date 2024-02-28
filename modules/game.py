import pygame as py
import os

from typing import Literal

from modules.skill import Skill
from .player import Player
from .board import Board
from .clicker import Clicker

from .const import *
from .square import *
from .piece import *

class Game:
  # init
  def __init__(self, yellow: object, blue: object,
               view: Literal['god', 'yellow', 'blue']='god', cheat=False) -> None:
    
    self.board = Board()
    self.clicker = Clicker()
    self.skill = Skill()
    
    # game init
    self.message = ''
    self.gameOver = False
    self.turn = 1
    self.movelog = {}
    self.skillLog = {}
    self.gamelog = {}
    
    self.animate = False
    self.view = view
    
    self.Yellow = yellow
    self.Blue = blue
    self.players = [self.Yellow, self.Blue]
    self.player = self.players[(self.turn + 1) % 2]
    self.enemy = self.players[self.turn % 2]
    
    self.displayOption = False
    
    # move init
    self.move = None
    self.moveMade = False
    
    # skill init
    self.whichSkill = None
    self.useSkill = False
    self.skillUsed = False
    self.undoSkill = False
    
    # piece init
    self.initPiece(self.Yellow)
    self.initPiece(self.Blue)
  
  def loadImages(self):
    IMAGES['BG'] = py.transform.scale(py.image.load("assets/images/BG.png"), (750, HEIGHT))
    IMAGES['b_board'] = py.image.load("assets/images/b_board.png")
    IMAGES['y_board'] = py.image.load("assets/images/y_board.png")
    # top
    IMAGES['b_top'] = py.image.load("assets/images/b_top.png")
    IMAGES['y_top'] = py.image.load("assets/images/y_top.png")
    # bottom
    IMAGES['b_bottom'] = py.image.load("assets/images/b_bottom.png")
    IMAGES['y_bottom'] = py.image.load("assets/images/y_bottom.png")
    
    # skills
    IMAGES['LB'] = py.transform.scale(py.image.load('assets/images/' + 'LB' + '.png'), (52, 52))
    IMAGES['shield'] = py.transform.scale(py.image.load('assets/images/' + 'shield' + '.png'), (80, 88))
    IMAGES['checked'] = py.transform.scale(py.image.load('assets/images/' + 'checked' + '.png'), (52, 56))
    # IMAGES['target'] = py.transform.scale(py.image.load('assets/images/' + 'target' + '.png'), (56, 56))
    IMAGES['LB'].convert()
    IMAGES['LB'].set_alpha(170)
    IMAGES['checked'].convert()
    IMAGES['checked'].set_alpha(150)
    
    # init skills' image
    for skill in SKILLS:
      IMAGES['blue_' + skill] = py.transform.scale(py.image.load('assets/images/blue_' + skill + '.png'), (PIECE_SIZE, PIECE_SIZE))
      IMAGES['yellow_' + skill] = py.transform.scale(py.image.load('assets/images/yellow_' + skill + '.png'), (PIECE_SIZE, PIECE_SIZE))
      IMAGES['blue_' + skill].convert()
      IMAGES['yellow_' + skill].convert()
      
  # display method
  def drawText(self, surface, text:str):
    font = py.font.SysFont("font/SoukouMincho.ttf", 40, False, False)
    # font = py.font.SysFont("arial", 40, False, False)
    textObject = font.render(text, 0, py.Color('white'))
    textLocation = py.Rect(0, 0, WIDTH, 70).move(WIDTH/2 - textObject.get_width()/2, 70/2 - textObject.get_height()/2)
    surface.blit(textObject, textLocation)
  
  def DrawGameState(self, surface, exceptPiece:object=None, Srow=None, Scol=None):
    self.drawBoard(surface)
    self.drawGameInfo(surface, self.Yellow, self.Blue)
    self.drawSquare(surface, exceptPiece, Srow, Scol)
    self.drawSkills(surface, self.Yellow, self.Blue)
    self.showMoves(surface)
  
  def drawBoard(self, surface):
    surface.blit(IMAGES['BG'], (0, 0))
    if self.view == 'god'or self.view == 'yellow':
      surface.blit(IMAGES['y_top'], (0, 0))
      surface.blit(IMAGES['y_board'], (0, 72))
      surface.blit(IMAGES['y_bottom'], (0, 817))
    elif self.view == 'blue':
      surface.blit(IMAGES['b_top'], (0, 0))
      surface.blit(IMAGES['b_board'], (0, 71))
      surface.blit(IMAGES['b_bottom'], (0, 817))
  
  def drawGameInfo(self, surface, Yellow:object, Blue:object):
    if self.view == 'god' or self.view == 'yellow':
      # name
      font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 45, True, False)
      
      text = 'yellow' if Yellow.name is None else Yellow.name
      yellowInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(20, 837, WIDTH/5, 70)
      surface.blit(yellowInfo, textLocation)
      
      text = 'blue' if Blue.name is None else Blue.name
      blueInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(450, 837, WIDTH/5, 70)
      surface.blit(blueInfo, textLocation)
      
      # score
      font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 40, True, False)
    
      text = 'link: ' + str(Yellow.link_eat)
      yellowInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(190, 825, WIDTH/5, 70)
      surface.blit(yellowInfo, textLocation)
      
      text = 'virus: ' + str(Yellow.virus_eat)
      yellowInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(190, 855, WIDTH/5, 70)
      surface.blit(yellowInfo, textLocation)
      
      text = 'link: ' + str(Blue.link_eat)      
      blueInfo = font.render(text, 0, py.Color('black'))
      textLocation = py.Rect(340, 825, WIDTH/5, 70)
      surface.blit(blueInfo, textLocation)    
      
      text = 'virus: ' + str(Blue.virus_eat)
      blueInfo = font.render(text, 0, py.Color('black'))
      textLocation = py.Rect(340, 855, WIDTH/5, 70)
      surface.blit(blueInfo, textLocation)   
    
    elif self.view == 'blue':
      # name
      font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 45, True, False)
      
      text = 'blue' if Blue.name is None else Blue.name
      blueInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(10, 837, WIDTH/5, 70)
      surface.blit(blueInfo, textLocation)
      
      text = 'yellow' if Yellow.name is None else Yellow.name
      yellowInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(450, 837, WIDTH/5, 70)
      surface.blit(yellowInfo, textLocation)
      
      # score
      font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 40, True, False)
      
      text = 'link: ' + str(Blue.link_eat)      
      blueInfo = font.render(text, 0, py.Color('black'))
      textLocation = py.Rect(190, 825, WIDTH/5, 70)
      surface.blit(blueInfo, textLocation)    
      
      text = 'virus: ' + str(Blue.virus_eat)
      blueInfo = font.render(text, 0, py.Color('black'))
      textLocation = py.Rect(190, 855, WIDTH/5, 70)
      surface.blit(blueInfo, textLocation)  
      
      text = 'link: ' + str(Yellow.link_eat)
      yellowInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(340, 825, WIDTH/5, 70)
      surface.blit(yellowInfo, textLocation)
      
      text = 'virus: ' + str(Yellow.virus_eat)
      yellowInfo = font.render(text, 1, py.Color('black'))
      textLocation = py.Rect(340, 855, WIDTH/5, 70)
      surface.blit(yellowInfo, textLocation)
   
  def drawPiece(self, surface, row, col, piece, drawStatus=False):
    if self.view == 'god': img = py.image.load(piece.texture)
    elif piece.checked or piece.color == self.view: img = py.image.load(piece.texture)
    elif piece.color != self.view and piece.color == 'yellow': img = py.image.load(Unknown('yellow').texture)
    elif piece.color != self.view and piece.color == 'blue': img = py.image.load(Unknown('blue').texture)
    
    img_center = 28+col*SQ_SIZE + SQ_SIZE//2, 95+row*SQ_SIZE + SQ_SIZE//2
    piece.texture_rect = img.get_rect(center=img_center)
    surface.blit(img, piece.texture_rect)
    
    if drawStatus:
      if piece.lb:
        surface.blit(IMAGES['LB'], (38+col*SQ_SIZE, 103.5+row*SQ_SIZE))
      if piece.checked:
        surface.blit(IMAGES['checked'], (38+col*SQ_SIZE, 103.5+row*SQ_SIZE))
  
  def drawFW(self, surface, row, col, fw):
    img = py.image.load(fw.texture)
    surface.blit(img, (32.5+col*SQ_SIZE, 100+row*SQ_SIZE))
    surface.blit(IMAGES['shield'], (23+col*SQ_SIZE, 86+row*SQ_SIZE))
      
  def drawSquare(self, surface, exceptPiece: object=None, Srow=None, Scol=None):
    if self.view == 'god' or self.view == 'yellow':
      board = self.board.squares
      bServerRow = YSERVERROL
      yServerRow = BSERVERROL
    elif self.view == 'blue':
      board = self.board.blueBoard
      bServerRow = BSERVERROL
      yServerRow = YSERVERROL
    
    # draw yellow pieces in blue server
    if len(self.Blue.serverStack) != 0:
      for y in range(len(self.Blue.serverStack)):
        piece = self.Blue.serverStack[y]
        self.drawPiece(surface, bServerRow, y, piece)
    
    # draw blue pieces in yellow server
    if len(self.Yellow.serverStack) != 0:
      for b in range(len(self.Yellow.serverStack)):
        piece = self.Yellow.serverStack[b]
        self.drawPiece(surface, yServerRow, b, piece)
    
    # draw board
    for row in range(ROWS):
      for col in range(COLS):
        # draw fire wall
        if board[row][col].has_fw():
          fw = board[row][col].fw
          self.drawFW(surface, row, col, fw)
        
        # draw piece
        if board[row][col].has_piece():
          piece = board[row][col].piece
          # draw moving piece
          if piece == exceptPiece: self.drawPiece(surface, Srow, Scol, exceptPiece, drawStatus=True)
          
          # draw normal pieces
          else: self.drawPiece(surface, row, col, piece, drawStatus=True)

  def setSkillAlpha(self):
    if self.players[0].skills['lb']['used']: IMAGES['yellow_lb'].set_alpha(100)
    else: IMAGES['yellow_lb'].set_alpha(255)
    
    if self.players[0].skills['fw']['used']: IMAGES['yellow_fw'].set_alpha(100)
    else: IMAGES['yellow_fw'].set_alpha(255)
    
    if self.players[1].skills['lb']['used']: IMAGES['blue_lb'].set_alpha(100)
    else: IMAGES['blue_lb'].set_alpha(255)
    
    if self.players[1].skills['fw']['used']: IMAGES['blue_fw'].set_alpha(100)
    else: IMAGES['blue_fw'].set_alpha(255)
  
  def drawSkills(self, surface, Yellow:object, Blue:object):
    self.setSkillAlpha()
    
    if self.view == 'god' or self.view == 'yellow':
      # will display constantly
      surface.blit(IMAGES['blue_fw'], (38+9*SQ_SIZE, 103.5+3*SQ_SIZE))
      surface.blit(IMAGES['blue_lb'], (38+9*SQ_SIZE, 103.5+4*SQ_SIZE))
      
      surface.blit(IMAGES['yellow_lb'], (38+9*SQ_SIZE, 103.5+5*SQ_SIZE))
      surface.blit(IMAGES['yellow_fw'], (38+9*SQ_SIZE, 103.5+6*SQ_SIZE))
      
      if not Yellow.skills['vc']['used']: surface.blit(IMAGES['yellow_vc'], (38+9*SQ_SIZE, 103.5+7*SQ_SIZE))
      if not Yellow.skills['404']['used']: surface.blit(IMAGES['yellow_404'], (38+9*SQ_SIZE, 103.5+8*SQ_SIZE))
      
      if not Blue.skills['vc']['used']: surface.blit(IMAGES['blue_vc'], (38+9*SQ_SIZE, 103.5+2*SQ_SIZE))
      if not Blue.skills['404']['used']: surface.blit(IMAGES['blue_404'], (38+9*SQ_SIZE, 103.5+1*SQ_SIZE))
    
    elif self.view == 'blue':
    # will display constantly
      surface.blit(IMAGES['blue_fw'], (38+9*SQ_SIZE, 103.5+6*SQ_SIZE))
      surface.blit(IMAGES['blue_lb'], (38+9*SQ_SIZE, 103.5+5*SQ_SIZE))
      
      surface.blit(IMAGES['yellow_lb'], (38+9*SQ_SIZE, 103.5+4*SQ_SIZE))
      surface.blit(IMAGES['yellow_fw'], (38+9*SQ_SIZE, 103.5+3*SQ_SIZE))
      
      if not Yellow.skills['vc']['used']: surface.blit(IMAGES['yellow_vc'], (38+9*SQ_SIZE, 103.5+2*SQ_SIZE))
      if not Yellow.skills['404']['used']: surface.blit(IMAGES['yellow_404'], (38+9*SQ_SIZE, 103.5+1*SQ_SIZE))
      
      if not Blue.skills['vc']['used']: surface.blit(IMAGES['blue_vc'], (38+9*SQ_SIZE, 103.5+7*SQ_SIZE))
      if not Blue.skills['404']['used']: surface.blit(IMAGES['blue_404'], (38+9*SQ_SIZE, 103.5+8*SQ_SIZE))
  
  def showMoves(self, surface):
    '''
    show valid moves of a piece when it's clicked
    '''
    if self.clicker.selected_piece:
      piece = self.clicker.piece
      r = self.clicker.initial_row
      c = self.clicker.initial_col
      
      s = py.Surface((PIECE_SIZE, PIECE_SIZE))
      s.set_alpha(100)  # transperancy value -> 0 transparent; 255 opaque
      s.fill(py.Color('white'))
      # loop all valid moves
      for move in piece.moves:
        if move.startRow == r and move.startCol == c:
          if self.view == 'blue': row = self.clicker.convertBlueRow(move.endRow)
          else: row = move.endRow
          surface.blit(s, (32.5+move.endCol*SQ_SIZE, 98+row*SQ_SIZE)) 
    
    if self.displayOption:
      font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 45, True, False)
      
      text = 'swap?'
      blueInfo = font.render(text, 1, py.Color('black'))
      surface.blit(blueInfo, (32.5+3.2*SQ_SIZE, 98+4*SQ_SIZE))
      
      text = 'Yes'
      blueInfo = font.render(text, 1, py.Color('black'))
      surface.blit(blueInfo, (32.5+3*SQ_SIZE, 98+5*SQ_SIZE))
      
      
      text = 'No'
      blueInfo = font.render(text, 1, py.Color('black'))
      surface.blit(blueInfo, (32.5+4*SQ_SIZE, 98+5*SQ_SIZE))
  
  def animateMove(self, surface, move):
    
    if self.view == 'blue': dR = BROW[move.endRow] - BROW[move.startRow]
    else: dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    
    framesPerSquare = 5 # frames to move one squares
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    
    for frame in range(frameCount + 1):
      if self.view == 'blue':
        r, c = (BROW[move.startRow] + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
      else: r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
      
      # draw piece
      self.DrawGameState(surface, move.pieceMoved, r, c)
      
      py.display.flip()
      py.time.Clock().tick(60)
    
  # game method
  def initPiece(self, player: object):
    color = player.color
    pieceInit = player.pieceInit
    i = 0
    for row, col in POS_INIT[color]:
      if pieceInit[i] == 'l':
        self.board.squares[row][col] = Square(row, col, Link(color))
        i += 1
      elif pieceInit[i] == 'v':
        self.board.squares[row][col] = Square(row, col, Virus(color))
        i += 1  
  
  def reset(self, yellow: object, blue: object,
               view: Literal['god', 'yellow', 'blue']='god') -> None:
    yellow.reset()
    blue.reset()
    self.__init__(yellow, blue, view)
    
  def checkGameOver(self):
    yLink = self.Yellow.link_eat + self.Yellow.link_enter
    yVirus = self.Yellow.virus_eat + self.Yellow.virus_enter
    bLink = self.Blue.link_eat + self.Blue.link_enter
    bVirus = self.Blue.virus_eat + self.Blue.virus_enter
    yPieces = len(self.board.getAllyPieces('yellow'))
    bPieces = len(self.board.getAllyPieces('blue'))
    
    if yLink == 4 or bVirus == 4: return self.Yellow.name
    elif bLink == 4 or yVirus == 4: return self.Blue.name
    elif yPieces == 0: return self.Blue.name
    elif bPieces == 0: return self.Yellow.name
    else: return None
  
  def yellowToMove(self):
    return True if self.player.color == 'yellow' else False
  
  def switchPlayer(self):
    self.player = self.players[(self.turn + 1) % 2]
    self.enemy = self.players[self.turn % 2]
  
  def updateInfo(self):
    self.animate = False
    
    self.moveMade = False

    self.whichSkill = None
    self.useSkill = False
    self.skillUsed = False
    self.undoSkill = False
   
  def nextPlayer(self):
    self.turn += 1
    self.switchPlayer()
    # print('switch to', self.player.name)
    
    self.updateInfo()
    
    # print(self.gamelog)
  
  def revert(self):
    self.turn -= 1
    self.switchPlayer()
    # print('revert to', self.player.name)
    
    self.updateInfo()
    
    # print(self.gamelog)
  
  def undo(self):
    if len(self.gamelog) != 0:
      last_key = list(self.gamelog)[-1]
      last_value = self.gamelog[last_key]
      
      # uninstall terminal card
      if last_value in SKILLS:
        self.skill.undoSkill(self)
      
      # undo move
      elif last_value not in SKILLS:
        self.board.undoMove(self)
        self.message = self.player.name + ' Undo move'
        self.gameOver = False
  
  def nextView(self, lst: list, element: str):
   idx = lst.index(element)
   if idx + 1 >= len(lst): return lst[0]
   else: return lst[idx +1]
  
  # other method
  def getValidMoves(self) -> list:
    '''
    get valid moves for all ally pieces
    '''
    moves = []
    for r in range(len(self.board.squares)):
      for c in range(len(self.board.squares[r])):
        if self.board.squares[r][c].piece is not None:
          turn = self.board.squares[r][c].piece.color
          # print(turn, self.next_player)
          if turn == self.player.color:
            self.board.calc_moves(self.board.squares[r][c].piece, r, c)
            for move in self.board.squares[r][c].piece.moves: moves.append(move)
    #           print(move.moveID)
    # print('No of valid moves:', len(moves))
    return moves
  
  def clearValidMoves(self):
    '''
    must use after `getValidMoves` used
    '''
    for r in range(len(self.board.squares)):
      for c in range(len(self.board.squares[r])):
        if self.board.squares[r][c].piece is not None:
          turn = self.board.squares[r][c].piece.color
          if turn == self.player.color:
            self.board.squares[r][c].piece.clear_moves()
