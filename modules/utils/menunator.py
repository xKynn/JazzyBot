import asyncio
import discord
import aiohttp
from modules.utils.exceptions import ServerManPrettyException
from modules.utils.exceptionhandler import SMexHandler
class MenuNator:
 @staticmethod
 async def listmenu(bot, message, optionlist, title, subtext, timeout = None,returnmode='index'):
  print("menu")
  msg = "```py\n"
  for number, option in enumerate(optionlist):
   msg += "{0}. {1}\n".format(number+1, option)
  msg += "\n\nType 'exit' to leave the menu\n```"
  def check(m):
   return m.author == message.author and m.channel == message.channel
  s_msg = await bot.send_message(message.channel,msg)
  response = await bot.wait_for_message(check = check, timeout = timeout)
  await bot.delete_message(s_msg)
  try:
   if response.content.lower() == 'exit':
    return
   if returnmode == 'index':
    x = optionlist[int(response.content)-1]
    return int(response.content)-1
   else:
    a = optionlist[int(response.content)-1]
    return a
  except:
   print("exception")
   await SMexHandler.handle(bot,ServerManPrettyException("Invalid Option!", "Error!", message.channel))
  
 @staticmethod
 async def checklist(bot, author, channel, optionlist, title, subtext, timeout = None):
  msg = "```py\n"
  optiondictlist = []
  for option in optionlist:
   x = {'option' : option, 'selected' : False}
   optiondictlist.append(x)
  for number, option in enumerate(optiondictlist):
   if option['selected'] == True:
    msg += "{2}	{0}. {1}\n".format(number+1, option['option'],'✅')
   else:
    msg += "{2}	{0}. {1}\n".format(number+1, option['option'],'⬜')
  msg += "\n```"
  def check(m):
   return m.author == author and m.channel == channel
  s_msg = await channel.send(msg)
  response = await bot.wait_for('message', check = check, timeout = timeout)
  try:
   val = optiondictlist[int(response.content)-1]
  except:
   await SMexHandler.handle(bot, channel,ServerManPrettyException("Invalid Option!", "Error!", channel))
   pass
  while response.content.lower() != "ok":
   try:
    val = optiondictlist[int(response.content)-1]
   except:
    await SMexHandler.handle(bot, channel,ServerManPrettyException("Invalid Option!", "Error!", channel))
    response = await bot.wait_for('message', check = check, timeout = timeout)
    continue
   if optiondictlist[int(response.content)-1]['selected'] == True:
    optiondictlist[int(response.content)-1]['selected'] = False
   else:
    optiondictlist[int(response.content)-1]['selected'] = True
   msg = "```py\n"
   for number, option in enumerate(optiondictlist):
    if option['selected'] == True:
     msg += "{2}	{0}. {1}\n".format(number+1, option['option'],'✅')
    else:
     msg += "{2}	{0}. {1}\n".format(number+1, option['option'],'⬜')
   msg += "\n```"
   await s_msg.edit(content = msg)
   response = await bot.wait_for('message', check = check, timeout = timeout)
   
  optionlist = []
  for option in optiondictlist:
   if option['selected'] == True:
    optionlist.append(option['option'])
  await s_msg.delete()
  return optionlist
# @staticmethod
# async def dialogue(bot
  
 