from discord.ext import commands
from discord import Intents
from enka import GenshinClient

import asyncio

from config import DiscordConfig, EnkaConfig
from base import db

class HeizouBot(commands.Bot):
    def __init__(self, api: GenshinClient) -> None:
        command_prefix: list[str] = DiscordConfig.command_prefix
        owner_ids: list[int] = DiscordConfig.owner_ids
        intents: Intents = Intents.all()

        super().__init__(command_prefix=command_prefix, owner_ids=owner_ids, intents=intents)
        self.api: GenshinClient = api
        self.db: db.DB | None = None
    
    async def on_ready(self) -> None:
        assert self.user is not None
        print(f"Online as {self.user} ({self.user.id})")

async def main():
    async with GenshinClient(headers={"User-Agent": EnkaConfig.useragent}) as api, HeizouBot(api) as bot:

        for cog in DiscordConfig.cogs:
            await bot.load_extension(cog)
        
        bot.db = db.DB("db.db", bot.loop)

        try: 
            await bot.start(DiscordConfig.TOKEN)
        except Exception as e:
            print(e)
        finally: 
            await bot.db.close()
    
asyncio.run(main())