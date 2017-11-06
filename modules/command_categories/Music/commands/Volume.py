import datetime

from modules.base.command import Command
from modules.utils.exceptionhandler import SMexHandler
from modules.utils.exceptions import ServerManPrettyException
class Volume(Command):
    name = "volume"
    alts = ["vol"]
    helpstring ="""Remove a song from queue
        Usage:
        <prefix>rmsong <number>
        """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        volume = float(message.content.split()[1])
        if volume<=2.0 and volume>=0:
            player.volume = volume
            await send(bot,"Volume changed!", ":loud_sound: New volume is %s"%volume,0xCCD6DD,message.channel)
            if player.voice_client.is_playing():
                player.justvoledit = 1
                player.voice_client.stop()
                seektm = datetime.datetime.fromtimestamp(player.accu_progress) - datetime.timedelta(hours=5,minutes=30)
                bot.loop.create_task(player.play(str(seektm.strftime('%H:%M:%S.%f')),player.accu_progress))
        else:
            await SMexHandler.handle(bot,ServerManPrettyException( "Volume value can only range from 0.0-2.0","Invalid Value!", message.channel))