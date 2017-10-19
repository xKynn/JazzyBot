import asyncio
import discord
import aiohttp
import inspect
import sys
import os
import modules
import traceback
import importlib
import json

#Categories are managed by folder names and a category class in every folder
categories = [d for d in os.listdir('modules/command_categories/') if os.path.isdir(os.path.join('modules/command_categories/', d)) and not d.startswith('_')]
mods = list()
for category in categories:
    mods.append(importlib.import_module('modules.command_categories.{0}.category'.format(category)))

import modules.music.downloader
import modules.utils.db
from modules.utils.db import User,ServerData,BGs, Session

class JazzyBot(discord.Client):
    def __init__(self):
        super().__init__()

        with open('config.json') as conf:
            self.config = json.load(conf)

        self.aiosession = aiohttp.ClientSession(loop=self.loop)

        #This is the sqlalchemy session used throughout the bot for transactions
        self.ses = Session()

        #Prefix can be managed like this because every func call originates from on_message and it checks who called something from where
        self.prefix = self.config['prefix']
        self.cgroups = []
        self.players = {}
        self.vc_clients = {}

        #Download class inspired from musicbot, handles youtubedl extract_info blocking call in an executor
        self.downloader = modules.music.downloader.Downloader(download_folder='dload')

        #nowplaying messages recorded and managed through this so the chat isn't full of these
        self.np_msgs = {}
        self.lock = asyncio.Lock()


    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.config['token'], bot=True, reconnect=True))
        finally:
            self.loop.close()


    async def _deny(self, message):
        await message.channel.send('**%s**, you have been ratelimited, try again in about **4 seconds**' % message.author.name)


    async def on_ready(self):
        await self.change_presence(game = discord.Game(name=";play songname"))

        #Once the bot's ready, go over each category and append the classes to cgroups, the classes hold commands in a list called commands
        for mod,cat in zip(mods,categories):
            self.cgroups.append(getattr(mod,cat))

        print('Logged in as %s/%s' % (self.user.name, self.user.id))


    async def on_message(self, message):
        await self.wait_until_ready()

        #Check if a user is already in our database
        if not message.author.bot: 
            nouse = False
            for user in self.ses.query(User):
                if user.id == int(message.author.id):
                    nouse = True
                    break
            if nouse == False:
                u = User()
                u.id = message.author.id
                u.dollas = 100
                u.level = 1
                u.xp = 0
                self.ses.add(u)
                self.ses.commit()

        found_prefix = False

        #if a server exists get its prefix, if not, make an entry for this new server, set the default prefix from config
        try:
            for qserver in self.ses.query(ServerData):
                if int(message.guild.id) == int(qserver.server_id):
                    self.prefix = qserver.server_prefix
                    found_prefix = True
                    break
            if found_prefix == False:
                try:
                    u = ServerData()
                    u.server_id = message.guild.id
                    u.server_prefix = self.config['prefix']
                    self.ses.add(u)
                    self.ses.commit()
                    self.prefix = self.config['prefix']
                except:
                    self.prefix = self.config['prefix']
        #If this isn't a server at all, set default prefix, when it's a DM
        except:
            self.prefix = r';'

        if not message.content.startswith(self.prefix):
            return

        command, *args = message.content.strip().split()
        command = command[len(self.prefix):].lower().strip() 

        conmsg = '[Command]: %s/%s : %s' % (message.author.name, message.author.id, message.content)
        print(conmsg)

        #Go over all commands in all categories, if it matches with the name or alts, set func to this class' main func and break
        func = None
        for group in self.cgroups:
            for cmd in group.commands:
                if command == cmd.name or command in cmd.alts:
                    func = cmd.main
                    break
        if not func:
            return

        #fetch params for func and populate func_params dict with the required params
        params = inspect.signature(func).parameters.copy()
        func_params = dict()
        if params.pop('bot',None):
            func_params['bot'] = self
        if params.pop('message',None):
            func_params['message'] = message
        if params.pop('leftover_args',None):
            func_params['leftover_args'] = args
        args_expected = []
        for key, param in list(params.items()):
            doc_key = '[%s=%s]' % (key, param.default) if param.default is not inspect.Parameter.empty else key
            args_expected.append(doc_key)
            if not args and param.default is not inspect.Parameter.empty:
                params.pop(key)
                continue
            if args:
                arg_value = args.pop(0)
                func_params[key] = arg_value
                params.pop(key)


        await func(**func_params)
    