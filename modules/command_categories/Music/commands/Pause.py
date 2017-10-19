from modules.base.command import Command
from modules.music import player,playlist
class Pause(Command):
    name = "pause"
    alts = []
    helpstring ="""Pauses playback of the current song.
           Usage:
               <prefix>pause
           """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        if player.state == 'playing':
            await player.pause()