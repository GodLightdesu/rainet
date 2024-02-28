from modules.main import Main
from modules.player import Player
from modules.AI.randomAI import RamdomMove

# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'llvvvvll'
  blueInit = 'llvvvvll'
  
  # Human
  # Yellow = Player('yellow', yellowInit, name='Kaito')
  # Blue = Player('blue', blueInit, name='Kaito')
  
  # random choose a piece move to Exit
  Yellow = RamdomMove('yellow', blueInit, name='Okabe', mode='Exit', virusProb=0.1)
  Blue = RamdomMove('blue', blueInit, name='Daruu', mode='Exit', virusProb=0.9)
  
  main = Main(Yellow, Blue, view='god', cheat=False)
  main.Gback()