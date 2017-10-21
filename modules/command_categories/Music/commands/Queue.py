from datetime import timedelta
from modules.base.command import Command
from modules.music import player
from modules.music import playlist
from modules.utils.exceptionhandler import SMexHandler
class Queue(Command):
    name = "queue"
    alts = ["list","q"]
    helpstring ="""Lists the current song queue.
           Usage:
               <prefix>queue
           """
    @staticmethod
    async def main(bot, message):
        player = bot.players[message.guild]
        channel = message.channel
        server = message.guild
        author = message.author
        printlines = {0 : []}
        lines = []
        for i, item in enumerate(player.playlist, 1):
            nextline = '{}. {} added by {}\n'.format(i, item['title'], item['author'].name).strip()
            if item == player.current_entry:
                ps = player.progress
                pt = player.current_entry['duration']
                song_progress = str(timedelta(seconds=ps)).lstrip('0').lstrip(':')
                song_total = str(timedelta(seconds=pt)).lstrip('0').lstrip(':')
                prog_str = '[ %s / %s ]' % (song_progress, song_total)
                nextline = "@" + nextline + ' - Currently Playing - ' + prog_str
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
                        printlines[pg].append('```py')
                        printlines[pg].append(nextline)
                        break
            else:
                printlines[0].append(nextline)
        if not printlines[0]:
            printlines[0].append(
                'Empty queue! Queue something with {}play.'.format(bot.prefix))
        if len(message.content.split()) == 1:
            pg_index = 1  #⬅  ➡
        else:
            pg_index = message.content.split()[1]
        if not isinstance(pg_index,int):
            return
        pg_index = int(pg_index)
        total_pgs = len(printlines.keys())
        if pg_index < 1 or pg_index > total_pgs:
            await SMexHandler.handle(bot,ServerManPrettyException( "Your playlist only has %s page(s)!\nPlease a supply a value between 1 and %s." % (total_pgs,total_pgs),"Invalid Value!", message.channel))
            return
        if pg_index == 1 and total_pgs == 1:
            msg = ""
            msg = '\n'.join(printlines[0])
            try:
                if bot.autoplay[player]:
                    msg += '\n`Autoplay is Currently On`'
            except:
                pass
            await channel.send('```py\n%s\n\nPage: 1/1\n```' % msg)
            return
        while True:
            msg = ""
            msg = '\n'.join(printlines[pg_index-1])
            try:
                if bot.autoplay[player]:
                    msg += '\n`Autoplay is Currently On`'
            except:
                pass
            try:
                await q_msg.edit(content = "```py\n%s\n\nPage: %s/%s\n``` " % (msg,pg_index,total_pgs))
            except:
                q_msg = await channel.send("```py\n%s\nPage: %s/%s\n``` " % (msg,pg_index,total_pgs))
            if pg_index == 1:
                await q_msg.add_reaction('➡')
                def chk(reaction, user):
                    return user == message.author and str(reaction.emoji) == '➡' and reaction.message == q_msg
                res,user = await bot.wait_for('reaction_add')
                if str(res.emoji) == '➡':
                    pg_index += 1
                    continue
            elif pg_index == total_pgs:
                await q_msg.add_reaction('⬅')
                def chk(reaction, user):
                    return user == message.author and str(reaction.emoji) == '⬅' and reaction.message == q_msg
                res,user = await bot.wait_for('reaction_add')
                if str(res.emoji) == '⬅':
                    pg_index -= 1
                    continue
                else:
                    await q_msg.add_reaction('⬅')
                    await q_msg.add_reaction('➡')
                    def chk(reaction, user):
                        return user == message.author and str(reaction.emoji) in ['⬅','➡'] and reaction.message == q_msg
                    res,user = await bot.wait_for('reaction_add')
                    if str(res.emoji) == '⬅':
                        pg_index -= 1
                        continue
                    elif str(res.emoji) == '➡':
                        pg_index += 1
                        continue