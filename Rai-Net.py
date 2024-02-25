from main import Main

# run game
if __name__ == '__main__':
  yellowID = 'Okabe'
  blueID = 'Daru'
  
  yellowInit = 'llvvvvll'
  blueInit = 'vvllllvv' # 'vvllllvv'
  main = Main(yellowInit, blueInit, yellowID, blueID, view='god')
  main.Gback()