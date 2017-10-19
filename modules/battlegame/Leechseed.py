import random
class Leechseed:
 def __init__(self, victim, healer):
  self.victim = victim
  self.healer = healer
 def execute(self):
  heal = round((1/16)*self.victim.health)
  if self.healer.health + heal > self.healer.max_health:
   self.healer.health = self.healer.max_health
  else:
   self.healer.health += heal
  return [0,""]