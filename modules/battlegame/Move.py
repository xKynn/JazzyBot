class Move:
 def __init__(self, name, element, pp, power=None, type=None, effect=None, acc=100):
  self.name = name
  self.power=power
  self.type=type
  self.effect=effect
  self.pp = pp
  self.acc=acc
  self.element = element
  self.disable = 0
 def __repr__(self):
  return self.name