import discord

from modules.base.command import Command
from modules.music import player
from modules.music import playlist
from modules.utils.decorators import needsvoice
from modules.utils.ytsearch import ytsearch
class Play(Command):
    name = "play"
    alts = ["pl"]
    helpstring ="""Make the bot add a song to the queue. can be Youtube URL or text to search for
           Usage:
            Normal Usage:
             <prefix>play songLink/playlistLink
             <prefix>play text to search for
            Options:
             earrape  : -rape : <prefix>play -rape you posted in the wrong neighbourhood
             karaoke  : -k    : <prefix>play -k westlife my love
             search   : -s    : <prefix>play -s i would like remix
           """
    @staticmethod
    @needsvoice
    async def main(bot, message):
        effect = 'None'
        searchmode = 0
        options = 0
        try:
            if '-rape' in message.content.split():
                print('rape')
                effect = 'rape'
            elif '-c' in message.content.split():
                print('chip')
                effect = 'c'
            elif '-k' in message.content.split():
                effect = 'k'
            if '-s' in message.content.split():
                searchmode = 1
        except:
            pass

        if not message.guild in bot.vc_clients:
            np_embed = discord.Embed(title = 'Connecting...' , colour=0xffffff )
            np_embed.set_thumbnail(url = 'https://i.imgur.com/DQrQwZH.png')
            trying_msg = await message.channel.send(embed = np_embed)
            if message.author.voice is None:
                np_embed = discord.Embed(title = 'Error',description = 'You are not in a voice channel' , colour=0xffffff )
                np_embed.set_thumbnail(url = 'https://imgur.com/B9YlwWt.png')
                await trying_msg.edit(embed=np_embed)
                return
            try:
                vc = await message.author.voice.channel.connect(timeout=6.0,reconnect=True)
            except:
                np_embed = discord.Embed(title = 'Error',description = "Wasn't able to connect, please try again!" , colour=0xffffff )
                np_embed.set_thumbnail(url = 'https://imgur.com/B9YlwWt.png')
                await trying_msg.edit(embed=np_embed)
                return
            bot.vc_clients[message.guild] = vc
            np_embed = discord.Embed(title = 'Bound to ' + message.author.voice.channel.name , description = 'summoned by **%s**' % message.author.mention, colour=0xffffff )
            np_embed.set_thumbnail(url = 'https://imgur.com/F95gtPV.png')
            await trying_msg.edit(embed = np_embed)
        for n,item in enumerate(message.content.split()[1:],1):
            if not item.startswith('-'):
                break
        song_name = ' '.join(message.content.split()[n:])
        if message.guild in bot.players:
            vc = bot.vc_clients[message.guild]
            mplayer = bot.players[message.guild]
            print('\nplay waiting for download lock\n')
        else:
            vc = bot.vc_clients[message.guild]
            pl = playlist.Playlist(bot)
            print(dir(vc.ws))
            mplayer = player.Player(bot,vc, pl)
            bot.players[message.guild] = mplayer
        with await mplayer.qlock:
            print('\nplay got download lock\n')
            if 'watch?' in song_name:
                info = await bot.downloader.extract_info(bot.loop, song_name, download = False, process=False,retry_on_error=True)
                entry, position = mplayer.playlist.add(info['webpage_url'], message.author, message.channel,info['title'],info['duration'],effect,info['thumbnail'])
                await message.channel.send("**%s** was added to the queue at position %s, %s" % (entry['title'], position, mplayer.playlist.estimate_time(position,mplayer)))
            elif 'list' in song_name:
                info = await bot.downloader.extract_info(bot.loop, song_name, download = False, process=False,retry_on_error=True)
                preparing_msg = await message.channel.send("Processing playlist...")
                position = await mplayer.playlist.async_pl(info['webpage_url'], message.author, message.channel)
                await preparing_msg.edit("Your playlist was added!")
            else:
                if not searchmode:
                    info = await bot.downloader.extract_info(bot.loop, 'ytsearch1:'+song_name, download = False, process=True,retry_on_error=True)
                    print(info['entries'][0]['thumbnails'])
                    entry, position = mplayer.playlist.add(info['entries'][0]['webpage_url'], message.author, message.channel,info['entries'][0]['title'],info['entries'][0]['duration'],effect,info['entries'][0]['thumbnails'][0]['url'],song_name)
                else:
                    info = await ytsearch(bot,message,song_name)
                    entry, position = mplayer.playlist.add(info['webpage_url'], message.author, message.channel,info['title'],info['duration'],effect,info['thumbnail'],song_name)
                await message.channel.send("**%s** was added to the queue at position %s, %s" % (entry['title'], position, mplayer.playlist.estimate_time(position,mplayer)))
            await mplayer.prepare_entry(position-1)