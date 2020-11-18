import discord
import aiosqlite
import sqlite3
from discord.ext import commands


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(hidden=True)
    async def setup(self, ctx):
        await ctx.send("Setting up your server...")
        con = sqlite3.connect('server-config.db')
        c = con.cursor()
        c.execute(f"""CREATE TABLE {ctx.guild.id} (
                    prefix text)""")
        con.commit()
        con.close()

    @commands.command(hidden=True)
    async def prefix(self, ctx, prefix):
        async with aiosqlite.connect('prefixes.sqlite') as db:
            await db.execute(f"INSERT INTO {ctx.guild.id} ({prefix})")
            await ctx.send(f"Prefix has been changed to {prefix}")


def setup(bot):
    bot.add_cog(Config(bot))
