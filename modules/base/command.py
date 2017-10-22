from abc import ABC, abstractmethod


class Command(ABC):
    name = str()
    alts = list()
    oneliner = str()
    help = str()
    examples = str()
    options = str()

    @abstractmethod
    async def main(*args, **kwargs):
        pass
