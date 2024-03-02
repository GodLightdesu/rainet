import random
from modules.main import Main
from modules.AI.BattleArray import *
from modules.player import Player
from modules.AI.randomAI import RamdomMove
from modules.AI.recursion import Recursion

# run game
if __name__ == '__main__':
  # use random piece init from database
  yellowInit = battleArraies[random.randint(0, len(battleArraies)-1)]
  blueInit = battleArraies[random.randint(0, len(battleArraies)-1)]
  
  # verse AI that search the future steps
  Yellow = Player('yellow', yellowInit, name='Okabe')
  Blue = Recursion('blue', blueInit, name='Daru', depth=4)
  
  # random choose a piece move to Exit
  # Yellow = RamdomMove('yellow', yellowInit, name='Okabe', mode='Random', virusProb=0.1)
  # Blue = RamdomMove('blue', blueInit, name='Daruu', mode='Exit', virusProb=0.4)
  
  main = Main (Yellow, Blue, view='yellow', cheat=False)
  main.Gback()