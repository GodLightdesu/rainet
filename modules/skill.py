import os
import copy

from .const import *

class FireWall():
  def __init__(self, color: str, used=False, texture=None) -> None:
    self.name = 'fw'
    self.color = color
    self.used = used
    self.texture = texture
    self.set_texture()
  
  def set_texture(self):
    self.texture = os.path.join(
      f'assets/images/{self.color}_{self.name}.png')

class Skill:
  
  def __init__(self) -> None:
    self.swap = None
    
  def undoSkill(self, game: object):
    '''
    undo must after a skill used and it is not reversible
    '''
    
    def undoLB():
      game.message = game.player.name + ' undo LB'
      # print(game.player.name + ' undo LB')
      if game.player.skills['lb']['used']:
        row, col = game.player.skills['lb']['log'].pop()
        game.board.squares[row][col].piece.lb = False
        game.player.skills['lb']['used'] = False
      
      else:
        lastLBpos = game.player.skills['lb']['log'].pop()
        # print(game.player.name, lastLBpos)
        row, col = lastLBpos
        game.board.squares[row][col].piece.lb = True
        game.player.skills['lb']['used'] = True
      
    def undoFW():
      game.message = game.player.name + ' undo FW'
      if game.player.skills['fw']['used']:
        row, col = game.player.skills['fw']['log'].pop()
        game.board.squares[row][col].fw = None
        game.player.skills['fw']['used'] = False
      
      else:
        row, col = game.player.skills['fw']['log'].pop()
        game.board.squares[row][col].fw = FireWall(game.player.color)
        game.player.skills['fw']['used'] = True
      
    def undoVC():
      game.message = game.player.name + ' undo VC'
      row, col = game.player.skills['vc']['log'].pop()
      game.board.squares[row][col].piece.checked = False
      game.player.skills['vc']['used'] = False
    
    def undo404():
      game.message = game.player.name + ' undo 404'
      posInfo = game.player.skills['404']['log'].pop()
      piece1 = game.player.skills['404']['log'].pop()
      piece0 = game.player.skills['404']['log'].pop()
      row0, col0 = posInfo[0]
      row1, col1 = posInfo[1]
      game.board.squares[row0][col0].piece = piece0
      game.board.squares[row1][col1].piece = piece1
      game.player.skills['404']['used'] = False
      # checked ?
    
    skillUndo = {
      'lb' : undoLB,
      'fw' : undoFW,
      'vc' : undoVC,
      '404' :  undo404
    }
    
    if len(game.skillLog) != 0:
      game.gamelog.pop(list(game.gamelog)[-1])
      skill = game.skillLog.pop(list(game.skillLog)[-1])
      game.revert()
      
      skillUndo[skill]()
  
  def use(self, game: object, which: str, target0: tuple, target1: tuple=None, swap=None) -> bool:
    '''
    - target0 -> row, col
    - target1 -> row, col
    - input must be on board
    '''
    
    def useLB() -> bool:
      row, col = target0
      targetSq = board.squares[row][col]
      
      if player.skills['lb']['used'] :
        row, col = board.getLBpiecePos(player.color)
        board.squares[row][col].piece.lb = False
        player.skills['lb']['used'] = False
        player.skills['lb']['log'].append((row, col))
        return True
      
      # not use lb and valid target
      elif not player.skills['lb']['used'] and targetSq.has_ally_piece(player.color):
        board.squares[row][col].piece.lb = True
        player.skills['lb']['used'] = True
        player.skills['lb']['log'].append((row, col))
        return True
      
      # invalid target
      else: return False
    
    def useFW() -> bool:
      row, col = target0
      
      # used fw, uninstall fw
      if player.skills['fw']['used'] and target0 == player.skills['fw']['log'][-1]:
        
        board.squares[row][col].fw = None
        player.skills['fw']['used'] = False
        player.skills['fw']['log'].append((row, col))
        return True
      
      # not use fw and valid target
      elif (not player.skills['fw']['used'] and
            target0 not in NONFWPOS and 
            not board.squares[row][col].has_enemy_piece(player.color)):
        
        board.squares[row][col].fw = FireWall(player.color)
        player.skills['fw']['used'] = True
        player.skills['fw']['log'].append((row, col))
        return True
      
      # invalid target
      else: return False

    def useVC() -> bool:
      row, col = target0
      targetSq = board.squares[row][col]
      
      if not targetSq.has_enemy_piece(player.color) or player.skills['vc']['used']:
        return False
      else:
        board.squares[row][col].piece.checked = True
        player.skills['vc']['used'] = True
        player.skills['vc']['log'].append((row, col))
        return True

    def use404() -> bool:
      row0, col0 = target0
      row1, col1 = target1
      targetSq0 = board.squares[row0][col0]
      targetSq1 = board.squares[row1][col1]
      
      if (player.skills['404']['used'] or 
          not targetSq0.has_ally_piece(player.color) or 
          not targetSq1.has_ally_piece(player.color)):
        return False
      
      else:
        # store lb position
        if board.squares[row0][col0].piece.lb: lb = row0, col0
        elif board.squares[row1][col1].piece.lb: lb = row1, col1
        else: lb = None
        
        # store swap info for undo
        player.skills['404']['log'].append(copy.deepcopy(board.squares[row0][col0].piece))
        player.skills['404']['log'].append(copy.deepcopy(board.squares[row1][col1].piece))
        player.skills['404']['log'].append([(row0, col0), (row1, col1)])
        
        # clear status of pieces
        board.squares[row0][col0].piece.lb = False
        board.squares[row1][col1].piece.lb = False
        board.squares[row0][col0].piece.checked = False
        board.squares[row1][col1].piece.checked = False
        
        # swap piece
        if swap is not None and swap:
          temp = copy.deepcopy(board.squares[row1][col1].piece)
          board.squares[row1][col1].piece = board.squares[row0][col0].piece
          board.squares[row0][col0].piece = temp
        '''other method'''
        # board.squares[row0][col0].piece, board.squares[row1][col1].piece = board.squares[row1][col1].piece, board.squares[row0][col0].piece
        
        # install lb back
        if lb is not None:
          lbrow, lbcol = lb
          board.squares[lbrow][lbcol].piece.lb = True
        
        player.skills['404']['used'] = True
        return True
        

    skills = {
      'lb' : useLB,
      'fw' : useFW,
      'vc' : useVC,
      '404' :  use404
    }
    
    board = game.board
    player = game.player
    
    if which == '404' and target1 is None: return False
    # elif len(target0) != 2:  return False
    else: # valid target
      used = skills[which]()
      if used: 
        if which != '404': game.message = f'{game.player.name} Used: {which} in {target0}'
        else: game.message = f'{game.player.name} Used: {which} in {target0} and {target1}'
        player.skillLog.append(which)
        game.skillLog[game.turn] = which
        game.gamelog[game.turn] = which
        game.nextPlayer()
      return used