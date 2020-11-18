import discord
import asyncio
from jishaku.codeblocks import codeblock_converter
from jishaku.modules import ExtensionConverter
from discord.ext import commands


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: codeblock_converter):
        jsk = self.bot.get_command("jishaku python")
        await jsk(ctx, argument=code)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *cogs: ExtensionConverter):
        jsk = self.bot.get_command("jishaku load")
        await jsk(ctx, *cogs)

    @commands.group()
    @commands.is_owner()
    async def dev(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Welcome to the Dev Menu. Use `{[c.name for c in ctx.command.commands]}` to look at those specific commands")

    @dev.group()
    async def util(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"`{[c.name for c in ctx.command.commands]}`")

    @util.command()
    async def shutdown(self, ctx):
        await ctx.send("Shutting Down!")
        await self.bot.db.close()
        await self.bot.logout()

    @util.command()
    async def restart(self, ctx, shard: int):
        """Restarts a shard"""
        shard = self.bot.get_shard(shard)
        await shard.reconnect()
        await ctx.send(f"Successfully restarted shard {shard.id}")

    @dev.group()
    async def override(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'`{[c.name for c in ctx.command.commands]}`')

    @override.command()
    async def prefix(self, ctx, *, prefix):
        if prefix:
            guild = await self.bot.db.fetch("SELECT * FROM guilds WHERE guild_id = $1 AND prefix = $2", ctx.guild.id, prefix)
            if not guild:
                await self.bot.db.execute("INSERT INTO guilds (guild_id, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
            guild = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guild_id = $1 AND prefix = $2", ctx.guild.id, prefix)
            await self.bot.db.execute("UPDATE guilds SET prefix = $1 WHERE guild_id = $2", guild['prefix'], ctx.guild.id)
            await ctx.send(f"Prefix change to {prefix}")
        else:
            await ctx.send("Please provide a prefix you want to change to.")

    @override.command()
    async def leave(self, ctx):
        message = await ctx.send("Are you sure you want to remove me from this server type `y` to proceed")

        def check(m):
            return m.content == 'y' and m.author == ctx.author

        try:
            await self.bot.wait_for('message', check=check, timeout=20.0)
            await ctx.send("Thanks for using MEE7!")
            await ctx.guild.leave()
        except asyncio.TimeoutError:
            await message.edit(content="Timed Out")

    @override.command()
    async def schannel(self, ctx, channel: discord.TextChannel):
        schannel = await self.bot.db.fetch("SELECT * FROM schannel WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
        if not schannel:
            await self.bot.db.execute("INSERT INTO schannel (guild_id, channel_id) VALUES ($1, $2)", ctx.guild.id, channel.id)
        schannel = await self.bot.db.fetchrow("SELECT * FROM schannel WHERE guild_id = $1 AND channel_id = $2",
                                              ctx.guild.id, channel.id)
        await self.bot.db.execute("UPDATE schannel SET channel_id = $1 WHERE guild_id = $2", schannel["channel_id"],
                                  ctx.guild.id)
        await ctx.send(f"Suggestion channel is now {channel.mention}")

    @override.command()
    async def schandisable(self, ctx):
        """Disables the suggestion system"""
        schannel = await self.bot.db.fetch("SELECT * FROM schannel WHERE guild_id = $1",
                                           ctx.guild.id)
        if not schannel:
            await ctx.send("You can't disable the suggestion system when there is no suggestion channel")
        await self.bot.db.execute("UPDATE schannel SET channel_id = $1 WHERE guild_id = $2", 0,
                                  ctx.guild.id)
        await ctx.send(f"Suggestions is now disabled")


def setup(bot):
    bot.add_cog(Dev(bot))
