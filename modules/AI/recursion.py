import random
import math
import numpy as np

from typing import Literal
from ..player import Player
from ..const import *

class Recursion(Player):
  
  def __init__(self, color: str, pieceInit: str, name='Null', depth: int=2) -> None:
    super().__init__(color, pieceInit, name)
    self.isHuman = False
    self.depth = depth
    self.bestMove = None
    
  def reset(self):
    self.__init__(self.color, self.pieceInit, self.name)
  
  def findRandomMove(self, validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
  
  def decision(self, game: object, validMoves: list, allyPiece: list):
    decisions = {
      'move': None,
      'skill': None
    }
    return decisions
  
  # def findBestMove(self, game, validMoves, depth):
  #   self.bestMove = self.Search(game, validMoves, depth)
  
  def selfToMove(self, game):
    return self.color == game.player.color
  
  def Search(self, game, depth: int):
    if depth == 0: return 0
    maxScore = 0.5 # target score
    
    validMoves = game.getValidMoves()
    for move in validMoves:
      piece = move.pieceMoved
      game.board.move(game, piece, move)
      score = -self.scoreBoard(game)
      print(move.moveID, '->', score, maxScore, score > maxScore)
      
      if score > maxScore:
        maxScore = score
        self.bestMove = move
      
      game.board.undoMove(game)
    game.clearValidMoves()
      
  def scoreBoard(self, game):
    '''
    `Current player view`
    '''
    winner = game.checkGameOver()
    if winner is not None and winner == self.name: return 100
    elif winner is not None and winner != self.name: return -100
    
    return self.scoreMaterial(game)
  
  def scoreMaterial(self, game):
    '''
    information can be collected
    - self piece enter server
    - self piece is captured?
    - enemy piece enter server?
    '''
    enemy_Link_eat = game.enemy.link_eat
    enemy_Virus_eat =  game.enemy.virus_eat
    # only know the total no of entered piece
    enemyEnter =  game.enemy.link_enter +  game.enemy.virus_enter
   
    score = 0
    
    score += PIECEVALUE['unknown'] * (game.player.virus_eat + game.player.link_eat) / 2
    
    # virus should not enter server
    score -= PIECEVALUE['virus'] * 2 * game.player.virus_enter
    score += PIECEVALUE['link'] * game.player.link_enter
    
    # lose combat power to capture piece
    score -= PIECEVALUE['virus'] / 1.5 * enemy_Virus_eat
    score -= PIECEVALUE['link'] * 2 * enemy_Link_eat
    
    # assume enemy always enter Link
    score -= PIECEVALUE['link'] * enemyEnter
    
    return score
  
  def Distance(self, game, startRow, startCol, targetRow, targetCol):
    if game.view == 'blue': dR = BROW[targetRow] - startRow
    else: dR = targetRow - startRow
    dC = targetCol - startCol
    
    return int(math.sqrt(dR**2 + dC**2))
  
  def distanceToExit(self, game, startRow, startCol):
    Exit1, Exit2 = EXITPOS[self.color]
    row0, col0 = Exit1  # col 3
    row1, col1 = Exit2  # col 4
    # check Exit1
    if startCol <= col0:
      if game.view == 'blue': dR = BROW[row0] - startRow
      else: dR = row0 - startRow
      dC = col0 - startCol
    # check Exit2
    elif startCol >= col1:
      if game.view == 'blue': dR = BROW[row1] - startRow
      else: dR = row1 - startRow
      dC = col1 - startCol
    
    return int(math.sqrt(dR**2 + dC**2))
  
  