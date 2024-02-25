from re import T
from move import Move

from const import *
from square import *
from piece import *
import copy

class Board:
  
  def __init__(self) -> None:
    self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for row in range(ROWS)]
    self.moveLog = []
    self._create()
    self._add_Piece('yellow')
    self._add_Piece('blue')
    
    self.blueBoard = copy.copy(self.squares)
    self.blueBoard.reverse()
  
  def isEnterServer(self, player: object, endSq: object):
    return endSq.is_ally_exit(player.color)
  
  def enterServer(self, player: object, piece: object):
    if piece.lb:
      player.skills['lb']['used'] = False

    # non lb piece
    if piece.name == 'link':  player.link_enter += 1
    elif piece.name == 'virus': player.virus_enter += 1
    
    player.serverStack.append(piece)
    
  def leaveServer(self, player: object):
    piece = player.serverStack.pop()
    
    if piece.lb:
      player.skills['lb']['used'] = True

    # non lb piece
    if piece.name == 'link':  player.link_enter -= 1
    elif piece.name == 'virus': player.virus_enter -= 1
  
  def capturePiece(self, player: object, enemy: object, enemyPiece: object):
    # lb piece
    if enemyPiece.lb:
      enemy.skills['lb']['used'] = False

    # non lb piece
    if enemyPiece.name == 'link':  player.link_eat += 1
    elif enemyPiece.name == 'virus': player.virus_eat += 1
  
  def unCapturePiece(self, player: object, enemy: object, enemyPiece: object):
    # lb piece
    if enemyPiece.lb:
      enemy.skills['lb']['used'] = True

    # non lb piece
    if enemyPiece.name == 'link':  player.link_eat -= 1
    elif enemyPiece.name == 'virus': player.virus_eat -= 1
    
  def add_moveToPiece(self, piece: object, startRow: int, startCol: int, endRow: int, endCol: int):
    # create asquares for the new move
    startSq = self.squares[startRow][startCol]
    endSq = self.squares[endRow][endCol]
    # create new move
    move = Move(startSq, endSq)
    # apeend new valid move
    piece.add_move(move)
  
  # move method
  def move(self, player: object, enemy: object, piece: object, move: object):
    startsq = move.startsq
    endsq = move.endsq
    
    startPiece = self.squares[startsq.row][startsq.col].piece
    endPiece = self.squares[endsq.row][endsq.col].piece
    
    # game info update
    if self.isEnterServer(player, endsq): # enter server
      self.enterServer(player, piece)
    
    if endsq.has_enemy_piece(player.color): # end square is enemy piece
      self.capturePiece(player, enemy, endPiece)
      
    # console board move update
    self.squares[startsq.row][startsq.col].piece = None
    
    if not self.isEnterServer(player, endsq):  self.squares[endsq.row][endsq.col].piece = piece
    else: self.squares[endsq.row][endsq.col].piece = None
    
    # print(self.squares[startsq.row][startsq.col].piece)
    # print(self.squares[endsq.row][endsq.col].piece)

    # move
    piece.move = True
    
    # clear valid moves
    piece.clear_moves()
    
    # set last move
    # player.moveLog.append(move)
    # self.moveLog.append(move)

  def undoMove(self, game: object):
    if len(game.movelog) != 0:
      game.gamelog.pop(list(game.gamelog)[-1])
      move = game.movelog.pop(list(game.movelog)[-1])
      game.revert()
      
      self.squares[move.startRow][move.startCol].piece = move.pieceMoved
      self.squares[move.endRow][move.endCol].piece = move.pieceCaptured 
      
      endSq = self.squares[move.endRow][move.endCol]
      
      # update info
      if self.isEnterServer(game.player, endSq):
        self.leaveServer(game.player)
      elif endSq.has_enemy_piece(game.player.color):
        self.unCapturePiece(game.player, game.enemy, endSq.piece)
  
  def validMove(self, piece: object, move: object):
    return move in piece.moves
  
  def calc_moves(self, piece: object, startRow: int, startCol: int):
    '''
    Calculate all the possible (valid) moves of an specific piece on a specific position
    '''
    
    def isValidMove(endRow: int, endCol: int) -> bool:
      '''
      True
      - empty square -> True
      - enenmy piece -> True  -> capture piece
      - server       -> True  -> enter server
      
      False
      - self piece   -> False
      - enemy FW     -> False
      - boundary     -> False
      - enemy server -> False
      '''
      if 0 <= endRow < 10 and 0 <= endCol < 8:
        if self.squares[endRow][endCol].can_pass(piece.color): valid = True
        else: valid = False
      else: valid = False
      return valid
    
    def nonLB_move():
      possible_moves = [
        (startRow -1, startCol), 
        (startRow +1, startCol), 
        (startRow, startCol -1), 
        (startRow, startCol +1)
      ]
      
      for possible_move in possible_moves:
        endRow, endCol = possible_move
        if isValidMove(endRow, endCol):
          self.add_moveToPiece(piece, startRow, startCol, endRow, endCol)
    
    def LB_move():
      possible_moves = [(startRow-2, startCol), (startRow+2, startCol), (startRow, startCol-2), (startRow, startCol+2), 
                        (startRow-1, startCol+1), (startRow+1, startCol+1), (startRow+1, startCol-1),  (startRow-1, startCol-1)]
    
      check = {
        (startRow -2, startCol) : [(startRow -1, startCol)],
        (startRow +2, startCol) : [(startRow +1, startCol)], 
        (startRow, startCol -2) : [(startRow, startCol -1)], 
        (startRow, startCol +2) : [(startRow, startCol +1)], 
        (startRow -1, startCol +1) : [(startRow -1, startCol), (startRow, startCol +1)], 
        (startRow +1, startCol +1) : [(startRow +1, startCol), (startRow, startCol +1)], 
        (startRow +1, startCol -1) : [(startRow +1, startCol), (startRow, startCol -1)], 
        (startRow -1, startCol -1) : [(startRow -1, startCol), (startRow, startCol -1)]
      }
      
      for possible_move in possible_moves:
        # vertival or horizontal move
        if len(check[possible_move]) == 1:
          eRow, eCol = check[possible_move][0]
          eSq = self.squares[eRow][eCol]
          if isValidMove(eRow, eCol):
            self.add_moveToPiece(piece, startRow, startCol, eRow, eCol)
            
            endRow, endCol = possible_move
            if isValidMove(endRow, endCol) and not eSq.isBlocked(piece.color):
              self.add_moveToPiece(piece, startRow, startCol, endRow, endCol)
        
        # diagonal move
        elif len(check[possible_move]) == 2:
          blocked = 0 # max 2 cause only check 2 dir
          # count no of blocked
          for check_move in check[possible_move]:    
            eRow, eCol = check_move
            eSq = self.squares[eRow][eCol]

            if eSq.isBlocked(piece.color):
              blocked += 1
          
          # print(possible_move, blocked)
          
          # has path to move  
          if blocked <= 1:
            endRow, endCol = possible_move
            # print(self.squares[endRow][endCol])
            if isValidMove(endRow, endCol):
              self.add_moveToPiece(piece, startRow, startCol, endRow, endCol)
    
    # lb piece
    if piece.lb: LB_move()
    # non lb piece
    else: nonLB_move()
    
  # other method
  def onBoard(self, row, col) -> bool:
    return 0 <= row <= 9 and 0 <= col <= 7
  
  def printboard(self, board):
    for row in range(ROWS):
      for col in range(COLS):
        if board[row][col].boundary:
          print('#', end=' ')
          continue
        if board[row][col].piece is not None:
          print(board[row][col].piece.name[0], end=' ')
        else: print('-', end=' ')
      print()
  
  def printBoard(self, color: str='yellow'):
    if color == 'yellow':
      self.printboard(self.squares)
    elif color == 'blue':
      self.printboard(self.blueBoard)
  
  def getLBpiecePos(self, color):
    for row in range(ROWS):
      for col in range(COLS):
        if (self.squares[row][col].piece is not None and 
            self.squares[row][col].piece.lb and 
            self.squares[row][col].piece.color == color):
          return row, col
  
  # private method (_methodName)
  def _create(self):
    # board
    for row in range(ROWS):
      for col in range(COLS):
        self.squares[row][col] = Square(row, col)
    
    # Exit
    for color in EXITPOS:
      for row, col in EXITPOS[color]:
        self.squares[row][col] = Square(row, col, exit=Exit(color))
        
    # Boundary
    for row, col in BOUNDARY_POS:
      self.squares[row][col].boundary = True
        
  def _add_Piece(self, color: str):
    for row, col in POS_INIT[color]:
      # init all pieces to unknown first
      self.squares[row][col] = Square(row, col, Unknown(color))