import random
class Sleep:
 def __init__(self, char, turns=None):
  self.char = char
  self.dmg = (((((2*char.level)/5)*40*(char.atk/char.defense))/50)+2)
  if not turns:
   self.turns = random.randint(1,8)
  else:
   self.turns = turns
 def execute(self):
  self.turns -= 1
  if self.turns < 1:
   self.char.statuses.remove(self)
  return [1, "**%s** is fast asleep!" % self.char.user.name]