# Rai-Net Access Battlers

Used for studying and developed based on pygame

## Description

Learning python for interest, hope I can add a AI engine in the future

## File structure

```bash
├── assets
│   ├── font
│   └── images
│   └── screenshots
├── modules
│   ├── AI
│   │   └── Okabe.py
│   ├── board.py
│   ├── clicker.py
│   ├── const.py
│   ├── game.py
│   ├── main.py
│   ├── move.py
│   ├── piece.py
│   ├── player.py
│   ├── skill.py
│   └── square.py
├── Rai-Net.py
```

Game images stored at folder `/assets/images/`;

libraries stored at folder `/modules/`;

## Getting Started

### Dependencies

`pygame`

### Executing program

start by simpely running `Rai-Net.py`

```python
# run game
if __name__ == '__main__':
  
  # 'vvllllvv'
  yellowInit = 'vvllvvll'
  blueInit = 'vvllvvll'
  
  player1 = Player('yellow', yellowInit, name='Kaito')
  player2 = Okabe('blue', blueInit) # random move AI
  
  main = Main(player1, player2, view='yellow', cheat=False)
  main.Gback()
```

<!-- ### Functions Introduction

```python

``` -->

## Authors

^_*

## Version History

* 1.3 Add function - aniamteMove
* 1.1 Add a random move AI - Okabe (without skills)
* 1.0
* 0.1 - 0.9
  * Initial Release
  * Various bug fixes and optimizations
  * See [commit change](https://github.com/GodLightdesu/Rai-Net/commits/main/)
  <!--or See [release history]() -->
  
## To do

* [✓] get all possible valid moves
  * [✓] get non lb-installed pieces' valid moves
  * [✓] get lb-installed pieces' valid moves
* [✓] add skills' function (include undo)
  * [✓] line boost
  * [✓] fire wall
  * [✓] virus check
  * [✓] 404
* [ ] add a AI
  * [✓] Okane (random move only)
  * Daru
  * Christina
  * Faris
  * etc...

## Acknowledgments

Inspiration, code snippets, images source, etc.

[Coding Spot](https://www.youtube.com/watch?v=OpL0Gcfn4B4&t=15084P)

[Creating a Chess Engine in Python](https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&si=L7rxLYA93rwiaS)

[Images source](https://github.com/FourProbiotics/RainetByCCC/blob/mybranch/assets/resources/Texture/Tex1.png)
