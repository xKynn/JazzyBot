import random
class BPoison:
 def __init__(self, char):
  self.char = char
  self.turns = random.randing(1,4)
  self.ratio = 1/16
 def execute(self):
  dmg = self.ratio*self.char.health
  self.char.health -= round(dmg)
  self.ratio += (1/16)
  self.turns -= 1
  if self.turns < 1:
   self.char.statuses.remove(self)
  return [0,""]