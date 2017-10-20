import asyncio
import discord
import aiohttp
import traceback
from abc import ABC
class Category(ABC):
    name = str()
    commands = []