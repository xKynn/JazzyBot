from datetime import timedelta
from modules.base.command import Command
from modules.utils.embedsender import send
from modules.utils.exceptionhandler import SMexHandler
from modules.utils.exceptions import ServerManPrettyException
class Seek(Command):
    name = "seek"
    alts = ["ss"]
    helpstring ="""Seek to a certain point in a playing audio
        Usage:
        <prefix>seek hh:mm:ss/h:m:s
        This format must be followed regardless of the track's length, use 0 where the section doesn't apply
        Example:
         For a 3 minute long track
         <prefix>seek 00:02:30
         <prefix>seek 0:2:30
        """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        duration = player.current_entry['duration']
        timelist = shlex.split(message.content)[1].split(':')
        if not len(timelist) == 3:
            await SMexHandler.handle(bot,ServerManPrettyException( "Read ;help seek\nto find out how to use this command","Incorrect format!", message.channel))    
        seek_seconds = int(timelist[0])*60*60 + int(timelist[1])*60 + int(timelist[2])
        print(seek_seconds,duration)
        if int(seek_seconds)>duration:
            await SMexHandler.handle(bot,ServerManPrettyException( "Value can only be between 00:00:00 and %s" % str(timedelta(seconds=duration)),"Invalid Value!", message.channel))
            return
        player.state = "seeking"
        player.justseeked = 1
        player.voice_client.stop()
        bot.loop.create_task(player.play(message.content.split(' ')[1],int(seek_seconds)))
        await message.channel.send("Seeking to %s" % message.content.split(' ')[1])