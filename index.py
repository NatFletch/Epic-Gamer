import discord
import asyncpg
import traceback
import tracemalloc as tm
from os import environ as e
from secret import token, password
from discord.ext import commands

e["JISHAKU_NO_UNDERSCORE"] = "True"
tm.start()
intents = discord.Intents.all()
extensions = ["extensions.fun", "extensions.help", "extensions.mod", "extensions.utility", "extensions.logs", "extensions.developer",
              "extensions.config", "extensions.eco", "extensions.manipulation", "extensions.modmail", "extensions.utils.error"]


class EpicContext(commands.Context):
    async def open_wallet(self, member=None):
        if member is None:
            member = self.author.id
        account = await self.bot.db.fetchrow("SELECT * FROM money WHERE user_id = $1", member)
        return account['amount']

    async def add_money(self, amount, member=None):
        if member is None:
            member = self.author.id
        bal = await self.open_wallet(member)
        await self.bot.db.execute("UPDATE money SET amount = $1 WHERE user_id = $2", bal + amount, member)

    async def subtract_money(self, amount, member=None):
        if member is None:
            member = self.author.id
        bal = await self.open_wallet(member)
        await self.bot.db.execute("UPDATE money SET amount = $1 WHERE user_id = $2", bal - amount, member)

    async def set_money(self, amount, member=None):
        if member is None:
            member = self.author.id
        await self.bot.db.execute("UPDATE money SET amount = $1 WHERE user_id = $2", amount, member)


class EpicGamer(commands.AutoShardedBot):
    async def get_context(self, message, *, cls=EpicContext):
        return await super().get_context(message, cls=cls)

    def __init__(self):
        super().__init__(command_prefix=EpicGamer.get_prefix, case_insensitive=True, help_command=None, shard_count=1, intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name=";help"), status=discord.Status.dnd)
        self.db = self.loop.run_until_complete(asyncpg.create_pool(database='MEE7Data', user='postgres', password=password))
        self.load_extension("jishaku")
        for extension in extensions:
            self.load_extension(extension)

    async def get_prefix(bot, message):
        if message.guild is not None:
            connection = await asyncpg.connect(database="MEE7Data", user="postgres", password=password)
            guild = await connection.fetchrow("SELECT * FROM guilds WHERE guild_id = $1", message.guild.id)
            await connection.close()
            if not guild:
                return commands.when_mentioned_or(';')(bot, message)
            return commands.when_mentioned_or(guild['prefix'])(bot, message)

    async def on_ready(self):
        print(f"Epic Gamer is up and running at {round(self.latency * 1000)}ms")

    async def close(self):
        await self.db.close()
        print("DB Closed")
        await super().close()


if __name__ == "__main__":
    EpicGamer().run(token)
