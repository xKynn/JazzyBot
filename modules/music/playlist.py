import asyncio
from random import shuffle
from collections import deque
from itertools import islice
import datetime
class Playlist:

    def __init__(self,bot):
        self.bot = bot
        self.entries = deque()

    def __iter__(self):
        return iter(self.entries)

    def shuffle(self):
        shuffle(self.entries)

    def clear(self):
           self.entries.clear()

    def repeat(self):
        l = deque()
        for m in self.entries:
         l.append(m)
        for x in l:
         self.entries.append(x)

    def remove(self, index):
        self.entries.remove(self.entries[index-1])

    def gettrack(self, index):
        return self.entries[index-1]

    def getlist(self):
        l = deque()
        for m in self.entries:
         l.append(m)
        return l

    def estimate_time(self,position,player):
        estimated_time = sum([e['duration'] for e in islice(self.entries,player.index+1, position - 1)])
        try:
            estimated_time += (player.current_entry['duration'] - player.progress)
        except:
            pass
        if estimated_time > 0:
            return "estimated time till playback is **%s**" % datetime.timedelta(seconds=estimated_time)
        else:
            return "playing shortly!"


    def add(self, url, author, channel,title, duration,effect,thumb,search_query=None):
        entry = {'title':title,'duration': duration, 'url' : url,'author' : author,'channel' : channel,'lock':asyncio.Lock(),'effect': effect,
            'thumb':thumb, 'search_query' : title if not search_query else search_query}
        self.entries.append(entry)
        return entry, len(self.entries)


    # This handles each entry in the youtube playlist, somewhat
    # asynchronously, the playlist is iterated over and add_pl_entry
    # is called for each entry
    async def async_pl(self, url, author, channel):
        info = await self.bot.downloader.extract_info(self.bot.loop, url, download = False, process=False,retry_on_error=True)
        print(info)
        pltog = True
        sendpos = 0
        for item in info['entries']:
            try:
                post = await self.add_pl_entry(info['webpage_url'].split('playlist?list=')[0]+'watch?v=%s' % item['id'], author, channel)
                if pltog:
                    sendpos = post
                    pltog = False
            except:
                pass
        return sendpos

    async def add_pl_entry(self,url,author,channel):
        info = await self.bot.downloader.extract_info(self.bot.loop, url, download = False, process=False,retry_on_error=True)
        ent,pos = await self.add(info['webpage_url'], author, channel,info['title'],info['duration'],'None',info['thumbnails'][0]['url'])
        return pos
  

  
 
  