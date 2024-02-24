import os

from const import *

class FireWall():
  def __init__(self, color: str, used=False, texture=None) -> None:
    self.name = 'fw'
    self.color = color
    self.used = used
    self.texture = texture
    self.set_texture()
  
  def __init__(self, color) -> None:
    super().__init__('fw', color)
  
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
    return True
    
  def useFW(self) -> bool:
    return True

  def useVC(self) -> bool:
    # VirusChecker(color)
    return True

  def use404(self) -> bool:
    # NotFound(color)
    return True

  def use(self, board: object, player: object, which: str, target0: tuple, target1: tuple=None) -> bool:
    # row, col = target0
    # targetSq = board.squares[row][col]
    
    if which == '404' and target1 is None: return False
    # elif len(target0) != 2:  return False
    else: # valid target
      used = self.skills[which]()
      if used: 
        player.skillLog.append(which)
        print(player.skills[which]['log'])
      return used