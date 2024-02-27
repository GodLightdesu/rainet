from modules.main import Main
from modules.player import Player
from modules.AI.Okabe import Okabe

# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'vvllvvll'
  blueInit = 'vvllvvll'
  
  player1 = Player('yellow', yellowInit, name='Kaito')
  player2 = Okabe('blue', blueInit) # random move AI
  
  main = Main(player1, player2, view='yellow', cheat=False)
  main.Gback()