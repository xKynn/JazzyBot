import random
class Paralyze:
 def __init__(self, char):
  self.char = char
  self.dmg = (((((2*char.level)/5)*40*(char.atk/char.defense))/50)+2)
 def execute(self):
  ran = random.randint(0,100)
  if ran <= 25:
   return [1, "**%s** is paralyzed!" % self.char.user.name]
  else:
   return [0,""]