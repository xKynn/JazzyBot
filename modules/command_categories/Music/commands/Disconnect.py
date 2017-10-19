from modules.utils.decorators import needsvoice
from modules.base.command import Command

class Disconnect(Command):
    name = "disconnect"
    alts = ["leave","destroy"]
    helpstring ="""Disconnect from the voice chat and stop the music
       Usage:
       <prefix>disconnect
       """
    @staticmethod
    @needsvoice
    async def main(bot, message):
        try:
            player = bot.players[message.guild]
            player.death = 1
            bot.players.pop(message.guild)
        except:
           	pass
        await bot.vc_clients.pop(message.guild).disconnect()