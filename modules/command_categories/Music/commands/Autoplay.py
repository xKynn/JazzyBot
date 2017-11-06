from modules.base.command import Command
from modules.utils.decorators import needsvoice


class Autoplay(Command):
    name = "autoplay"
    alts = []
    oneliner = "Auto queue songs based on the last song in queue"
    help = "The command works like a toggle, so if you turned autoplay on by using `<prefix>autoplay`, using the same " \
           "command again will disable it. "
    examples = "`<prefix>autoplay` - Turns autoplay on"
    options = "None"

    @staticmethod
    @needsvoice
    async def main(bot, message):
        player = bot.players[message.guild]
        command = '%sautoplay ' % bot.prefix
        if player.autoplay:
            player.autoplay = False
            await message.channel.send("**:musical_score: Autoplay:** Stopped", delete_after=None)
        else:
            player.autoplay = True
            await message.channel.send("**:musical_score: Autoplay:** Started", delete_after=None)
