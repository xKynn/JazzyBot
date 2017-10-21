from modules.base.command import Command
class Remove(Command):
    name = "remove"
    alts = ["rm","rmsong"]
    helpstring ="""Remove a song from queue
        Usage:
        <prefix>rmsong <number>
        """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        stripprefix = message.content.lstrip('%srmsong' % bot.prefix)
        stripspace = stripprefix.lstrip(" ")
        player.playlist.remove(int(stripspace))