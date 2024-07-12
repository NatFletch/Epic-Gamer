import discord
import asyncpg
import traceback
import tracemalloc as tm
from os import environ as e
from secret import token, password, username, db_name
from discord.ext import commands

e["JISHAKU_NO_UNDERSCORE"] = "True"
tm.start()
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


class EpicGamer(commands.Bot):
    async def get_context(self, message, *, cls=EpicContext):
        return await super().get_context(message, cls=cls)

    def __init__(self):
        super().__init__(
            command_prefix=EpicGamer.get_prefix,
            case_insensitive=True,
            help_command=None,
            intents=discord.Intents.all(),
            activity=discord.Activity(type=discord.ActivityType.listening, name=";help"),
            status=discord.Status.dnd
        )

    async def get_prefix(bot, message):
        if message.guild is not None:
            guild = await bot.db.fetchrow("SELECT * FROM guilds WHERE guild_id = $1", message.guild.id)
            if not guild:
                return commands.when_mentioned_or(';')(bot, message)
            return commands.when_mentioned_or(guild['prefix'])(bot, message)

    async def on_ready(self):
        print(f"Epic Gamer is up and running at {round(self.latency * 1000)}ms")

    async def setup_db(self, conn):
        await conn.execute(
                        '''
                           CREATE TABLE IF NOT EXISTS guilds (guild_id bigint, prefix text);
                           CREATE TABLE IF NOT EXISTS money (amount bigint, user_id bigint);
                           CREATE TABLE IF NOT EXISTS warnings (server_id bigint, case_id serial, user_id bigint, reason text, moderator bigint)
                        '''
                    )

    async def setup_hook(self):
        self.db = await asyncpg.create_pool(database=db_name, user=username, password=password)
        await self.setup_db(self.db)
        await self.load_extension("jishaku")
        for extension in extensions:
            await self.load_extension(extension)

    async def close(self):
        await self.db.close()
        print("DB Closed")
        await super().close()


if __name__ == "__main__":
    EpicGamer().run(token)
