from discord.ext import commands
from discord import Intents
from enka import GenshinClient

import asyncio, aiosqlite

from config import DiscordConfig, EnkaConfig

class HeizouBot(commands.Bot):
    def __init__(self, api: GenshinClient, db: aiosqlite.Connection) -> None:
        command_prefix = DiscordConfig.command_prefix
        owner_ids = DiscordConfig.owner_ids
        intents = Intents.all()

        super().__init__(command_prefix=command_prefix, owner_ids=owner_ids, intents=intents)
        self.db: aiosqlite.Connection = db
        self.db.row_factory = aiosqlite.Row
        self.api: GenshinClient = api
    
    async def on_ready(self) -> None:
        assert self.user is not None
        print(f"Online as {self.user} ({self.user.id})")

async def main():
    async with aiosqlite.connect("db.db") as db, GenshinClient(headers={"User-Agent": EnkaConfig.useragent}) as api, HeizouBot(api, db) as bot:

        for cog in DiscordConfig.cogs:
            await bot.load_extension(cog)
        
        try: 
            await bot.start(DiscordConfig.TOKEN)
        except (asyncio.exceptions.CancelledError,KeyboardInterrupt):
            pass
        except Exception as e:
            print(e)
        finally: 
            await bot.db.close()
    
asyncio.run(main())