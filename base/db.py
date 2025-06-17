
import asyncio, aiosqlite
from typing import Any, Iterable, Optional

# yes i know a lot of boilerplate code, i'll figure out how to compress all of it without too much risk later :tm:
# it's all just wraps around basic sql stuff because i do not trust myself with not screwing it up in other files
class DB:
    tables = ["users", "leaderboards", "builds", "scores", "verification", "settings"]
    def __init__(self, path: str, event_loop: asyncio.EventLoop) -> None:
        self.path = path
        asyncio.ensure_future(self.__ainit__(), loop=event_loop)

    async def __ainit__(self) -> None:
        self.db = await aiosqlite.connect(self.path)
        await self._install()
    
    async def _install(self) -> None:
        data = [
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, did INTEGER);",
            "CREATE TABLE IF NOT EXISTS leaderboards(id INTEGER PRIMARY KEY, name TEXT, description TEXT);",
                    
            ("CREATE TABLE IF NOT EXISTS builds(id INTEGER PRIMARY KEY, uid INTEGER, name TEXT, "
            "build TEXT, FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE);"),
                    
            ("CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY, uid INTEGER, lid INTEGER, "
            "score INTEGER, weapon TEXT, scores TEXT, bid INTEGER, "
            "FOREIGN KEY (lid) REFERENCES leaderboards(id) ON DELETE CASCADE, "
            "FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE, "
            "FOREIGN KEY (bid) REFERENCES build(id) ON DELETE CASCADE);"),
                    
            "CREATE TABLE IF NOT EXISTS verification(uid INTEGER PRIMARY KEY, did INTEGER, code TEXT);",
            "CREATE TABLE IF NOT EXISTS settings(name TEXT, value TEXT);"
        ]
        
        for x in data:
            await self.db.execute(x)
        await self.db.commit()
        
        return
    
    async def add_user(self, uid: int, name: str, did: int) -> None:
        await self.db.execute("INSERT INTO users (id, name, did) VALUES (?, ?, ?);", (uid, name, did))
        await self.db.commit()
        return
    
    async def add_unverified(self, uid: int, did: int, code: str) -> None:
        await self.db.execute("INSERT INTO verification (uid, did, code) VALUES (?, ?, ?);", (uid, did, code))
        await self.db.commit()
        return

    async def add_lb(self, name: str, desc: str) -> None:
        await self.db.execute("INSERT INTO leaderboards (name, description) VALUES (?, ?);", (name, desc))
        await self.db.commit()
        return
    
    async def add_build(self, uid: int, name: int, build: str) -> None:
        await self.db.execute("INSERT INTO builds (uid, name, build) VALUES (?, ?, ?);", (uid, name, build))
        await self.db.commit()
        return
    
    async def add_setting(self, name: str, value: str) -> None:
        await self.db.execute("INSERT INTO settings(name, value) VALUES (?, ?);", (name, value))
        await self.db.commit()
        return

    async def fetch_lb(self, name: str) -> aiosqlite.Row:
        out = await self.db.execute("SELECT * FROM leaderboards WHERE name = ?;", (name,))
        lb = await out.fetchone()
        if lb is None: raise
        return lb
    
    async def fetch_by_did(self, did: int) -> Iterable[aiosqlite.Row]:
        out = await self.db.execute("SELECT * FROM users WHERE did = ?;", (did,))
        users = await out.fetchall()
        if users is None: raise
        return users
    
    async def fetch_user(self, uid: int) -> aiosqlite.Row:
        out = await self.db.execute("SELECT * FROM users WHERE uid = ?;", (uid,))
        users = await out.fetchone()
        if users is None: raise
        return users
    
    async def fetch_score(self, lbid: int) -> Iterable[aiosqlite.Row]:
        res = await self.db.execute("SELECT uid, MAX(score) as mscore, weapon, bid FROM scores WHERE lid = ? GROUP BY uid ORDER BY mscore DESC;", (lbid,))
        out = await res.fetchall()
        if out is None: raise
        return out