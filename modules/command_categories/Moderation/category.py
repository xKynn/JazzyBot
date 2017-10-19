import os
from modules.base.category import Category
path = os.path.dirname(os.path.abspath(__file__)) + r'/commands'
cat_commands = [d.split('.')[0] for d in os.listdir(path) if os.path.isfile(os.path.join(path, d)) and not d.startswith('_') and not d.split('.')[0]==""]
for command in cat_commands:
 exec('from .commands.{0} import {0}'.format(command))
class Moderation(Category):
		  name = "Moderation"
		  commands = []
		  for command in cat_commands:
					   commands.append(eval(command))