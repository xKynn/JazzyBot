from modules.base.command import Command
from modules.utils.db import ServerData
import shlex
class SetPrefix(Command):
    name = "setprefix"
    alts = ["prefix"]
    helpstring ="""Change the command prefix of the bot on a server, if mod and admin roles are set, only an admin can do this. Prefix by default is supposed to be ;
        Usage Example:
        <prefix>setlocalprefix !
   	 """
    @staticmethod
    async def main(bot, message, user_mentions):
        edited = False
        stripcommand=shlex.split(message.content)[1]
        if len(stripcommand.strip(" ")) == 0:
            await message.channel.send("Supply a prefix after the command For ex. '%ssetlocalprefix !' " % bot.prefix)
            return
        else:
            for qserver in bot.ses.query(ServerData):
                sid = qserver.server_id
                if int(message.guild.id) == int(sid):
                    ex = ServerData.__table__.update().where(ServerData.server_id==sid).values(server_prefix=stripcommand.strip(" "))
                    bot.ses.execute(ex)
                    bot.ses.commit()
        await message.channel.send('```New Bot Prefix is: %s\n Usage: %scommand```' % (stripcommand.strip(" "),stripcommand.strip(" ")))