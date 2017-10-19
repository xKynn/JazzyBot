import discord
async def send(bot,title, value, color,channel):
 em = discord.Embed(color = color)
 em.add_field(name = title, value = value)
 await channel.send(embed = em)
 