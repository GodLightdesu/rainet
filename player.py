
class Player:
  
  def __init__(self, color,  name=None) -> None:
    # self info
    self.color = color
    self.name = name
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