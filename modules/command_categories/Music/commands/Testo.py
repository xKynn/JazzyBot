from modules.base.command import Command
from modules.utils.decorators import needsvoice
import discord
class Testo(Command):
    name = "testo"
    alts = []
    helpstring ="""Skips the current song when enough votes are cast. (50% votes)
        Usage:
            <prefix>skip
        """
    @staticmethod
    @needsvoice
    async def main(bot, message):
            x = await bot.application_info()
            print(x)
            print(dir(x))
