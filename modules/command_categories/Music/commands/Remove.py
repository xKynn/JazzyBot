import asyncio
import discord
import aiohttp
import traceback
import random
import requests
import bs4
from modules.base.command import Command
from modules.music import player,playlist
class Remove(Command):
    name = "remove"
    alts = ["rm","rmsong"]
    helpstring ="""Remove a song from queue
        Usage:
        <prefix>rmsong <number>
        """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        stripprefix = message.content.lstrip('%srmsong' % bot.prefix)
        stripspace = stripprefix.lstrip(" ")
        player.playlist.remove(int(stripspace))