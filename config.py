import dotenv
dotenv.load_dotenv(".env")
import os
import aiosqlite

class DiscordConfig:
    DEBUG: bool = os.environ.get("DEBUG", 0)
    TOKEN: str = os.environ.get("TOKEN") if not DEBUG else os.environ.get("TOKEN_DEBUG")
    command_prefix: list[str] = os.environ.get("PREFIX").split(",") if not DEBUG else os.environ.get("PREFIX_DEBUG").split(",")
    cogs: list[str] = ["jishaku"]
    owner_ids: list[str] = os.environ.get("OWNERS").split(",")

    db: aiosqlite.Connection = aiosqlite.connect("db.db")
    db.row_factory = aiosqlite.Row

class EnkaConfig:
    useragent: str = os.environ.get("USERAGENT")
    char_id: int = os.environ.get("CHAR_ID")