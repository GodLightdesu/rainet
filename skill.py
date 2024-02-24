import os

from const import *

class Skill:
  
  def __init__(self, name, color, used=False, texture=None) -> None:
    self.name = name
    self.color = color
    self.used = used
    self.texture = texture
    self.set_texture()
    
  def set_texture(self):
    self.texture = os.path.join(
      f'assets/images/{self.color}_{self.name}.png')