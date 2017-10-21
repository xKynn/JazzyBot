import discord

from modules.base.command import Command
class Join(Command):
    name = "join"
    alts = ["summon","init"]
    oneliner = "Manually call the bot to your voice channel"
    help = "You can alternatively just use `<prefix>play songname` which will also summon the bot\nUntill the first track is requested a lot of the player features cannot be used."
    examples = "`<prefix>join`"
    options = "None"

    @staticmethod
    async def main(bot, message):
        np_embed = discord.Embed(title = 'Connecting...' , colour=0xffffff )
        np_embed.set_thumbnail(url = 'https://i.imgur.com/DQrQwZH.png')
        trying_msg = await message.channel.send(embed = np_embed)
        if not message.author.voice.channel:
            np_embed = discord.Embed(title = 'Error',description = 'You are not in a voice channel' , colour=0xffffff )
            np_embed.set_thumbnail(url = 'https://imgur.com/B9YlwWt.png')
            await trying_msg.edit(embed=np_embed)
            return
        try:
            vc = await message.author.voice.channel.connect(timeout=6,reconnect=True)
        except:
            np_embed = discord.Embed(title = 'Error', colour=0xffffff )
            np_embed.set_thumbnail(url = 'https://imgur.com/B9YlwWt.png')
            await trying_msg.edit(embed=np_embed)
            return
        bot.vc_clients[message.guild] = vc
        np_embed = discord.Embed(title = 'Bound to ' + message.author.voice.channel.name , description = 'summoned by **%s**' % message.author.mention, colour=0xffffff )
        np_embed.set_thumbnail(url = 'https://imgur.com/F95gtPV.png')
        await trying_msg.edit(embed = np_embed)