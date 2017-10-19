async def ytsearch(bot,message, song_name):
   info = await bot.downloader.extract_info(bot.loop, 'ytsearch4:'+song_name, download = False, process=True,retry_on_error=True)
   output = []
   for a,b in enumerate(info['entries'], 1):
    output.append('{}. {}'.format(a, b['title']))
   outputlist = '\n'.join(map(str,output))
   outputlist = '```py\n' + outputlist + '\n' + '#Choose the appropriate result number or type exit to leave the menu\n' + '```'
   sent_msg = await message.channel.send(outputlist)
   def check(m):
      return m.author == message.author and m.channel == message.channel
   while True:
      response_msg = await bot.wait_for('message',check=check,timeout=30)
      if response_msg.content.lower() == 'exit':
       await sent_msg.delete()
       return
      try:
       chosen_number = int(response_msg.content) - 1
       chosen_song = info['entries'][chosen_number]
       break
      except:
       em = discord.Embed(title=':exclamation: Invalid choice', colour = 0xff3a38)
       await message.channel.send(embed = em)
   await sent_msg.delete()
   return chosen_song
