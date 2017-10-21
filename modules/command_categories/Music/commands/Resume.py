from modules.base.command import Command
class Resume(Command):
    name = "resume"
    alts = []
    helpstring ="""Resumes playback of a paused song.
           Usage:
               <prefix>resume
           """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        if player.state == 'paused':
            await player.resume()