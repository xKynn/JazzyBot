import random
class Flinch:
 def __init__(self, char):
  self.char = char
  self.dmg = (((((2*char.level)/5)*40*(char.atk/char.defense))/50)+2)
  self.turns = 1
 def execute(self):
  self.turns -= 1
  if self.turns < 1:
   self.char.statuses.remove(self)
  return 1
