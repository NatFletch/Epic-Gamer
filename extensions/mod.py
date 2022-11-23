import discord
import typing
import secret
import re
import aiohttp
from discord.ext import commands


class Moderation(commands.Cog):
    """Useful moderator commands that can come in handy"""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `Manage Messages`", aliases=["strike"])
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member, *, reason: typing.Optional[str]):
        """Warns a user in the guild"""
        if member == ctx.author:
            await ctx.send("I am not sure you want to do that")
        guild = await self.bot.db.fetch("SELECT * FROM warnings WHERE server_id = $1", ctx.guild.id)
        case_id = 0
        case_id += guild['case_id']
        await self.bot.db.execute("INSERT INTO warnings (server_id, case_id, user, reason, moderator) VALUES ($1, $2, $3, $4, $5)", ctx.guild.id, case_id, member.id, reason, ctx.author.id)
        await ctx.send(f"{member} has been warned for: {reason}")
        embed = discord.Embed(title="Warning!", description=f"You have been warned in {ctx.guild.name}\n**Reason:** {reason}\n**Moderator:** {ctx.author}", color=0xff0000)
        await member.send(embed=embed)

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `Ban Members`")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: typing.Optional[discord.Member], *, reason=None):
        """Bans a user from the guild"""
        if member == ctx.author:
            await ctx.send("uhhhh I'm not sure you want to do that Chief")
            return
        if member is None:
            await ctx.send("I have successfully banned no one")
        if member.top_role > ctx.author.top_role or member.top_role == ctx.author.top_role:
            await ctx.send(f"{member} has a higher role than you or has an equal role to you!")
            return
        if member.top_role > ctx.me.top_role or member.top_role == ctx.author.top_role:
            await ctx.send(f"{member} has a higher role than me or has an equal role to me. I cannot ban them")
            return
        await member.ban(reason=reason)
        await ctx.send(f"{member.name}#{member.discriminator} has been banned for the reason of: `{reason}`")

    @commands.command(aliases=["statuses"], brief="**Cooldown:** 10 minutes\n**Permissions Required:** `Administrator`")
    @commands.cooldown(1, 6000, commands.BucketType.guild)
    async def activities(self, ctx):
        """Gets all the statuses members have. Sends it into a hastebin link"""
        if ctx.author.guild_permissions.manage_guild or commands.is_owner():
            msg = await ctx.send("Working... this may take a few seconds")
            statuses = sorted([f"{member} ({member.id}): {str(member.activity)}" for member in ctx.guild.members if member.activity is not None], key=str)
            if len(statuses) == 0:
                return await msg.edit(content="No statuses found")
            text = "\n".join(statuses)
            data = bytes(text, 'utf-8')
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://hastebin.com/documents', data=data) as r:
                    res = await r.json()
                    key = res["key"]
                    await msg.edit(content=f"https://hastebin.com/{key}")
        else:
            return

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I do not have permission to ban specified user")
        raise error

    @commands.command(aliases=["massban", "mass-ban"], brief="**Cooldown:** None\n**Permissions Required:** `Administrator`")
    @commands.has_permissions(administrator=True)
    async def mban(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Bans multiple people from the guild. Requires Administrator permission"""
        for member in members:
            await member.ban(reason=reason)
        await ctx.send("Process Complete. Banned everyone specified")

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `Ban Members`")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        """Unbans a member from a server. Only takes user ids"""
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned specified user {user.display_name}")

    @commands.group(aliases=["clear"], brief="**Cooldown:** None\n**Permissions Required:** `Manage Messages`")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        """Purges x amount of messages."""
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Wrong Usage!", description="Purge command has seperate options. The available options it has are:\n`!purge all` purges any message from the current channel with a given amount\n`!purge bots` purges messages sent from bots", color=0xff0000)
            await ctx.send(embed=e)

    @purge.command(brief="**Cooldown:** None\n**Permissions Required:** `Manage Messages`")
    async def all(self, ctx, amount: int):
        """Purges all messages"""
        if amount < 1001:
            await ctx.message.delete()
            if len(str(amount)) > 2:
                list = [char for char in str(amount)]
                digit = int(list[0])
                while digit != 0:
                    await ctx.channel.purge(limit=100)
                    digit -= 1
            await ctx.channel.send(f"Purged {amount} messages from {ctx.channel.mention}", delete_after=3)
        else:
            await ctx.send("Amount must be 1000 messages or under")

    @purge.command(aliases=["bot"], brief="**Cooldown:** None\n**Permissions Required:** `Manage Messages`")
    async def bots(self, ctx, amount: int):
        """Purges messages from bots"""
        def is_bot(m):
            return m.author.bot
        if amount < 1001:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount, check=is_bot)
            await ctx.send(f"Purged {amount} bot messages from {ctx.channel.mention}", delete_after=3)
        else:
            await ctx.send("Amount must be 1000 messages or under")

    @purge.command(aliases=["embed"], brief="**Cooldown:** None\n**Permissions Required:** `Manage Messages`")
    async def embeds(self, ctx, amount: int):
        """Purges embed messages from bots, webhooks, or link embeds"""
        pass


def setup(bot):
    bot.add_cog(Moderation(bot))
