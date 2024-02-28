from modules.main import Main
from modules.player import Player
from modules.AI.randomAI import RamdomMove

# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'llvvvvll'
  blueInit = 'vvllllvv'
  
  # random move AI
  Yellow = RamdomMove('yellow', blueInit, name='Daruu', mode='Exit')
  Yellow.setProb(0.1, 0.9)
  
  # random choose a piece move to Exit
  Blue = Player('blue', yellowInit, name='Kaito')
  
  main = Main(Yellow, Blue, view='blue', cheat=False)
  main.Gback()