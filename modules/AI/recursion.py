import random
import timeit
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
  
  def randomEnePiece(self, enemyPieces: list) -> object:
    Prob = 1 / len(enemyPieces)
    pieceProb = [Prob for i in range(len(enemyPieces))]
    piece = np.random.choice(enemyPieces, p=pieceProb)
    return piece
  
  def findRandomMove(self, validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
  
  def decision(self, game: object):
    # collect information for AI decision
    allyPieces = game.board.getAllyPieces(game.player.color)
    enemyPieces =  game.board.getAllyPieces(game.enemy.color)
    
    # make decision
    decisions = {
      'move': None,
      'skill': None
    }
    actions = ['lb', 'fw', 'vc', '404', 'move']
    lbProb = 0.75 if not self.skills['lb']['used'] else 0.00
    fwProb = 0.0
    vcProb = 0.1
    # 404
    checkedPiece = None
    swap = np.random.choice([True, False], p=[0.5, 0.5])
    for piece in allyPieces:
      if piece.checked: 
        checkedPiece = piece
        _404Prob = 0.1
      else: _404Prob = 0.0
    # move
    moveProb = 1 - lbProb - fwProb - vcProb - _404Prob
    actionProb = [lbProb, fwProb, vcProb, _404Prob, moveProb]
    actions = np.random.choice(actions, p=actionProb)

    
    if actions == 'lb': # lb
      piece = self.randomPiece(allyPieces, 0.7)
      decisions['skill'] = ['lb', piece]
   
    elif actions == 'vc':  # vc
      piece = self.randomEnePiece(enemyPieces)
      decisions['skill'] = ['vc', piece]
    
    elif actions == '404' and checkedPiece is not None:  # 404
      swapPiece = self.randomEnePiece([piece for piece in allyPieces if piece != checkedPiece])
      decisions['skill'] = ['404', checkedPiece, swapPiece, swap]
    
    else: # move
      game.player.findBestMove(game)
      validMoves = game.getValidMoves()
      if self.bestMove is None: decisions['move'] = self.findRandomMove(validMoves)
      else: decisions['move'] = self.bestMove
      # check if there is a link can enter exit
      for move in validMoves:
        # there is a link can enter exit
        if move.endsq.is_ally_exit(self.color) and move.pieceMoved.name == 'link' and len(allyPieces) != 0: 
          decisions['move'] =  move
      game.clearValidMoves()
      game.player.bestMove = None
    
    return decisions
  
  def findBestMove(self, game):
    self.counter = 0
    start = timeit.default_timer()
    # score = self.Search(game, self.DEPTH)
    score = self.SearchAlphaBeta(game, self.DEPTH, alpha=float('-inf'), beta=float('inf'))
    stop = timeit.default_timer()
    print('-------------------------------------')
    print('Depth:', self.DEPTH)
    print(f'Runtime: {round(stop-start, 4)} s')
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
      # undo move
      game.board.undoMove(game)
      
      if score > maxScore:
        maxScore = score
        if depth == self.DEPTH:
          self.bestMove = move
          print(game.player.name + ':', move.moveID, score)
    game.clearValidMoves()
    return maxScore
  
  def SearchAlphaBeta(self, game, depth: int, alpha: int, beta: int):
    self.counter += 1
    if depth == 0: return scoreBoard(game)
    
    validMoves = game.getValidMoves()
    random.shuffle(validMoves)
    for move in validMoves:
      # make move
      piece = move.pieceMoved
      game.board.move(game, piece, move)
      game.clearValidMoves()
      # search next game state
      score = -self.SearchAlphaBeta(game, depth - 1, -beta, -alpha)
      # undo move
      game.board.undoMove(game)
      game.clearValidMoves()
      # check best move
      if score >= beta:
        if depth == self.DEPTH:
          self.bestMove = move
          print(game.player.name + ':', move.moveID, score)
        return beta
      # find a new best move
      if score > alpha:
        alpha = score
        if depth == self.DEPTH:
          self.bestMove = move
          print(game.player.name + ':', move.moveID, score)
    return alpha