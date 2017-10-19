from modules.base.command import Command
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
from modules.utils.embedsender import send
from datetime import timedelta
import shlex
class Jump(Command):
    name = "jump"
    alts = ["pick"]
    helpstring ="""Jump to a certain position in the queue and continue playing from there
       Usage:
       <prefix>jump <number>
       """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        try:
            pickno = int(shlex.split(message.content)[1])
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