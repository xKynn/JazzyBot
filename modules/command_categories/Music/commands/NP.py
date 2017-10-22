import discord

from datetime import timedelta
from modules.base.command import Command


class NP(Command):
    name = "nowplaying"
    alts = ["np", "current"]
    oneliner = "Get info about the player and the currently playing entry"
    help = "Get status of the current music player, equalizer, current entry, author of the entry and progress."
    examples = "`<prefix>np`"
    options = "None"

    @staticmethod
    async def main(bot, message):
        filled = "▰"
        unfilled = "▱"
        player = bot.players[message.guild]
        if not player.state == 'stopped':
            ps = player.progress
            pt = player.current_entry['duration']
            filled_bars = round((ps * 10) / pt)
            print(filled_bars)
            pstr = str()
            for i in range(10):
                if (i + 1) > filled_bars:
                    pstr += unfilled
                else:
                    pstr += filled
            song_progress = str(timedelta(seconds=ps)).lstrip('0').lstrip(':')
            song_total = str(timedelta(seconds=pt)).lstrip('0').lstrip(':')
            prog_str = pstr + '  %s / %s' % (song_progress, song_total)
            np_embed = discord.Embed(title=player.current_entry['title'],
                                     description='added by **%s**' % player.current_entry['author'].name,
                                     url=player.current_entry['url'], colour=0xffffff)
            np_embed.add_field(name='Progress', value=prog_str)
            np_embed.set_image(url=player.current_entry['thumb'])
            np_embed.set_author(name='Now Playing', icon_url=player.current_entry['author'].avatar_url)
            await message.channel.send(embed=np_embed)
        else:
            await message.channel.send("Nothing is playing!")
