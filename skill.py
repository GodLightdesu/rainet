import os

from const import *

class Skill:
  
  def __init__(self, name: str, color: str, used=False, texture=None) -> None:
    self.name = name
    self.color = color
    self.used = used
    self.texture = texture
    self.set_texture()
    
  def set_texture(self):
    self.texture = os.path.join(
      f'assets/images/{self.color}_{self.name}.png')

def use(board: object, player: object, which: str, target0: tuple, target1: tuple=None) -> bool:
  
  def useLB() -> bool:
    return True
  
  def useFW() -> bool:
    return True

  def useVC() -> bool:
    # VirusChecker(color)
    return True

  def use404() -> bool:
    # NotFound(color)
    return True
  
  skills = {
    'lb' : useLB,
    'fw' : useFW,
    'vc' : useVC,
    '404' :  use404
  }
  
  # row, col = target0
  # targetSq = board.squares[row][col]
  

  if which == '404' and target1 is None: return False
  # elif len(target0) != 2:  return False
  else: # valid target
    used = skills[which]()
    if used: 
      player.skillLog.append(which)
      print(player.skills[which]['log'])
    return used