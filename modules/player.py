
from email import message


class Player:
  
  def __init__(self, color: str, pieceInit: str, name: str=None, isHuman=True) -> None:
    '''
    ID is sugggested to be less or equal to 7 characters
    
    pieceInit: 'v' -> virus; 'l' -> link
      - please award capital letter is not allowed
    '''
    # self info
    self.isHuman = isHuman
    self.color = color
    self.name = name
    
    if self.checkPieceInit(pieceInit) is not None:
      raise ValueError(self.checkPieceInit(pieceInit))
    
    self.pieceInit = pieceInit
    
    self.link_eat = 0
    self.link_enter = 0
    self.virus_eat = 0
    self.virus_enter = 0
    self.moveLog = []
    self.skillLog = []
    # skill
    self.skills = {
      'lb' : {'used' : False, 'log' : []},
      'fw' : {'used' : False, 'log' : []}, 
      'vc' : {'used' : False, 'log' : []}, 
      '404' : {'used' : False, 'log' : []}
    }
    
    # server
    self.serverStack = []
  
  def reset(self):
    self.__init__(self.color, self.pieceInit, self.name, self.isHuman)
  
  def checkPieceInit(self, pieceInit: str):
    v, l = 0, 0
    message = None
    for piece in pieceInit:
      if piece == 'V' or piece == 'L': return 'Capital letter'
      elif piece == 'v':  v += 1
      elif piece == 'l': l += 1
    
    if v != 4: message = 'You should input 4 virus'
    elif l != 4:  message = 'You should input 4 link'
    
    return message