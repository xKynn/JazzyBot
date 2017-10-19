from modules.base.command import Command
from modules.utils.decorators import needsvoice
class Skip(Command):
    name = "skip"
    alts = ["sk"]
    helpstring ="""Skips the current song when enough votes are cast. (50% votes)
           Usage:
               <prefix>skip
           """
    @staticmethod
    @needsvoice
    async def main(bot, message):
      player = bot.players[message.guild]
      if not player.voice_client.is_playing():
          await message.channel.send("Nothing is playing to skip!")
      else:
          if player.current_entry['author'] == message.author:
              await message.channel.send("**%s** was skipped by it's author, %s!" % (player.current_entry['title'], player.current_entry['author']))
              player.voice_client.stop()
          else:
              if not message.author in player.skip_votes:
                  num_voice = sum(1 for m in message.author.voice.channel.members if not (
                  m.voice.deaf or m.voice.self_deaf or m.id == bot.user.id))
                  player.skip_votes.append(message.author)
                  current_votes = len(player.skip_votes)
                  required_votes = round(num_voice*(2/3))
                  await message.channel.send("Your vote was added!\n**%s/%s** skip votes recieved, song will be skipped upon meeting requirements" %(current_votes, required_votes))
                  if current_votes >= required_votes:
                      await message.channel.send("**%s** was skipped upon meeting skip vote requirements!" % player.current_entry['title'])
                      player.voice_client.stop()
                  else:
                      await message.channel.send("You have already voted to skip **%s**, wait till more votes arrive!" % player.current_entry['title'])