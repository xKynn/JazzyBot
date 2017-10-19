import asyncio
import discord
import aiohttp
import traceback
import random
import requests
import bs4
from urllib.parse import quote_plus
from modules.base.command import Command
from modules.music import player,playlist
import shlex
class Lyrics(Command):
    name = "lyrics"
    alts = ["subtitles"]
    helpstring ="""Get lyrics for songs from www.genius.com
       provide song name for specific lyrics, currently playing song is searched by default
       """
    @staticmethod
    async def main(bot, message):
        noplayer=0
        try:
            player = bot.players[message.server]
        except:
            noplayer = 1
        splitreq = False 
        genius_url = 'https://genius.com/search?q='
        stripspace = ' '.join(shlex.split(message.content)[1:])
        if len(stripspace) < 2 and not noplayer:
            songname = player.current_entry['title']
        else:
            songname = stripspace
        headers = {'Authorization': 'Bearer cUEbLMkIH6Wiw6A3M-yG4VFxyorTPE9ef9pwFiQFU4UhmeEuXewuFe9vGjGZC8-Q'}
        response = requests.get("http://api.genius.com/search?q="+quote_plus(songname),headers=headers)
        output = list()
        for a, b in enumerate(response.json()['response']['hits'][:4], 1):
            output.append('{} {}'.format(a, b['result']['full_title']))
        outputlist = '\n'.join(map(str,output))
        outputlist = '```Markdown\n' + outputlist + '\n' + '#Choose the appropriate result number or type exit to leave the menu\n' + '```'
        sent_msg = await message.channel.send(outputlist)
        def check(m):
            return m.author == message.author and m.channel == message.channel
        while True:
            response_msg = await bot.wait_for('message',check=check,timeout=30)
            if response_msg.content.lower() == 'exit':
                await sent_msg.delete()
                return
            try:
                chosen_number = int(response_msg.content) - 1
                chosen_song = response.json()['response']['hits'][chosen_number]['result']['url']
                break
            except:
                em = discord.Embed(title=':exclamation: Invalid choice', colour = 0xff3a38)
                await message.channel.send(embed = em)
        await sent_msg.delete()
        legit_lyrics = requests.get(chosen_song)
        alphabetsoup = bs4.BeautifulSoup(legit_lyrics.text)
        lyrics = [a.text for a in alphabetsoup.select('div.lyrics p')][0]
        counter=0
        for x in lyrics:
            counter += 1
            if counter >= 1800:
                 splitreq = True
        if splitreq ==True:
            lyrics1 = lyrics[:1800]
            remaininglen = len(lyrics) - 1800
            lyrics2 = lyrics[remaininglen:]
            await message.channel.send(lyrics1)
            await message.channel.send(lyrics2)
        else:
            await message.channel.send(lyrics)