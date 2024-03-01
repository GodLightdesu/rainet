import math
import random
from .const import *

def Distance(game, startRow, startCol, targetRow, targetCol):
  if game.view == 'blue': dR = BROW[targetRow] - startRow
  else: dR = targetRow - startRow
  dC = targetCol - startCol
  
  return int(math.sqrt(dR**2 + dC**2))

def distanceToExit(game, color, startRow, startCol):
  Exit1, Exit2 = EXITPOS[color]
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

def scoreBoard(game):
  '''
  `Current player view`
  '''
  # it will be cheating that will know whether the piece is virus
  # winner = game.checkGameOver()
  # if winner is not None and winner == game.player.name: return WINNINGSCORE
  # elif winner is not None and winner != game.enemy.name: return -WINNINGSCORE
  enemyPieces = len(game.board.getAllyPieces(game.enemy.color))
  allyPieces = len(game.board.getAllyPieces(game.player.color))
  if enemyPieces == 0: return WINNINGSCORE
  elif allyPieces == 0: return -WINNINGSCORE
  
  return scoreMaterial(game)

def scoreMaterial(game):
  '''
  information can be collected
  - self piece enter server
  - self piece is captured?
  - enemy piece enter server?
  '''
  score = 0
  
  allyLink, allyVirus = 0, 0
  allyPieces = game.board.getAllyPieces(game.player.color)
  enemyPieces = game.board.getAllyPieces(game.enemy.color)
  # assume enemy will not enter virus
  # enemyLink = 4 - game.player.link_eat -. round((game.enemy.link_enter + game.enemy.virus_enter) / 2)
  # if enemyLink == 0 and game.player.link_eat == 4: return WINNINGSCORE0
  allyEat = (game.player.link_eat + game.player.virus_eat)
  
  if game.enemy.virus_eat == 4: return WINNINGSCORE
  elif game.enemy.link_eat == 4: return -WINNINGSCORE
  
  # pieces on board
  for piece in allyPieces:
    if piece.name == 'link': allyLink += 1
    elif piece.name == 'virus': allyVirus += 1
  score += allyLink * PIECEVALUE['link']
  score += allyVirus * PIECEVALUE['virus']
  
  for piece in enemyPieces:
    if piece.checked: score -= PIECEVALUE[piece.name]
    else: score -= PIECEVALUE['unknown']
  
  # pieces ate (will cause cheating?)
  score -= (PIECEVALUE['link'] * game.enemy.link_eat)/10
  score += (PIECEVALUE['virus'] * game.enemy.virus_eat)/10
  
  # score += PIECEVALUE['unknown'] * 10 * (game.player.link_eat + game.player.virus_eat)
  
  # pieces in server
  # print(game.enemy.name + ' serverStack:', end=' ')
  for piece in game.enemy.serverStack:
    # print(piece.name, end=' ')
    if piece.name == 'link': score += PIECEVALUE['link']
    elif piece.name == 'virus': score -= PIECEVALUE['virus'] * 1.5
  # print()
  
  # print(game.player.name + ' serverStack:', end=' ')
  for piece in game.player.serverStack:
    # print(piece.name, end=' ')
    if piece.checked and piece.name == 'virus': score += PIECEVALUE['virus'] * 1.5
    # assume enemy will enter link
    else: score -= PIECEVALUE['link']
  # print()
  
  # bouns of link's dis to exit
  for piece in allyPieces:
    # if piece.name == 'link':
    startRow, startCol = game.board.findPiecePos(piece)
    if game.view == 'blue': startRow = BROW[startRow]
    dis = distanceToExit(game, game.player.color, startRow, startCol)
    score += (10 - dis)
  
  
  random.shuffle(enemyPieces)
  for piece in enemyPieces:
    startRow, startCol = game.board.findPiecePos(piece)
    if game.view == 'blue': startRow = BROW[startRow]
    dis = distanceToExit(game, game.enemy.color, startRow, startCol)
    score -= (10 - dis)
  
  # bouns of virus's dis to enemy pieces
  for piece in allyPieces:
    dMin = 7
    linkFound = False
    # if piece.name == 'virus':
    startRow, startCol = game.board.findPiecePos(piece)
    for ePiece in enemyPieces:
      endRow, endCol = game.board.findPiecePos(ePiece)
      dst = Distance(game, startRow, startCol, endRow, endCol)
      if dst < dMin: dst = dMin
      if ePiece.checked and ePiece.name == 'link': linkFound = True
    if linkFound: score += (10 - dMin) * 7
    else: score += (10 - dMin) * 4
  
  for piece in enemyPieces:
    dMin = 7
    linkFound = False
    # if piece.name == 'virus':
    startRow, startCol = game.board.findPiecePos(piece)
    for ePiece in allyPieces:
      endRow, endCol = game.board.findPiecePos(ePiece)
      dst = Distance(game, startRow, startCol, endRow, endCol)
      if dst < dMin: dst = dMin
      if ePiece.checked and ePiece.name == 'link': linkFound = True
    if linkFound: score -= (10 - dMin) * 7
    else: score -= (10 - dMin) * 4
  
  # print(game.player.name + '\'s score :', score)
  return score
  