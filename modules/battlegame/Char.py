import math
import yaml
import random
class Char:
 def __init__(self,user, type, PS, FS, level,moveset):
  self.user = user
  self.type = type
  self.PS = PS
  self.FS = FS
  self.atk = 50 + (int(level)-1)
  self.defense = 50 + (int(level)-1)
  self.acc = 100
  self.ev = 100
  self.level = int(level)
  self.health = round(((((100+294)*2+(math.sqrt(150)/4))*int(level))/100)+int(level)+10)
  self.max_health = round(((((100+294)*2+(math.sqrt(150)/4))*int(level))/100)+int(level)+10)
  self.moveset = moveset
  self.statuses = []
  self.Invincible = False
  self.hide_move = [False]
  self.last_move = None
  self.bide = [False]
 def attack(self,enemy,move=None):
  self.last_move = move
  lst = []
  for status in self.statuses:
   lst.append(status.execute())
  try:
   if self.bide[2] > 0:
    self.bide[2] -= 1
    return False, "**%s**, is storing energy!" % self.user.name
   elif self.bide[2] == 0:
    enemy.health -= self.bide[1]*2
    self.bide.clear()
    return False, "**%s** unleashed their stored energy!" % self.user.name
  except:
   pass
  statusmsg = str()
  for status in lst:
   if status[0]:
    move.pp -= 1
    return False, status[1]
  if enemy.Invincible:
   return False, "**%s**, cannot be damaged in this state!" % enemy.user.name
  if self.hide_move[0]:
   hit = False
   move = self.hide_move[1]
   self.hide_move.clear()
   self.Invincible = False
   baseA = move.acc
   p = round(baseA * (self.acc/enemy.ev))
   p = p*100
   if p >= 100:
    hit = True
   else:
    prob = random.randint(0,100)
    if prob >= p:
     hit = True
   if hit == True:
    typematchup = yaml.load(open(r'modules\battlegame\types.yaml',"r"))
    if enemy.type in typematchup[move.element]['weak']:
     type = 0.5
    elif enemy.type in typematchup[move.element]['strong']:
     type = 2
    else:
     type = 1
    ran = random.randint(85,100)/100
    if move.element == self.type:
     stab = 1.5
    else:
     stab = 1
    mod = type * ran * stab
    dmg = round(((((2*self.level)*move.power*(self.atk/enemy.defense))/50)+2) * mod)
    enemy.health -= dmg
    if enemy.bide[0]:
     enemy.bide[1] += dmg
    move.pp -= 1
    return False, "**%s** dealt %s HP of damage and came back to their original place!" % (self.user.name, round(dmg))
   else:
    return False, "**%s's** comeback failed!" % self.user.name
  if move.type == 'bide':
   self.bide[0] = True
   self.bide.append(0)
   self.bide.append(2)
   move.pp -= 1
   return False, "**%s** used Bide, they're storing energy!" % self.user.name
  if move.pp < 1:
   return True, "**%s** doesn't have enough PP to use this move!" % self.user.name
  if move.disable:
   move.pp -= 1
   return False, "**%s**, can't use **%s**, **%s's** Disable is blocking it's usage!" % (self.user.name, move.name, enemy.user.name)
  if move.type in ['mirror move', 'mimic']:
   if not enemy.last_move.type in ['mirror move','mimic']:
    move.pp -= 1
    move = enemy.last_move
    move.pp += 1
   else:
    move.pp -= 1
    return False, "**%s**, was not able to replicate the previous move!" % self.user.name
  if move.type == 'disable':
   move.pp -= 1
   print(enemy.last_move)
   if not enemy.last_move == None:
    print("disable if")
    from .Disable import Disable
    status = Disable(enemy,enemy.last_move)
    enemy.statuses.append(status)
    return False, "**%s**, used Disable!\n**%s** was disabled from using **%s**!" % (self.user.name, enemy.user.name, enemy.last_move.name)
   else:
    return False, "**%s**, used Disable!\nDisable failed, as it cannot be played as a first move!" % self.user.name
  if move.type == 'stat':
   if move.effect == 'def-':
    enemy.defense -= move.power
    return False, "**%s** decreased **%s's** defense by %s" % (self.user.name, enemy.user.name, move.power)
   if move.effect == 'def+':
    self.defense += move.power
    return False, "**%s** increased their defense by %s" % (self.user.name, move.power)
   if move.effect == 'acc-':
    enemy.acc -= move.power
    return False, "**%s** decreased **%s's** accuracy by %s" % (self.user.name, enemy.user.name, move.power)
   if move.effect == 'ev+':
    self.ev += move.power
    return False, "**%s** increased their evasiveness by %s" % (self.user.name, move.power)
   if move.effect == 'atk-':
    enemy.atk -= move.power
    return False, "**%s** decreased **%s's** attack by %s" % (self.user.name, enemy.user.name, move.power)
   if move.effect == 'atk+':
    self.atk += move.power
    return False, "**%s** increased their attack by %s" % (self.user.name, move.power)
   move.pp -= 1
  elif move.type == 'dmg':
   hit = False
   move.pp -= 1
   baseA = move.acc
   p = round(baseA * (self.acc/enemy.ev))
   p = p*100
   if p >= 100:
    hit = True
   else:
    prob = random.randint(0,100)
    if prob <= p:
     hit = True
   if hit == True:
    typematchup = yaml.load(open(r'modules\battlegame\types.yaml',"r"))
    if enemy.type in typematchup[move.element]['weak']:
     type = 0.5
    elif enemy.type in typematchup[move.element]['strong']:
     type = 2
    else:
     type = 1
    ran = random.randint(85,100)/100
    if move.element == self.type:
     stab = 1.5
    else:
     stab = 1
    mod = type * ran * stab
    dmg = round(((((2*self.level)*move.power*(self.atk/enemy.defense))/50)+2) * mod)
    enemy.health -= dmg
    if enemy.bide[0]:
     enemy.bide[1] += dmg
    game_log = "**%s** used **%s**!" % (self.user.name, move.name)
    if type == 2:
     game_log += "It's very effective!"
    elif type == 0.5:
     game_log += "It's not effective!"
   else:
    return False, "**%s** used **%s**, but it missed!" % (self.user.name, move.name)
   if move.effect:
     stat = False
     stat_p = random.randint(0,100)
     if stat_p <= 30:
      stat = True
     if stat == True:
      if 'confuse' in move.effect:
       from .Confusion import Confusion
       status = Confusion(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also confused **%s**!" % enemy.user.name
      if 'paralyze' in move.effect:
       from .Paralyze import Paralyze
       status = Paralyze(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also paralyzed **%s**!" % enemy.user.name
      if 'poison' in move.effect:
       if 'badly' in move.effect:
        from .BPoison import BPoison
        status = Poison(enemy)
        enemy.statuses.append(status)
        game_log += "\nIt also badly poisoned **%s**!" % enemy.user.name
       else:
        from .Poison import Poison
        status = Poison(enemy)
        enemy.statuses.append(status)
        game_log += "\nIt also poisoned **%s**!" % enemy.user.name
      if 'sleep' in move.effect:
       from .Sleep import Sleep
       status = Sleep(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also put **%s** to sleep!" % enemy.user.name
      if 'turn-skip' in move.effect:
       from .Flinch import Flinch
       if '+' in move.effect:
        #status = Flinch(enemy)
        #enemy.statuses.append(status)
        game_log += "\n**%s** flinched!" % enemy.user.name
        return True, game_log
      if 'bind' in move.effect:
       if not enemy.type == "ghost":
        from .Bind import Bind
        status = Bind(enemy)
        enemy.statuses.append(status)
        game_log += "\nIt also tighly bound **%s**!" % enemy.user.name
       else:
        game_log += "\nAn enemy of the ghost type can not be bound!"
      if 'burn' in move.effect:
       from .Burn import Burn
       status = Burn(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also burnt **%s**!" % enemy.user.name
      if 'freeze' in move.effect:
       from .Freeze import Freeze
       status = Freeze(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also froze **%s**!" % enemy.user.name
     if move.effect == 'turn-skip-':
        status = Flinch(self)
        self.statuses.append(status)
     if move.effect == 'self-dmg':
      self.health -= (dmg*0.25)
      game_log += "\nIt also hurt **%s**!" % self.user.name
     if move.effect == 'dream eater':
      from .Sleep import Sleep
      if Sleep in enemy.statuses:
       heal = dmg/2
       if self.health + heal > self.max_health:
        self.health = self.max_health
       else:
        self.health += heal
       game_log += "\nIt also healed **%s**!" % self.user.name
     if move.effect == 'heal':
       heal = dmg/2
       if self.health + heal > self.max_health:
        self.health = self.max_health
       else:
        self.health += heal
       game_log += "\nIt also healed **%s**!" % self.user.name
     if move.effect == 'fire spin':
       from .Burn import Burn
       status = Burn(enemy, random.randint(4,6))
       enemy.statuses.append(status)
       game_log += "\nIt also trapped **%s** in fire!" % enemy.user.name
   return False, game_log
  elif move.type == 'multihit':
   hit = False
   move.pp -= 1
   baseA = move.acc
   p = round(baseA * (self.acc/enemy.ev))
   p = p*100
   if p >= 100:
    hit = True
   else:
    prob = random.randint(0,100)
    if prob >= p:
     hit = True
   if hit == True:
    typematchup = yaml.load(open(r'modules\battlegame\types.yaml',"r"))
    if enemy.type in typematchup[move.element]['weak']:
     type = 0.5
    elif enemy.type in typematchup[move.element]['strong']:
     type = 2
    else:
     type = 1
    ran = random.randint(85,100)/100
    if move.element == self.type:
     stab = 1.5
    else:
     stab = 1
    mod = type * ran * stab
    dmg = round(((((2*self.level)*move.power*(self.atk/enemy.defense))/50)+2) * mod)
    hits = random.randint(eval(move.effect))
    enemy.health -= dmg * hits
    if enemy.bide[0]:
     enemy.bide[1] += dmg*hits
    game_log = "**%s** used **%s**!" % (self.user.name, move.name)
    if type == 2:
     game_log += "It's very effective!"
    elif type == 0.5:
     game_log += "It's not effective!"
    return False, game_log
   else:
    return False, "**%s** used **%s**, but it missed!" % (self.user.name, move.name)
  elif move.type == 'status': 
   baseA = move.acc
   p = round(baseA * (self.acc/enemy.ev))
   p = p*100
   hit = False
   if p >= 100:
    hit = True
   if random.randint(0,100) < p:
    hit = True
   game_log += "**%s** used **%s**!" % (self.user.name, move.name)
   if hit:
      if 'confuse' in move.effect:
       from .Confusion import Confusion
       status = Confusion(enemy)
       enemy.statuses.append(status)
       game_log += "\n**%s**, was confused!" % enemy.user.name
      if 'paralyze' in move.effect:
       from .Paralyze import Paralyze
       status = Paralyze(enemy)
       enemy.statuses.append(status)
       game_log += "\n**%s**, was paralyzed!" % enemy.user.name
      if 'sleep' in move.effect:
       from .Sleep import Sleep
       status = Sleep(enemy)
       enemy.statuses.append(status)
       game_log += "\n**%s**, was put to sleep!" % enemy.user.name
      if 'poison' in move.effect:
       if 'badly' in move.effect:
        from .BPoison import BPoison
        status = Poison(enemy)
        enemy.statuses.append(status)
        game_log += "\n**%s**, was badly poisoned!" % enemy.user.name
       else:
        from .Poison import Poison
        status = Poison(enemy)
        enemy.statuses.append(status)
        game_log += "\n**%s**, was poisoned!" % enemy.user.name
      if 'bind' in move.effect:
       from .Bind import Bind
       status = Bind(enemy)
       enemy.statuses.append(status)
       game_log += "\n**%s**, was rightly bound!" % enemy.user.name
      if 'burn' in move.effect:
       from .Burn import Burn
       status = Burn(enemy)
       enemy.statuses.append(status)
       game_log += "\n**%s**, was burnt!" % enemy.user.name
   else:
    game_log += '\nBut it failed!'
   return False, game_log
  elif move.type == 'counter':
   if not enemy.last_move:
    move.pp-= 1
    return False, "**%s** used **%s**, but it failed!" % (self.user.name, move.name)
   if enemy.last_move.type == 'dmg':
    move.pp -= 1
    c_move = enemy.last_move
    hit = False
    baseA = c_move.acc
    p = round(baseA * (self.acc/enemy.ev))
    p = p*100
    if p <= 100:
     hit = True
    else:
     prob = random.randint(0,100)
     if prob >= p:
      hit = True
    if hit == True:
     typematchup = yaml.load(open(r'modules\battlegame\types.yaml',"r"))
     if enemy.type in typematchup[c_move.element]['weak']:
      type = 0.5
     elif enemy.type in typematchup[c_move.element]['strong']:
      type = 2
     else:
      type = 1
     ran = random.randint(85,100)/100
     if c_move.element == self.type:
      stab = 1.5
     else:
      stab = 1
     mod = type * ran * stab
     dmg = round(((((2*self.level)*(c_move.power*2)*(self.atk/enemy.defense))/50)+2) * mod)
     enemy.health -= dmg
     if enemy.bide[0]:
      enemy.bide[1] += dmg
     game_log = "**%s** used **%s**!" % (self.user.name, c_move.name)
     if type == 2:
      game_log += "It's very effective!"
     elif type == 0.5:
      game_log += "It's not effective!"
    else:
     return False, "**%s** used **%s**, but it missed!" % (self.user.name, c_move.name)
   else:
     return False, "**%s** used **%s**, but it failed!" % (self.user.name, move.name)
   if c_move.effect:
     stat = False
     stat_p = random.randint(0,100)
     if stat_p <= 30:
       stat = True
     if stat == True:
      if 'confuse' in c_move.effect:
       from .Confusion import Confusion
       status = Confusion(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also confused **%s**!" % enemy.user.name
      if 'paralyze' in c_move.effect:
       from .Paralyze import Paralyze
       status = Paralyze(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also paralyzed **%s**!" % enemy.user.name
      if 'poison' in c_move.effect:
       if 'badly' in c_move.effect:
        from .BPoison import BPoison
        status = Poison(enemy)
        enemy.statuses.append(status)
        game_log += "\nIt also badly poisoned **%s**!" % enemy.user.name
       else:
        from .Poison import Poison
        status = Poison(enemy)
        enemy.statuses.append(status)
        game_log += "\nIt also poisoned **%s**!" % enemy.user.name
      if 'sleep' in c_move.effect:
       from .Sleep import Sleep
       status = Sleep(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also put **%s** to sleep!" % enemy.user.name
      if 'turn-skip' in c_move.effect:
       from .Flinch import Flinch
       if '+' in c_move.effect:
        #status = Flinch(enemy)
        #enemy.statuses.append(status)
        game_log += "\n**%s** flinched!" % enemy.user.name
        return True, game_log
      if 'bind' in c_move.effect:
       from .Bind import Bind
       status = Bind(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also tighly bound **%s**!" % enemy.user.name
      if 'burn' in c_move.effect:
       from .Burn import Burn
       status = Burn(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also burnt **%s**!" % enemy.user.name
      if 'freeze' in c_move.effect:
       from .Freeze import Freeze
       status = Freeze(enemy)
       enemy.statuses.append(status)
       game_log += "\nIt also froze **%s**!" % enemy.user.name
     if c_move.effect == 'turn-skip-':
        status = Flinch(self)
        self.statuses.append(status)
     if c_move.effect == 'self-dmg':
      self.health -= (dmg*0.25)
      game_log += "\nIt also hurt **%s**!" % self.user.name
     if c_move.effect == 'dream eater':
      from .Sleep import Sleep
      if Sleep in enemy.statuses:
       heal = dmg/2
       if self.health + heal > self.max_health:
        self.health = self.max_health
       else:
        self.health += heal
       game_log += "\nIt also healed **%s**!" % self.user.name
     if c_move.effect == 'heal':
       heal = dmg/2
       if self.health + heal > self.max_health:
        self.health = self.max_health
       else:
        self.health += heal
       game_log += "\nIt also healed **%s**!" % self.user.name
     if c_move.effect == 'fire spin':
       from .Burn import Burn
       status = Burn(enemy, random.randint(4,6))
       enemy.statuses.append(status)
       game_log += "\nIt also trapped **%s** in fire!" % enemy.user.name
   return False, game_log
  elif move.type == 'hide-attack':
   self.hide_move[0] = True
   self.hide_move.append(move)
   self.Invincible = True
   return False, "**%s** went out of **%s's** reach!" % (self.user.name, enemy.user.name)
  elif move.type == 'rest':
   from .Sleep import Sleep
   status = Sleep(self,2)
   self.statuses.append(status)
   self.health = self.max_health
   return False, "**%s**, is resting!" % self.user.name
  elif move.type == 'dragon rage':
   enemy.health -= 40
   move.pp -= 1
   return False, "**%s**, used Dragon Rage!" % self.user.name
  elif move.type == 'leech seed':
   from .Leechseed import Leechseed
   status = Leechseed(enemy, self)
   enemy.statuses.append(status)
   move.pp -= 1
   return False, "**%s**, planted a Leech Seed!" % self.user.name
  elif move.type == 'super fang':
   hit = False
   move.pp -= 1
   baseA = move.acc
   p = round(baseA * (self.acc/enemy.ev))
   p = p*100
   if p <= 100:
    hit = True
   else:
    prob = random.randint(0,100)
    if prob >= p:
     hit = True
   if hit == True:
    dmg = round(enemy.health/2)
    enemy.health -= dmg
    if enemy.bide[0]:
     enemy.bide[1] += dmg
    return False, "**%s** used Super Fang!" % self.user.name
   else:
    return False, "**%s** used Super Fang, but it failed!" % self.user.name
 def miss_turn(self, reason):
  pass
 def pop_potion(self):
  if self.PS < 1:
   return True, "**%s**, has no potions available!" % self.user.name
  if self.health + 20 > self.max_health:
   self.health = self.max_health
  else:
   self.health += 20
  self.PS -= 1
  return False, "**%s** healed themselves for 20HP" % self.user.name
 def pop_FS(self):
  if self.FS < 1:
   return True, "**%s**, has no Full Restores available!" % self.user.name
  self.health = self.max_health
  self.statuses.clear()
  self.FS -= 1
  return False, "**%s** completely healed themselves and got rid of all status effects!" % self.user.name
    
    
    
    
    
    
    
    
    
    
    