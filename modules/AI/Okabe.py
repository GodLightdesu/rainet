import random

from ..player import Player

class Okabe(Player):
  def __init__(self, color: str, pieceInit: str, name='Okabe', isHuman=False) -> None:
    super().__init__(color, pieceInit, name, isHuman)

  def findRandomMove(self, validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]