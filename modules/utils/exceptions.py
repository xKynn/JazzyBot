import discord
class ServerManPrettyException(Exception):
 def __init__(self, msg, title, channel, color = 0xffffff):
  self._embed = discord.Embed()
  self._embed.add_field(name = title, value = msg, inline = True)
  self._embed.colour = color
  self._channel = channel
 @property
 def channel(self):
  return self._channel
 @property
 def embed(self):
  return self._embed 
 def __repr__(self):
  return "aa"
class ServerManHelpfulException(ServerManPrettyException):
 def __init__(self, msg, title, channel, solution):
  super().__init__(msg, title, channel)
  self._embed.add_field(name="Solution", value = solution, inline = True)