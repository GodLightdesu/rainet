import random
import math
import numpy as np

from typing import Literal
from ..player import Player
from ..const import *

class RamdomMove(Player):
  def __init__(self, color: str, pieceInit: str, name='Random', 
               mode: Literal['Exit', 'Random']='Exit', virusProb=0.3) -> None:
    if virusProb == 1: raise ValueError('virusProb must not equal to 1')
    elif virusProb == 0: raise ValueError('virusProb must not equal to 0')
    
    super().__init__(color, pieceInit, name)
    self.isHuman = False
    self.virusProb = virusProb
    self.linkProb = 1 - virusProb
    self.mode = mode
    
  def reset(self):
    self.__init__(self.color, self.pieceInit, self.name, self.mode, virusProb=self.virusProb)
    
  def setVirusProb(self, virusProb):
    self.virusProb = virusProb
    self.linkProb = 1 - virusProb
  
  def setLinkProb(self, linkProb):
    self.virusProb = 1 - linkProb
    self.linkProb = linkProb
  
  def decision(self, game: object, validMoves: list, allyPiece: list):
    decisions = {
      'move': None,
      'skill': None
    }
    # not used lb, random select a piece to install
    if not self.skills['lb']['used']:
      piece = self.randomPiece(allyPiece, self.virusProb, self.linkProb)
      decisions['skill'] = ['lb', piece]
    
    # used lb, move
    elif self.mode == 'Exit': decisions['move'] = self.findMoveToExit(game, validMoves, allyPiece)
    elif self.mode == 'Random': decisions['move'] = self.findRandomMove(validMoves)
    
    return decisions

  def randomPiece(self, allyPieces, virusProb, linkProb):
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
  
  def findMoveToExit(self, game: object, validMoves: list, allyPiece: list):
    '''
    Random select a piece and move it to exit
    '''
    # find a link can enter exit
    for move in validMoves:
      # there is a link can enter exit
      if move.endsq.is_ally_exit(self.color) and move.pieceMoved.name == 'link': 
        return move
    
    # get all ally piece that have valid moves
    # allyPieces = [piece for piece in allyPieces if len(piece.moves) != 0]
    allyPieces = [piece for piece in allyPiece if len(piece.moves) != 0]
    
    piece = self.randomPiece(allyPiece, self.virusProb, self.linkProb)
    
    # check dis to exit
    closestMove = piece.moves[0]
    row, col = closestMove.endRow, closestMove.endCol
    if game.view == 'blue': row = BROW[row]
    closestDistance = self.distanceToExit(game, row, col)
    
    for move in piece.moves:
      if (move.endsq.is_ally_exit(self.color) and move.pieceMoved.name == 'virus'):
        # print(game.player.name, 'virus to exit')
        continue
      
      row, col = move.endRow, move.endCol
      if game.view == 'blue': row = BROW[row]
      disToExit = self.distanceToExit(game, row, col)
      if disToExit < closestDistance:
        closestMove = move
        closestDistance = disToExit
    
    return closestMove
    
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