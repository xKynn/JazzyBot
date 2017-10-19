from modules.base.command import Command
from modules.utils.decorators import needsvoice
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
from modules.utils.embedsender import send
import time
import datetime
import shlex
class EQ(Command):
    name = "eq"
    alts = ["equalizer"]
    helpstring ="""Apply preset equalizers! Choose from Pop, Classic, Jazz, Rock and Bass Boost
          Usage:
              <prefix>eq pop
              <prefix>eq bassboost
          """
    @staticmethod
    @needsvoice
    async def main(bot, message):
        effects = {'pop':'Pop','classic':'Classic','jazz':'Jazz','rock':'Rock','bb':'Bass Boost','normal':'Normal','vocals':'Vocals'}
        player = bot.players[message.guild]
        eq = shlex.split(message.content)[1]
        if not eq.lower() in effects.keys():
            await SMexHandler.handle(bot,ServerManPrettyException( "%s, is not a valid EQ effect." % eq,"Invalid EQ effect!", message.channel))
            return
        player.EQ = eq.lower()
        if player.voice_client.is_playing():
            player.justvoledit = 1
            player.voice_client.stop()
            seektm = datetime.datetime.fromtimestamp(player.accu_progress) - datetime.timedelta(hours=5,minutes=30)
            bot.loop.create_task(player.play(str(seektm.strftime('%H:%M:%S.%f')),player.accu_progress))
            print(str(time.strftime('%H:%M:%S', time.gmtime(player.accu_progress))))
        await send(bot,"Equalizer", ":loud_sound: Equalizer has been set to %s."%effects[eq.lower()],0xCCD6DD,message.channel)
