from modules.base.command import Command
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
import shlex
class Clean(Command):
    name = "clean"
    alts = ['cln']
    helpstring ="""Removes up to [range] messages the bot has posted in chat. Default: 50, Max: 1000
       Usage:
           <prefix>clean [range]
       """
    @staticmethod
    async def main(bot, message):
        try:
            search_range = min(int(shlex.split(message.content)[1]),1000)
        except:
            search_range = 1000
        await message.delete()
        def check(message):
            return message.author == bot.user or message.content.startswith(bot.prefix)
        if bot.user.bot:
            if message.channel.permissions_for(message.guild.me).manage_messages:
                try:
                    deleted = await message.channel.purge(check=check, limit=search_range, before=message)
                except:
                    await message.channel.send("Messages older than 14 days couldn't be bulk deleted in regard to a discord limitation")
                await message.channel.send('Cleaned up %s message(s).' % deleted)
        else:
            deleted = 0
            async for msg in message.channel.history(search_range, before=message):
                if msg.author == bot.user or msg.content.startswith(bot.prefix):
                    bot.loop.create_task(msg.delete())
                    deleted += 1
                    await asyncio.sleep(0.25)
            await message.channel.send('Cleaned up %s message(s).' % deleted)

