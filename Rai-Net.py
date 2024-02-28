from modules.main import Main
from modules.player import Player
from modules.AI.randomAI import RamdomMove

# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'llvvvvll'
  blueInit = 'vvllllvv'
  
  # random move AI
  player1 = RamdomMove('yellow', yellowInit, name='Okabe', mode='Random') 
  # random choose a piece move to Exit
  player2 = RamdomMove('blue', blueInit, name='Daruu', mode='Exit')
  
  main = Main(player1, player2, view='blue', cheat=True)
  main.Gback()