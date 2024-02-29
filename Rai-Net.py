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
  Yellow = Player('yellow', yellowInit, name='Kaito')
  # Blue = Player('blue', blueInit, name='Amadeus')
  
  # random choose a piece move to Exit
  # Yellow = RamdomMove('yellow', blueInit, name='Okabe', mode='Exit', virusProb=0.1)
  # Blue = RamdomMove('blue', blueInit, name='Daruu', mode='Exit', virusProb=0.4)
  
  # test 
  Blue = Recursion('blue', blueInit)
  
  main = Main(Yellow, Blue, view='blue', cheat=False)
  main.Gback()