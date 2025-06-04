import dotenv
dotenv.load_dotenv(dotenv_path=".env")
import os

class DiscordConfig:
    DEBUG: bool = bool(os.environ.get("DEBUG", False))
    TOKEN: str = os.environ.get("TOKEN", "") if not DEBUG else os.environ.get("TOKEN_DEBUG", "")
    command_prefix: list[str] = os.environ.get("PREFIX","").split(",") if not DEBUG else os.environ.get("PREFIX_DEBUG","").split(",")
    cogs: list[str] = ["jishaku"]
    owner_ids: list[int] = list(map(int, os.environ.get("OWNERS","").split(",")))

class EnkaConfig:
    useragent: str = os.environ.get("USERAGENT", "")
    char_id: int = int(os.environ.get("CHAR_ID", 0))