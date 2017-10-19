import asyncio
import discord
import aiohttp
import traceback
import random
import requests
import bs4
from modules.base.command import Command
from modules.music import player,playlist
class Resume(Command):
    name = "resume"
    alts = []
    helpstring ="""Resumes playback of a paused song.
           Usage:
               <prefix>resume
           """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        if player.state == 'paused':
            await player.resume()