import discord
import platform
import typing
import asyncio
from discord.ext import commands


class Utility(commands.Cog):
    """Displays useful info. May require permissions"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def ping(self, ctx):
        """Shows api and bot latency"""
        e = discord.Embed(color=0xff0000)
        e.add_field(name=":robot: Bot Latency", value=f"{round(self.bot.latency * 1000)} ms", inline=False)
        await ctx.send(embed=e)

    @commands.command(aliases=["invite", "join", "info", "about"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def stats(self, ctx):
        """Shows bot stats"""
        user = self.bot.get_user(598325949808771083)
        e = discord.Embed(title=f"{ctx.bot.user.name} Stats",
                          description=f"The invite for Epic Gamer can be found [**here**](https://discord.com/oauth2/authorize?client_id=728818742917726249&scope=bot&permissions=2146958847)\n\u200B\n**Guild Count:** {len(self.bot.guilds)}\n**User Count:** {len(self.bot.users)}\n\u200B\n‎**Python Version:** {platform.python_version()}\n**Discord.py Version:** {discord.__version__}\n\u200B\nMade by {user} `(598325949808771083)`",
                          color=0xff0000)
        e.set_footer(text="Stats Command")
        await ctx.send(embed=e)

    @commands.command(aliases=['uinfo', 'ui', 'user-info'], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def userinfo(self, ctx, member: typing.Optional[discord.Member]):
        """Provides info on a certain user in the guild"""
        if member is None:
            member = ctx.author
        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        roletext = " ".join(roles)
        join_pos = sorted(ctx.guild.members, key=lambda member: member.joined_at).index(member) + 1
        e = discord.Embed(description=f"**Username:** {member}\n**User ID:** {member.id}\n**Nickname:** {member.nick}\n\u200B\n**Creation Date:** {member.created_at.strftime('%A, %B %e, %Y %I:%M %p')}\n**Join Date:** {member.joined_at.strftime('%A, %B %e, %Y %I:%M %p')}\n**Join Position:** {join_pos}\n\u200B\n**Top Role:** {member.top_role.mention}\n**Roles ({len(roles)}):** {roletext}", color=0xff0000, timestamp=ctx.message.created_at, type="rich")
        e.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar.with_format("png"))
        e.set_thumbnail(url=member.avatar.with_format("png"))
        e.set_footer(icon_url=ctx.author.avatar.with_format("png"), text=f"{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=e)

    @commands.command(aliases=["sinfo", "guildinfo", "server-info", "ginfo", 'gi', 'si'], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def serverinfo(self, ctx):
        """Provides info on this guild"""
        e = discord.Embed(
            description=f"**Server Name:** {ctx.guild.name}\n**Server ID:** `{ctx.guild.id}`\n**Creation Date:** {ctx.guild.created_at.strftime('%A, %B %e, %Y %I:%M %p')}\n\u200b\n**Owner:** {ctx.guild.owner.mention}\n**Member Count:** {ctx.guild.member_count}\n\u200b\n**Text Channels** ({len(ctx.guild.text_channels)})\n**Voice Channels** ({len(ctx.guild.voice_channels)})\n**Total Channels:** ({len(ctx.guild.channels)})\n**Roles:** ({len(ctx.guild.roles)})\n\u200b\n**Nitro Boost Tier:** {ctx.guild.premium_tier}\n**Verification Level:** {ctx.guild.verification_level}",
            color=0xff0000,
            type="rich",
            timestamp=ctx.message.created_at
            )
        
        if ctx.guild.icon is not None:
            e.set_thumbnail(url=ctx.guild.icon.with_format('png'))
        e.set_footer(icon_url=ctx.author.avatar.with_format("png"), text=f"{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=e)

    @commands.command(aliases=["pfp"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def avatar(self, ctx, member: typing.Optional[discord.Member]):
        """Displays user's avatar"""
        if member is None:
            member = ctx.author
        e = discord.Embed(title=f"{member.name}", color=0xff0000, type="image")
        e.set_image(url=member.avatar.with_format("png"))
        await ctx.send(embed=e)

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `Manage Server`")
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx):
        """Removes the bot from your server (needs Manage Server)"""
        message = await ctx.send(
            "Are you sure you want to remove me from this server type `y` to proceed")

        def check(m):
            return m.content == 'y' and m.author == ctx.author

        try:
            await self.bot.wait_for('message', check=check, timeout=20.0)
            await ctx.send("Thanks for using MEE7!")
            await ctx.guild.leave()
        except asyncio.TimeoutError:
            await message.edit(content="Timed Out")


async def setup(bot):
    await bot.add_cog(Utility(bot))
