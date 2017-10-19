import random
class Burn:
 def __init__(self, char, turns=999999999):
  self.char = char
  self.turns = turns
 def execute(self):
  dmg = (1/16)*self.victim.health
  self.char.health -= dmg
  self.turns -= 1
  return [0,""]