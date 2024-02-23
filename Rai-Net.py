from main import Main

# run game
if __name__ == '__main__':
  yellowID = 'Okabe'
  blueID = 'Daru'
  
  yellowInit = 'llvvvvll'
  blueInit = 'llvvvvll' # 'vvllllvv'
  main = Main(yellowInit, blueInit, yellowID, blueID)
  main.Gback()