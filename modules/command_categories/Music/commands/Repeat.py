from modules.base.command import Command
from modules.utils.decorators import needsvoice
class Repeat(Command):
    name = "repeat"
    alts = [""]
    helpstring ="""Repeats the current song.
           Usage:
               <prefix>repeat
           """
    @staticmethod
    @needsvoice
    async def main(bot, message):
        player = bot.players[message.guild]
        if not player.voice_client.is_playing():
            await message.channel.send("Nothing is playing to repeat!")
        else:
            if player.repeat:
                player.repeat = 0
                await message.channel.send(":negative_squared_cross_mark: **%s**, has been taken off repeat." % player.current_entry['title'])
            else:
                player.repeat = 1
                await message.channel.send(":arrows_counterclockwise: **%s**, has been set to repeat, till the end of time itself!\nUse this command again to interrupt the repetition." % player.current_entry['title'])