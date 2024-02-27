from modules.main import Main
from modules.player import Player
from modules.AI.Okabe import Okabe

# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'vvllllvv'
  blueInit = 'llvvvvll'
  
  # player1 = Player('yellow', yellowInit, name='Kaito')
  # player2 = Player('blue', blueInit, name='Daru')
  player1 = Okabe('yellow', yellowInit) # random move AI
  player2 = Okabe('blue', blueInit) # random move AI
  
  main = Main(player1, player2, view='yellow', cheat=True)
  main.Gback()