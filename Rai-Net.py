from modules.main import Main
from modules.player import Player
from modules.AI.randomAI import RamdomMove
from modules.AI.recursion import Recursion

# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'llvvvvll'
  blueInit = 'llvvvvll'
  
  # Human
  # Yellow = Player('yellow', yellowInit, name='Okabe')
  # Blue = Player('blue', blueInit, name='Daru')
  
  # random choose a piece move to Exit
  # Yellow = RamdomMove('yellow', yellowInit, name='Okabe', mode='Exit', virusProb=0.1)
  # Blue = RamdomMove('blue', blueInit, name='Daruu', mode='Exit', virusProb=0.4)
  
  # test 
  Yellow = Recursion('yellow', yellowInit, name='Okabe', depth=3)
  Blue = Recursion('blue', blueInit, name='Daru', depth=3)
  
  main = Main(Yellow, Blue, view='yellow', cheat=False)
  main.Gback()