from modules.utils.decorators import needsvoice
from modules.base.command import Command

class Disconnect(Command):
    name = "disconnect"
    alts = ["leave","destroy"]
    oneliner = "Disconnect from the voice chat and stop the music"
    help = "Use this once you're done using the bot if you want the\nbot to leave your voice channel.\nYou can also not disconnect pickup where you left off later."
    examples = "`<prefix>disconnect` - Makes the bot leave your voice channel"
    options = "None"

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