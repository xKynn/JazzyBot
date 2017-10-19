import random
class Freeze:
 def __init__(self, char, turns=None):
  self.char = char
  self.dmg = (((((2*char.level)/5)*40*(char.atk/char.defense))/50)+2)
  if not turns:
   self.turns = random.randint(1,4)
  else:
   self.turns = turns
 def execute(self):
  self.turns -= 1
  if self.turns < 1:
   self.char.statuses.remove(self)
  return [1, "**%s** is frozen, it cannot move!" % self.char.user.name]