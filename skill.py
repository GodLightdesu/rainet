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
  
  def useLB(self) -> bool:
    row, col = self.target0
    targetSq = self.board.squares[row][col]
    
    if self.player.skills['lb']['used'] and self.target0 == self.player.skills['lb']['log'][-1]:
      
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
    # targetSq = self.board.squares[row][col]
    
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