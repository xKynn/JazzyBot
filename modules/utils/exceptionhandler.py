import discord
import asyncio
class SMexHandler:

 @staticmethod
 async def handle(bot, exc):
  await exc.channel.send(embed = exc.embed)