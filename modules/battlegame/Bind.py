import random
class Bind:
 def __init__(self, char):
  self.char = char
  self.turns = random.randing(1,4)
 def execute(self):
  dmg = round((1/16)*self.char.health)
  self.char.health -= dmg
  self.turns -= 1
  if self.turns < 1:
   self.char.statuses.remove(self)
  return [0,""]