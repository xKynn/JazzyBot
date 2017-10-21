from datetime import timedelta
from modules.base.command import Command
from modules.utils.embedsender import send
from modules.utils.exceptionhandler import SMexHandler
from modules.utils.exceptions import ServerManPrettyException
class Jump(Command):
    name = "jump"
    alts = ["pick"]
    oneliner = "Jump to any position in the current queue"
    help = "You can use `<prefix>queue` to check where the player is and go back to any track in the queue"
    examples = "`<prefix>jump 2` - If the bot was at 17 before, it will jump after the current song finishes playing and continue playing from 2, i.e 2, 3, 4.."
    options = "None"

    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        try:
            pickno = int(message.content.split()[1])
        except:
            await SMexHandler.handle(bot,ServerManPrettyException( "","Invalid Input!", message.channel))
            return
        if pickno-1 < 0 or pickno > len(player.playlist.entries):
            await SMexHandler.handle(bot,ServerManPrettyException( "Value can only be between 1 and %s" % len(player.playlist.entries),"Invalid Value!", message.channel))
            return
        player.index = pickno-1
        if not player.voice_client.is_playing() and not player.state == "paused":
            bot.loop.create_task(player.prepare_entry())
            await message.channel.send("Jumping to **%s**!" % pickno)
        else:
            player.justjumped = 1
            await message.channel.send("Will jump to **%s** after the current track finishes playing!" % pickno)