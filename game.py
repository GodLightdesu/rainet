import pygame as py
import os

from player import Player
from board import Board

from const import *
from square import *
from piece import *

class Game:
  
  def __init__(self, yellowInit, blueInit, yellowID=None, blueID=None) -> None:
    self.board = Board()
    
    # game init
    self.message = ''
    self.gameOver = False
    self.turn = 1
    self.gamelog = []
    
    self.next_player = 'yellow'
    self.humanMove = True
    
    self.Yellow = Player('yellow', yellowID)
    self.Blue = Player('blue', blueID)
    self.players = [self.Yellow, self.Blue]
    self.player = self.players[(self.turn + 1) % 2]
    self.enemy = self.players[self.turn % 2]
    
    # move init
    self.moveMade = False
    
    # skill init
    self.whichSkill = None
    self.useSkill = False
    self.skillUsed = False
    self.undoSkill = False
    
    # piece init
    i = 0
    for row, col in POS_INIT['yellow']:
      if yellowInit[i] == 'l':
        self.board.squares[row][col] = Square(row, col, Link('yellow'))
        i += 1
      elif yellowInit[i] == 'v':
        self.board.squares[row][col] = Square(row, col, Virus('yellow'))
        i += 1
    
    i = 0
    for row, col in POS_INIT['blue']:
      if blueInit[i] == 'l':
        self.board.squares[row][col] = Square(row, col, Link('blue'))
        i += 1
      elif blueInit[i] == 'v':
        self.board.squares[row][col] = Square(row, col, Virus('blue'))
        i += 1  
    
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
    IMAGES['target'] = py.transform.scale(py.image.load('assets/images/' + 'target' + '.png'), (56, 56))
    
    # init skills' image
    for skill in SKILLS:
      IMAGES['blue_' + skill] = py.transform.scale(py.image.load('assets/images/blue_' + skill + '.png'), (PIECE_SIZE, PIECE_SIZE))
      IMAGES['yellow_' + skill] = py.transform.scale(py.image.load('assets/images/yellow_' + skill + '.png'), (PIECE_SIZE, PIECE_SIZE))
      
  # display method
  def DrawGameState(self, surface, view='god'):
    self.drawBoard(surface, view)
    self.drawGameInfo(surface, self.Yellow, self.Blue)
    self.drawSquare(surface, view)
    self.drawSkills(surface, self.Yellow, self.Blue)
  
  def drawBoard(self, surface, view):
    surface.blit(IMAGES['BG'], (0, 0))
    if view == 'god'or view == 'yellow':
      surface.blit(IMAGES['y_top'], (0, 0))
      surface.blit(IMAGES['y_board'], (0, 72))
      surface.blit(IMAGES['y_bottom'], (0, 817))
    elif view == 'blue':
      surface.blit(IMAGES['b_top'], (0, 0))
      surface.blit(IMAGES['b_board'], (0, 71))
      surface.blit(IMAGES['b_bottom'], (0, 817))
      
  def drawText(self, surface, text):
    font = py.font.SysFont("font/SoukouMincho.ttf", 40, False, False)
    # font = py.font.SysFont("arial", 40, False, False)
    textObject = font.render(text, 0, py.Color('white'))
    textLocation = py.Rect(0, 0, WIDTH, 70).move(WIDTH/2 - textObject.get_width()/2, 70/2 - textObject.get_height()/2)
    surface.blit(textObject, textLocation)
    
  def drawGameInfo(self, surface, Yellow, Blue):
    font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 45, True, False)
    
    text = 'yellow' if Yellow.name is None else Yellow.name
    yellowInfo = font.render(text, 0, py.Color('black'))
    textLocation = py.Rect(5, 837, WIDTH/5, 70)
    surface.blit(yellowInfo, textLocation)
    
    text = 'blue' if Blue.name is None else Blue.name
    blueInfo = font.render(text, 0, py.Color('black'))
    textLocation = py.Rect(530, 837, WIDTH/5, 70)
    surface.blit(blueInfo, textLocation)
    
    font = py.font.SysFont(os.path.join('assets/font/SoukouMincho.ttf'), 40, True, False)
  
    text = 'link: ' + str(Yellow.link_eat) + ' virus: ' + str(Yellow.virus_eat)
    
    yellowInfo = font.render(text, 0, py.Color('black'))
    textLocation = py.Rect(110, 840, WIDTH/5, 70)
    surface.blit(yellowInfo, textLocation)
    
    text = 'link: ' + str(Blue.link_eat) + ' virus: ' + str(Blue.virus_eat)
    
    yellowInfo = font.render(text, 0, py.Color('black'))
    textLocation = py.Rect(330, 840, WIDTH/5, 70)
    surface.blit(yellowInfo, textLocation)    
    
  def drawSquare(self, surface, view):
    # god view or yellow view
    if view == 'god':
      # draw yellow pieces in server
      if len(self.Yellow.serverStack) != 0:
        for y in range(len(self.Yellow.serverStack)):
          piece = self.Yellow.serverStack[y]

          img = py.image.load(piece.texture)
          img_center = 28 + y * SQ_SIZE + SQ_SIZE//2, 95+YSERVERROL*SQ_SIZE + SQ_SIZE//2
          piece.texture_rect = img.get_rect(center=img_center)
          surface.blit(img, piece.texture_rect)
      
      # draw blue pieces in server
      if len(self.Blue.serverStack) != 0:
        for b in range(len(self.Blue.serverStack)):
          piece = self.Blue.serverStack[b]
          
          img = py.image.load(piece.texture)
          img_center = 28 + b * SQ_SIZE + SQ_SIZE//2, 95+BSERVERROL*SQ_SIZE + SQ_SIZE//2
          piece.texture_rect = img.get_rect(center=img_center)
          surface.blit(img, piece.texture_rect)
      
      # draw board
      for row in range(ROWS):
        for col in range(COLS):
          # draw fire wall
          if self.board.squares[row][col].has_fw():
            fw = self.board.squares[row][col].fw
            img = py.image.load(fw.texture)
            surface.blit(img, (32.5+col*SQ_SIZE, 100+row*SQ_SIZE))
            surface.blit(IMAGES['shield'], (23+col*SQ_SIZE, 86+row*SQ_SIZE))
          
          # draw piece
          if self.board.squares[row][col].has_piece():
            piece = self.board.squares[row][col].piece

            img = py.image.load(piece.texture)
            img_center = 28+col*SQ_SIZE + SQ_SIZE//2, 95+row*SQ_SIZE + SQ_SIZE//2
            piece.texture_rect = img.get_rect(center=img_center)
            surface.blit(img, piece.texture_rect)
            
            if piece.lb:
              surface.blit(IMAGES['LB'], (38+col*SQ_SIZE, 103.5+row*SQ_SIZE))
            if piece.checked:
              surface.blit(IMAGES['checked'], (38+col*SQ_SIZE, 103.5+row*SQ_SIZE))

  def drawSkills(self, surface, Yellow, Blue):
    # will display constantly
    surface.blit(IMAGES['blue_fw'], (38+9*SQ_SIZE, 103.5+3*SQ_SIZE))
    surface.blit(IMAGES['blue_lb'], (38+9*SQ_SIZE, 103.5+4*SQ_SIZE))
    
    surface.blit(IMAGES['yellow_lb'], (38+9*SQ_SIZE, 103.5+5*SQ_SIZE))
    surface.blit(IMAGES['yellow_fw'], (38+9*SQ_SIZE, 103.5+6*SQ_SIZE))
    
    if not Yellow.skills['vc']['used']: surface.blit(IMAGES['yellow_vc'], (38+9*SQ_SIZE, 103.5+7*SQ_SIZE))
    if not Yellow.skills['404']['used']: surface.blit(IMAGES['yellow_404'], (38+9*SQ_SIZE, 103.5+8*SQ_SIZE))
    
    if not Blue.skills['vc']['used']: surface.blit(IMAGES['blue_vc'], (38+9*SQ_SIZE, 103.5+2*SQ_SIZE))
    if not Blue.skills['404']['used']: surface.blit(IMAGES['blue_404'], (38+9*SQ_SIZE, 103.5+1*SQ_SIZE))
    
  # game method
  def reset(self, yellowInit, blueInit, yellowID, blueID):
    self.__init__(yellowInit, blueInit, yellowID, blueID)
    
  def checkGameOver(self):
    yLink = self.Yellow.link_eat + self.Yellow.link_enter
    yVirus = self.Yellow.virus_eat + self.Yellow.virus_enter
    bLink = self.Blue.link_eat + self.Blue.link_enter
    bVirus = self.Blue.virus_eat + self.Blue.virus_enter
    
    if yLink == 4 or bVirus == 4:
      if self.Yellow.name is not None:  return self.Yellow.name
      else: return self.Yellow.color
    elif bLink == 4 or yVirus == 4:
      if self.Blue.name is not None:  return self.Blue.name
      else: return self.Blue.color
    else: return None
    
  def switch_player(self):
    self.turn += 1
    self.player = self.players[(self.turn + 1) % 2]
    self.enemy = self.players[self.turn % 2]
    # print(self.player.color)
    
    self.moveMade = False

    self.whichSkill = None
    self.useSkill = False
    self.skillUsed = False
    self.undoSkill = False