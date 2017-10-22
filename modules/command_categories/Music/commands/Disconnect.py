import discord

from modules.base.command import Command
from modules.utils.decorators import needsvoice


class Disconnect(Command):
    name = "disconnect"
    alts = ["leave", "destroy"]
    oneliner = "Disconnect from the voice chat and stop the music"
    help = ("Use this once you're done using the bot if you want the\n"
            "bot to leave your voice channel.\nYou can also not disconnect pickup where you left off later.")
    examples = "`<prefix>disconnect` - Makes the bot leave your voice channel"
    options = "None"

    @staticmethod
    @needsvoice
    async def main(bot, message):
        try:
            player = bot.players[message.guild]
            player.death = 1
            bot.players.pop(message.guild)
        except KeyError:
            return
        await bot.vc_clients.pop(message.guild).disconnect()
        em = discord.Embed(title="Disconnected", description="by " + message.author.mention)
        em.set_image(url="https://i.imgur.com/BkrB9E3.png")
        await message.chanel.send(embed=em)
