from modules.base.command import Command


class Pause(Command):
    name = "pause"
    alts = []
    oneliner = "Pauses playback of the current song."
    help = "You cannot switch entries while the player is paused"
    examples = "`<prefix>pause`"
    options = "None"

    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        if player.state == 'playing':
            await player.pause()
