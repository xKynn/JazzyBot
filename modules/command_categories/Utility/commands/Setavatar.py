from modules.base.command import Command
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
class Setavatar(Command):
    name = "setava"
    alts = ["setavatar"]
    helpstring = "Let the 8ball answer all your queries\nUsage:\n<prefix>8ball questionhere"
    @staticmethod
    async def main(bot, message,url=None):
        if message.attachments:
            thing = message.attachments[0]['url']
        else:
            thing = url.strip('<>')
        try:
            with aiohttp.Timeout(10):
                async with bot.aiosession.get(thing) as res:
                    await bot.user.edit(avatar=await res.read())
        except Exception as e:
            await SMexHandler.handle(bot, channel,ServerManPrettyException("Wasn't able to change avatar!", "Error!", channel)) 
        await message.channel.send(":ok_hand:")
