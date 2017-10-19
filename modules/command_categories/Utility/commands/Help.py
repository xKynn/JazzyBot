from modules.base.command import Command
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
from textwrap import dedent
import shlex
class Help(Command):
    name = "help"
    alts = []
    helpstring = "Get a general help message or specialized documents about commands."
    @staticmethod
    async def main(bot, message,url=None):
        args = shlex.split(message.content)
        if len(args) >1:
            u_command = args[1]
            for command_group in bot.cgroups:
                for command in command_group.commands:
                    if command.name == u_command or u_command in command.alts:
                        hlp = command.helpstring.replace('<prefix>',bot.prefix)
                        await message.channel.send("```\n{}```".format(dedent(hlp)))
                        return
        categories = {}
        for command_group in bot.cgroups:
            for command in command_group.commands:
                try:
                    liner = command.helpstring.split('\n')[0]
                except:
                    pass
                try:
                    categories[command_group.name].append('#%s (%s):\n\t%s' %(command.name,', '.join(command.alts), liner))
                except:
                    categories[command_group.name] = []
                    categories[command_group.name].append('#%s:\n\t%s' %(command.name, liner))
        send = False
        snmsg_str = str()
        for cat in list(categories.keys()):
            if cat != 'Owner':
                msg_str = '\n'.join(categories[cat])
                snmsg_str += "```Markdown\n@%s\n%s```" % (cat, msg_str)
                #snmsg_str = str()
        await message.author.send(snmsg_str)
        helpmsg3 = str()
        try:
            helpmsg3 += '\n\nPrefix for server `"%s"` is %s > `Example`: %shelp' % (message.guild.name,bot.prefix,bot.prefix)
        except:
            pass
        helpmsg3 += "\n\nYou can continue using help and some other commands here in the DMs"
        helpmsg3 += "\n\nUse `%shelp AnyCommandNameHere` :  to get more info on a specific command" % bot.prefix
        helpmsg3 += "\n\nYou can use this link to invite the bot to your server"
        url = 'https://discordapp.com/oauth2/authorize?client_id=362940471447912449&scope=bot&permissions=305196094'
        helpmsg3 +="\n%s" % url
        await message.author.send(helpmsg3)
        await message.add_reaction('✔')