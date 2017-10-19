import asyncio
import discord
import aiohttp
import traceback
from abc import ABC, abstractmethod
class Command(ABC):
  helpstring = str()
  name = str()
  alts = list()

  @abstractmethod
  async def main():
   pass