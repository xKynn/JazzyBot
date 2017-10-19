import random
class Confusion:
 def __init__(self, char):
  self.char = char
  self.dmg = (((((2*char.level)/5)*40*(char.atk/char.defense))/50)+2)
  self.turns = random.randint(1,5)
 def execute(self):
  p = random.randint(0,10)
  self.turns -= 1
  if self.turns < 1:
   self.char.statuses.remove(self)
  if p <= 50:
   self.char.health -= self.dmg
   return [1, "**%s** hit itself in confusion!" % self.char.user.name]
  return [0,""]