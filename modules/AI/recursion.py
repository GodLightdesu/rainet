import random
import numpy as np

# from typing import Literal
from ..player import Player
from ..const import *
from ..utils import *

class Recursion(Player):
  
  def __init__(self, color: str, pieceInit: str, name='Null', depth: int=7) -> None:
    super().__init__(color, pieceInit, name)
    self.isHuman = False
    self.DEPTH = depth
    self.bestMove = None
    self.counter = 0 
    
  def reset(self):
    self.__init__(self.color, self.pieceInit, self.name, self.DEPTH)
  
  def randomPiece(self, allyPieces, virusProb):
    linkProb = 1 - virusProb
    # # count no of link and virus
    v, l = 0, 0
    for i in range(len(allyPieces)):
      if allyPieces[i].name == 'virus': v += 1
      if allyPieces[i].name == 'link': l += 1
    
    # set probability of each piece being chosen
    pieceProb = []
    for i in range(len(allyPieces)):
      # 40% chance to pick virus
      if allyPieces[i].name == 'virus': pieceProb.append(virusProb/v)
      # 60% chance to pick link
      elif allyPieces[i].name == 'link': pieceProb.append(linkProb/l)
    pieceProb = np.array(pieceProb)
    pieceProb /= pieceProb.sum()
    # print(game.turn, '|', game.player.name, '|', len(allyPieces), '|', len(pieceProb), pieceProb)
    
    # random choose a piece
    piece = np.random.choice(allyPieces, p=pieceProb)
    
    return piece
  
  def findRandomMove(self, validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
  
  def decision(self, game: object, validMoves: list, allyPiece: list):
    decisions = {
      'move': None,
      'skill': None
    }
    return decisions
  
  def findBestMove(self, game):
    self.counter = 0 
    # score = self.Search(game, self.DEPTH)
    score = self.SearchAlphaBeta(game, self.DEPTH, alpha=-WINNINGSCORE, beta=WINNINGSCORE)
    print('-------------------------------------')
    print('Depth:', self.DEPTH)
    print('Evaluated:', self.counter, 'moves')
    print('bestMove:', self.bestMove.moveID)
    print(self.name + '\'s score :', score)
    print('-------------------------------------')
    return score
    
  def selfToMove(self, game):
    return self.color == game.player.color
  
  def Search(self, game, depth: int):
    self.counter += 1
    if depth == 0: return scoreBoard(game)
    maxScore = -20
    
    validMoves = game.getValidMoves()
    random.shuffle(validMoves)
    for move in validMoves:
      # make move
      piece = move.pieceMoved
      game.board.move(game, piece, move)
      game.clearValidMoves()
      # search next game state
      score = -self.Search(game, depth - 1)
      if score > maxScore:
        maxScore = score
        if depth == self.DEPTH:
          self.bestMove = move
          print(game.player.name + ':', move.moveID, score)
      game.board.undoMove(game)
    
    game.clearValidMoves()
    return maxScore
  
  def SearchAlphaBeta(self, game, depth: int, alpha: int, beta: int):
    self.counter += 1
    if depth == 0: return scoreBoard(game)
    maxScore = -WINNINGSCORE
    
    validMoves = game.getValidMoves()
    random.shuffle(validMoves)
    for move in validMoves:
      # make move
      piece = move.pieceMoved
      game.board.move(game, piece, move)
      game.clearValidMoves()
      # search next game state
      score = -self.SearchAlphaBeta(game, depth - 1, -beta, -alpha)
      if score > maxScore:
        maxScore = score
        if depth == self.DEPTH:
          self.bestMove = move
          print(game.player.name + ':', move.moveID, score)
      game.board.undoMove(game)
      
      # pruning
      if maxScore > alpha:
        alpha = maxScore
      if alpha >= beta:
        break
      
    game.clearValidMoves()
    return maxScore