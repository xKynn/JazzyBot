import random
class Disable:
 def __init__(self, char,move):
  self.char = char
  move.disable = 1
  self.move = move
  self.turns = random.randint(1,4)
 def execute(self):
  self.turns -= 1
  if self.turns < 1:
     self.move.disable = 0
     self.char.statuses.remove(self)
  return [0,""]