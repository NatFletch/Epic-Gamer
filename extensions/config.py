import discord
from secret import password
from discord.ext import commands


class Config(commands.Cog):
    """Commands that change the server settings. All commands either require manage server permissions or administrator"""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `Administrator`")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix=None):
        """Sets the prefix for your server. Requires administrator or owner"""
        if prefix:
            guild = await self.bot.db.fetch("SELECT * FROM guilds WHERE guild_id = $1 AND prefix = $2", ctx.guild.id, prefix)
            if not guild:
                await self.bot.db.execute("INSERT INTO guilds (guild_id, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
            guild = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guild_id = $1 AND prefix = $2", ctx.guild.id, prefix)
            await self.bot.db.execute("UPDATE guilds SET prefix = $1 WHERE guild_id = $2", guild['prefix'], ctx.guild.id)
            await ctx.send(f"Prefix changed to {prefix}")
        else:
            await ctx.send("Please provide a prefix you want to change to.")


async def setup(bot):
    await bot.add_cog(Config(bot))