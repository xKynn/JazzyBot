import asyncio
import discord
import aiohttp
import traceback
import random
import requests
import bs4
from modules.base.command import Command
from modules.music import player,playlist
class Autoplay(Command):
    name = "autoplay"
    alts = []
    helpstring ="""Start the bot's autoplay function:\nYouTube autoplay based on last queued song.
      This starts queueing videos that would appear on the right side of the YouTube recommendations automatically based on the last song you queued.
      use <prefix>autoplay stop , to stop autoplay"""
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        command = '%sautoplay ' % bot.prefix
        if message.content[len(command):].lower() == 'stop':
            player.autoplay = False
            await message.channel.send("**:musical_score: Autoplay:** Stopped")
        else:
            player.autoplay = True
            await message.channel.send("**:musical_score: Autoplay:** Started")