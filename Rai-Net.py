from modules.main import Main

# run game
if __name__ == '__main__':
  yellowID = 'Okabe'
  blueID = 'Daru'
  
  yellowInit = 'vvllvvll'
  blueInit = 'vvllvvll' # 'vvllllvv'
  
  main = Main(yellowInit, blueInit, yellowID, blueID, view='yellow', cheat=False)
  main.Gback()