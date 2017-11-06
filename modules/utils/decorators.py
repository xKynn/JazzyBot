import time
import discord
from functools import wraps


def ratelimit(func):
    @wraps(func)
    async def wrapper(bot, message, *args, **kwargs):
        orig_msg = message
        print(round(time.time()))
        try:
            isRL = bot.RLdata[orig_msg.author]['isRL']
            prev_uses = bot.RLdata[orig_msg.author][func]['uses']
            prev_time = bot.RLdata[orig_msg.author][func]['lastusage']
            if isRL == 1 and round(time.time()) - prev_time <= 10:
                return await bot._deny(orig_msg)
            elif isRL == 1:
                bot.RLdata[orig_msg.author][func]['lastusage'] = round(time.time())
                bot.RLdata[orig_msg.author][func]['uses'] = 1
                bot.RLdata[orig_msg.author]['isRL'] = 0
                return await func(bot, message, *args, **kwargs)
            if round(time.time()) - prev_time <= 9 and prev_uses + 1 >= 4:
                print('deny usage exc')
                bot.RLdata[orig_msg.author]['isRL'] = 1
                return await bot._deny(orig_msg)
            elif round(time.time()) - prev_time <= 9:
                print('add to counter')
                bot.RLdata[orig_msg.author][func]['lastusage'] = round(time.time())
                bot.RLdata[orig_msg.author][func]['uses'] = prev_uses + 1
                return await func(bot, message, *args, **kwargs)
            else:
                print('counter reset')
                bot.RLdata[orig_msg.author][func]['lastusage'] = round(time.time())
                bot.RLdata[orig_msg.author][func]['uses'] = 1
                return await func(bot, message, *args, **kwargs)
        except KeyError:
            print('created')
            bot.RLdata[orig_msg.author] = {}
            bot.RLdata[orig_msg.author][func] = {}
            bot.RLdata[orig_msg.author][func]['lastusage'] = round(time.time())
            bot.RLdata[orig_msg.author][func]['uses'] = 1
            bot.RLdata[orig_msg.author]['isRL'] = 0
            return await func(bot, message, *args, **kwargs)

    return wrapper


def needsvoice(func):
    @wraps(func)
    async def wrapper(bot, message, *args, **kwargs):
        orig_msg = message
        print(orig_msg)
        if orig_msg.guild in bot.vc_clients:
            try:
                if orig_msg.author.voice.channel == orig_msg.guild.voice_client.channel:
                    return await func(bot, message, *args, **kwargs)
            except AttributeError:
                pass
            error_embed = discord.Embed(title='Error', description="You need to be in the bot's voice channel to use "
                                                                   "this command!", colour=0xffffff)
            error_embed.set_thumbnail(url='https://imgur.com/B9YlwWt.png')
            return await orig_msg.channel.send(embed=error_embed)
        else:
            return await func(bot, message, *args, **kwargs)

    return wrapper
