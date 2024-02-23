import pygame as py
import os

from player import Player

from const import *

class Game:
  
  def __init__(self, yellowInit, blueInit, yellowID=None, blueID=None) -> None:
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
    
  