import random
from modules.main import Main
from modules.AI.BattleArray import *
from modules.player import Player
from modules.AI.randomAI import RamdomMove
from modules.AI.recursion import Recursion

# run game
if __name__ == '__main__':
  yellowInit = battleArraies[random.randint(0, len(battleArraies)-1)]
  blueInit = battleArraies[random.randint(0, len(battleArraies)-1)]
  
  # Human
  Yellow = Player('yellow', yellowInit, name='Okabe')
  # Blue = Player('blue', blueInit, name='Daru')
  
  # random choose a piece move to Exit
  # Yellow = RamdomMove('yellow', yellowInit, name='Okabe', mode='Exit', virusProb=0.1)
  # Blue = RamdomMove('blue', blueInit, name='Daruu', mode='Exit', virusProb=0.4)
  
  # test 
  # Yellow = Recursion('yellow', yellowInit, name='Okabe', depth=4)
  Blue = Recursion('blue', blueInit, name='Daru', depth=4)
  
  main = Main (Yellow, Blue, view='yellow', cheat=False)
  main.Gback()