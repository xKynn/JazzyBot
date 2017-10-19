import asyncio
import discord
import aiohttp
import traceback
import os
import importlib
from modules.base.category import Category
path = os.path.dirname(os.path.abspath(__file__)) + r'/commands'
cat_commands = [d.split('.')[0] for d in os.listdir(path) if os.path.isfile(os.path.join(path, d)) and not d.startswith('_') and not d.split('.')[0]==""]
mods = list()
for command in cat_commands:
    exec('from .commands.{0} import {0}'.format(command))
class Music (Category):
		  name = "Music"
		  commands = []
		  for command in cat_commands:
					   commands.append(eval(command))