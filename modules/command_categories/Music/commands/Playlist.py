from modules.base.command import Command
from modules.music import player,playlist
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
from modules.utils.embedsender import send
from modules.utils.db import User
from modules.music import playlist
from modules.music import player as ply
import shlex
class Playlist(Command):
    name = "playlist"
    alts = ["pl","mylist"]
    helpstring ="""Save songs on the bot so you can listen to them anytime quickly, a personal playlist!
        Usage:
        <prefix>playlist [optional page no.]- shows your playlist
        <prefix>playlist add [song_number or 'np'] - adds the song from current queue with the song number or now playing song if 'np' is used
        <prefix>playlist dump - whole current queue is added to your playlist
        <prefix>playlist play [optional song number or range] - plays the song number from your playlist, if nothing is specified whole playlist is played
        <prefix>playlist reorder number>number - swap the places of the two numbers specified in your playlist
        <prefix>playlist delete [song_number] - deletes the song with that number on your list
        <prefix>playlist clear - clears your whole list
        """
    @staticmethod
    async def main(bot, message):
        try:
            player = bot.players[message.guild]
        except:
            player = None
        track_names = list()
        track_urls = list()
        printlines = {0 : []}
        nextline = str()
        d = bot.ses
        s = bot.ses
        uwu = bot.ses
        if len(shlex.split(message.content)) == 1 or not shlex.split(message.content)[1] in ['dump','add','clear','play','reorder']:
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                 if user.playlist == None:
                     await message.channel.send(":notes: Empty playlist")
                 else:
                     st = eval(user.playlist)
                     break
            for x in st.keys():
                track_names.append(st[x][0])
                track_urls.append(st[x][1])
            counter = 0
            for track in track_names:
                nextline = '%s. %s - [Link](%s)\n' % ((counter+1),str(track_names[counter]), track_urls[counter])
                currentlinesum = sum(len(x) + 1 for x in printlines[0])
                if currentlinesum + len(nextline) + 600 > 2000:
                    for pg in range(1,25):
                        try:
                            if sum(len(x) + 1 for x in printlines[pg]) + 800 > 2000:
                                continue
                            else:
                                printlines[pg].append(nextline)
                                break
                        except:
                            printlines[pg] = []
                            printlines[pg].append(nextline)
                            break
                else:
                    printlines[0].append(nextline)
                counter += 1
            if len(shlex.split(message.content)) == 1:
                pg_index = 1  #⬅  ➡
            else:
                pg_index = int(shlex.split(message.content)[1])
            total_pgs = len(printlines.keys())
            if pg_index < 1 or pg_index > total_pgs:
                await SMexHandler.handle(bot,ServerManPrettyException( "Your playlist only has %s page(s)!\nPlease a supply a value between 1 and %s." % (total_pgs,total_pgs),"Invalid Value!", message.channel))
                return
            if total_pgs == 1 and pg_index == 1:
                msg = ""
                msg = '\n\n'.join(printlines[0])
                await bmessage.channel.send('```py\n%s\nPage: 1/1\n```' % msg)
                return
            while True:
                msg = ""
                msg = '\n\n'.join(printlines[pg_index-1])
                try:
                    await q_msg.edit(content = """```py\n"%s's Playlist"\n%s\nPage: %s/%s\n```""" % (message.author.name,msg,pg_index,total_pgs))
                except:
                    q_msg = await message.channel.send("""```py\n"%s's Playlist"\n%s\nPage: %s/%s\n```""" % (message.author.name,msg,pg_index,total_pgs))
                if pg_index == 1:
                    await q_msg.add_reaction('➡')
                def chk(reaction, user):
                    return user == message.author and str(reaction.emoji) == '➡' and reaction.message == q_msg
                res,user = await bot.wait_for('reaction_add')
                if str(res.emoji) == '➡':
                    try:
                        await q_msg.remove_reaction('➡',message.author)
                    except:
                        pass
                    pg_index += 1
                    continue
                elif pg_index == total_pgs:
                    await q_msg.add_reaction('⬅')
                    def chk(reaction, user):
                        return user == message.author and str(reaction.emoji) == '⬅' and reaction.message == q_msg
                    res,user = await bot.wait_for('reaction_add')
                    if str(res.emoji) == '⬅':
                        try:
                            await q_msg.remove_reaction('⬅',message.author)
                        except:
                            pass
                    pg_index -= 1
                    continue
                else:
                    await q_msg.add_reaction('⬅')
                    await q_msg.add_reaction('➡')
                    def chk(reaction, user):
                        return user == message.author and str(reaction.emoji) in ['⬅','➡'] and reaction.message == q_msg
                    res,user = await bot.wait_for('reaction_add')
                    if str(res.emoji) == '⬅':
                        try:
                            await q_msg.remove_reaction('⬅',message.author)
                        except:
                            pass
                        pg_index -= 1
                        continue
                    elif str(res.emoji) == '➡':
                        try:
                            await q_msg.remove_reaction('➡',message.author)
                        except:
                            pass
                        pg_index += 1
                        continue
        elif shlex.split(message.content)[1].lower() == 'dump':
            full_deque = player.playlist.getlist()
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    if user.playlist is None:
                        lst = {}
                    else:
                        lst = eval(str(user.playlist))
            new_index = len(lst)
            player_dict={}
            try:
                new_index += 1
                player_dict[new_index]=list()
                player_dict[new_index].append(player.current_entry['title'])
                player_dict[new_index].append(player.current_entry['url'])
            except:
                pass
            for m in full_deque:
                new_index += 1
                player_dict[new_index]=list()
                player_dict[new_index].append(m['title'])
                player_dict[new_index].append(m['url'])
            lst.update(player_dict)
            await message.channel.send(":notes: Added the full queue to your playlist")
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    ex = User.__table__.update().where(User.id==user.id).values(playlist=str(lst))
                    d.execute(ex)
                    d.commit()
                    break
        elif shlex.split(message.content)[1].lower() == 'add':
            song_index = shlex.split(message.content)[2].lower()
            if len(song_index)>3:
                await message.channel.send("I never thought someone would make a playlist so big, but here you are, I just made a precautionary block for above 100, but well i might have to get rid of this, thanks, %s" % message.author.name)
                return
            if song_index == ('np'):
                m_title = player.current_entry['title']
                m_url = player.current_entry['url']
                await message.channel.send(":notes: Added **%s**, to your playlist!" % m_title)
            else:
                m = player.playlist.gettrack(int(song_index))
                m_title = m['title']
                m_url = m['url']
                await message.channel.send(":notes: Added **%s**, to your playlist!" % m_title)
            for user in d.query(User):
                if int(message.author.id) == user.id:
                    if user.playlist is None:
                        lst = {}
                    else:
                        lst = eval(str(user.playlist))
            new_index = len(lst)+1
            player_dict = {}
            player_dict[new_index]=list()
            player_dict[new_index].append(m_title)
            player_dict[new_index].append(m_url)
            lst.update(player_dict)
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    ex = User.__table__.update().where(User.id==user.id).values(playlist=str(lst))
                    d.execute(ex)
                    d.commit()
                    break
        elif shlex.split(message.content)[1] == 'clear':
            await message.channel.send(":put_litter_in_its_place: Cleared!")
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    ex = User.__table__.update().where(User.id==user.id).values(playlist='{}')
                    d.execute(ex)
                    d.commit()
                    break
        elif shlex.split(message.content)[1] == 'play':
            if not player:
                try:
                    vc = bot.vc_clients[message.guild]
                except:
                    vc = await message.author.voice.channel.connect(timeout=6,reconnect=True)
                    bot.vc_clients[message.guild] = vc
                pl = playlist.Playlist(bot)
                player = ply.Player(bot,vc, pl)
                bot.players[message.guild] = player
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    if user.playlist is None:
                        lst = {}
                    else:
                        lst = eval(str(user.playlist))
                    break
            for x in lst.keys():
                track_names.append(lst[x][0])
                track_urls.append(lst[x][1])
            if '-' in shlex.split(message.content)[2].lower():
                msg = shlex.split(message.content)[2]
                from_index = msg[:msg.find('-')]
                to_index = msg[msg.find('-')+1:]
                if not from_index.isdigit() and not to_index.isdigit():
                    await message.channel.send("Please provide the numbers from your playlist as start and end points")
                    return
                from_index = int(from_index)
                to_index = int(to_index)
                for play_index in range(from_index,to_index):
                    try:
                        info = await bot.downloader.extract_info(bot.loop, track_urls[play_index-1], download = False, process=False,retry_on_error=True)
                        entry, position = player.playlist.add(info['webpage_url'], message.author, message.channel,info['title'],info['duration'])
                    except:
                        pass
                if player.state == 'stopped':
                    bot.loop.create_task(player.prepare_entry())
                await message.channel.send(":notes: Queued songs from **%s-%s**, from your saved playlist" % (from_index, to_index))
            elif shlex.split(message.content)[2].lower()>0:
                if not shlex.split(message.content)[2].isdigit():
                    await message.channel.send("Please provide a number from your playlist to play")
                    return
                play_index = int(shlex.split(message.content)[2])
                await message.channel.send(":notes: Playing **%s**, from your saved playlist" % track_names[play_index-1])
                info = await bot.downloader.extract_info(bot.loop, track_urls[play_index-1], download = False, process=False,retry_on_error=True)
                entry, position = player.playlist.add(info['webpage_url'], message.author, message.channel,info['title'],info['duration'])
                if player.state == 'stopped':
                    await player.prepare_entry()
            else:
                await message.channel.send(":notes: Playing full playlist")
                for track in track_urls:
                    info = await bot.downloader.extract_info(bot.loop, track, download = False, process=False,retry_on_error=True)
                    entry, position = player.playlist.add(info['webpage_url'], message.author, message.channel,info['title'],info['duration'])
                    if player.state == 'stopped':
                        bot.loop.create_task(player.prepare_entry())
        elif shlex.split(message.content)[1] == 'reorder':
            song_index = shlex.split(message.content)[2]
            from_index = int(song_index.split('>')[0])
            to_index = int(song_index.split('>')[1])
            if len(song_index)>3:
                return
            for user in d.query(User):
                if int(message.author.id) == user.id:
                    if user.playlist is None:
                        lst = {}
                    else:
                        lst = eval(str(user.playlist))
            temp = lst[from_index]
            from_data = lst[to_index]
            to_data = temp
            player_dict = {}
            player_dict[from_index] = from_data
            player_dict[to_index] = to_data
            lst.update(player_dict)
            await message.channel.send("%s :arrows_counterclockwise: %s" % (from_index, to_index))
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    ex = User.__table__.update().where(User.id==user.id).values(playlist=str(lst))
                    d.execute(ex)
                    d.commit()
                    break
        elif shlex.split(message.content)[1] == 'delete':
            if not shlex.split(message.content)[2].isdigit():
                await message.channel.send("Please provide a number from your playlist to delete")
                return
            song_index = int(shlex.split(message.content)[2])
            for user in d.query(User):
                if int(message.author.id) == user.id:
                    if user.playlist is None:
                        lst = {}
                    else:
                        lst = eval(str(user.playlist))
            new_lst = lst
            deleted_name = new_lst[song_index][0]
            for x in range(song_index, len(lst)+1):
                if x == len(lst):
                    lst.pop(x, None)
                    break
                lst[x] = new_lst[x+1]
            await message.channel.send(":notes: **%s**, was deleted from your playlist." % deleted_name)
            for user in d.query(User):
                if int(message.author.id) == int(user.id):
                    ex = User.__table__.update().where(User.id==user.id).values(playlist=str(lst))
                    d.execute(ex)
                    d.commit()
                    break