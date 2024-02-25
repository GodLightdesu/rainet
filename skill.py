import os

from const import *

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
    self.skills = {
      'lb' : self.useLB,
      'fw' : self.useFW,
      'vc' : self.useVC,
      '404' :  self.use404
    }
    
    self.skillUndo = {
      'lb' : self.undoLB,
      'fw' : self.undoFW,
      'vc' : self.undoVC,
      '404' :  self.use404
    }
    
    self.board = None
    self.player = None
    self.target0 = None
    self.target1 = None
    
  def undoSkill(self, game: object):
    if len(game.skillLog) != 0:
      game.gamelog.pop(list(game.gamelog)[-1])
      skill = game.skillLog.pop(list(game.skillLog)[-1])
      game.revert()
      
      self.skillUndo[skill](game)
  
  def undoLB(self, game):
    game.message = 'undo LB'
    if game.player.skills['lb']['used']:
      row, col = self.player.skills['lb']['log'].pop()
      game.board.squares[row][col].piece.lb = False
      game.player.skills['lb']['used'] = False
    else:
      row, col = self.player.skills['lb']['log'].pop()
      game.board.squares[row][col].piece.lb = True
      game.player.skills['lb']['used'] = True
    
  def undoFW(self, game):
    pass
  
  def undoVC(self, game):
    pass
  
  def use404(self, game):
    pass
  
  def useLB(self) -> bool:
    row, col = self.target0
    targetSq = self.board.squares[row][col]
    
    if self.player.skills['lb']['used'] :
      row, col = self.board.getLBpiecePos(self.player.color)
      self.board.squares[row][col].piece.lb = False
      self.player.skills['lb']['used'] = False
      self.player.skills['lb']['log'].append((row, col))
      return True
    
    # not use lb and valid target
    elif not self.player.skills['lb']['used'] and targetSq.has_ally_piece(self.player.color):
      self.board.squares[row][col].piece.lb = True
      self.player.skills['lb']['used'] = True
      self.player.skills['lb']['log'].append((row, col))
      return True
    
    # invalid target
    else: return False
    
  def useFW(self) -> bool:
    row, col = self.target0
    
    # used fw, uninstall fw
    if self.player.skills['fw']['used'] and self.target0 == self.player.skills['fw']['log'][-1]:
      
      self.board.squares[row][col].fw = None
      self.player.skills['fw']['used'] = False
      self.player.skills['fw']['log'].append((row, col))
      return True
    
    # not use fw and valid target
    elif (not self.player.skills['fw']['used'] and
          self.target0 not in NONFWPOS and 
          not self.board.squares[row][col].has_enemy_piece(self.player.color)):
      
      self.board.squares[row][col].fw = FireWall(self.player.color)
      self.player.skills['fw']['used'] = True
      self.player.skills['fw']['log'].append((row, col))
      return True
    
    # invalid target
    else: return False

  def useVC(self) -> bool:
    # VirusChecker(color)
    return True

  def use404(self) -> bool:
    # NotFound(color)
    return True

  def use(self, board: object, player: object, which: str, target0: tuple, target1: tuple=None) -> bool:
    self.board = board
    self.player = player
    self.target0 = target0
    self.target1 = target1
    
    if which == '404' and target1 is None: return False
    # elif len(target0) != 2:  return False
    else: # valid target
      used = self.skills[which]()
      if used: 
        player.skillLog.append(which)
        print(player.skills[which]['log'])
      return used