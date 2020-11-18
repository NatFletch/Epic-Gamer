import discord
import time
import platform
import typing
from discord.ext import commands


class Info(commands.Cog):
    """Displays useful info. May require permissions"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """Shows api and bot latency"""
        e = discord.Embed(color=0xff0000)
        Starts = time.perf_counter()
        Message = await ctx.send("Pinging...")
        Ending = time.perf_counter()
        Duration = (Ending - Starts) * 1000
        await Message.delete()
        e = discord.Embed(color=0xff0000)
        e.add_field(name=":robot: Bot Latency", value=f"{round(self.bot.latency * 1000)} ms", inline=False)
        e.add_field(name=":desktop: API Latency", value=f"{round(Duration)} ms", inline=False)
        await ctx.send(embed=e)

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You're being rate limited. You need to wait {round(error.retry_after)} seconds to use this command again")

    @commands.command(aliases=["invite", "join"])
    async def stats(self, ctx):
        """Shows bot stats"""
        e = discord.Embed(title="MEE7 Stats",
                          description=f"[**Invite**](https://discord.com/oauth2/authorize?client_id=728818742917726249&scope=bot&permissions=2146958847)\n\u200B\n**Guild Count:** {len(self.bot.guilds)}\n**User Count:** {len(self.bot.users)}\n\u200B\n‎**Python Version:** {platform.python_version()}\n**Discord.py Version:** {discord.__version__}",
                          color=0xff0000)
        e.set_footer(text="Stats Command")
        await ctx.send(embed=e)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Provides info on a certain user in the guild"""
        if member:
            roles = [role for role in member.roles if role != ctx.guild.default_role]
            e = discord.Embed(
                description=f"**Username:** {member.name}#{member.discriminator}\n**User ID:** {member.id}\n**Nickname:** {member.nick}\n\u200B\n**Creation Date:** {member.created_at.strftime('%A, %B %e, %Y %I:%M %p')}\n**Join Date:** {member.joined_at.strftime('%A, %B %e, %Y %I:%M %p')}\n\u200B\n**Status:** {member.status}\n\u200B\n**Top Role:** {member.top_role.mention}",
                color=0xff0000,
                timestamp=ctx.message.created_at,
                type="rich")
            e.add_field(name=f"**Roles** ({len(roles)})", value=" ".join([role.mention for role in roles]))
            e.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url_as(format='png'))
            e.set_thumbnail(url=member.avatar_url_as(format='png'))
            e.set_footer(icon_url=ctx.author.avatar_url_as(format='png'),
                         text=f"{ctx.author.name}#{ctx.author.discriminator}")
            await ctx.send(embed=e)
        else:
            author = ctx.author
            roles = [role for role in author.roles if role != ctx.guild.default_role]
            e = discord.Embed(
                description=f"**Username:** {author.name}#{author.discriminator}\n**User ID:** {author.id}\n**Nickname:** {author.nick}\n\u200B\n**Creation Date:** {author.created_at.strftime('%A, %B %e, %Y %I:%M %p')}\n**Join Date:** {author.joined_at.strftime('%A, %B %e, %Y %I:%M %p')}\n\u200B\n**Status:** {author.status}\n\u200B\n**Top Role:** {author.top_role.mention}",
                color=0xff0000,
                timestamp=ctx.message.created_at,
                type="rich")
            e.set_author(name=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url_as(format='png'))
            e.set_thumbnail(url=ctx.author.avatar_url_as(format='png'))
            e.set_footer(icon_url=ctx.author.avatar_url_as(format='png'), text=f"{ctx.author.name}#{ctx.author.discriminator}")
            e.add_field(name=f"**Roles** ({len(roles)})", value=" ".join([role.mention for role in roles]))
            await ctx.send(embed=e)

    @commands.command(aliases=["sinfo", "guildinfo", "server-info", "ginfo"])
    async def serverinfo(self, ctx):
        """"Provides info on this guild"""
        e = discord.Embed(
            description=f"**Server Name:** {ctx.guild.name}\n**Server ID:** `{ctx.guild.id}`\n**Region:** `{ctx.guild.region}`\n\u200b\n**Owner:** {ctx.guild.owner.mention}\n**Member Count:** {ctx.guild.member_count}\n\u200b\n**Text Channels** ({len(ctx.guild.text_channels)})\n**Voice Channels** ({len(ctx.guild.voice_channels)})\n**Total Channels:** {len(ctx.guild.channels)}\n**Roles:** ({len(ctx.guild.roles)})\n\u200b\n**Nitro Boost Tier:** {ctx.guild.premium_tier}\n**Verification Level:** {ctx.guild.verification_level}",
            color=0xff0000,
            type="rich",
            timestamp=ctx.message.created_at
            )
        e.set_thumbnail(url=ctx.guild.icon_url_as(format='png'))
        e.set_footer(icon_url=ctx.author.avatar_url_as(format='png'), text=f"{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=e)

    @commands.command(aliases=["pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        """Displays user's avatar"""
        if member:
            e = discord.Embed(title=f"{member.name}#{member.discriminator}", color=0xff0000, type="image")
            e.set_image(url=member.avatar_url_as(format='png'))
            await ctx.send(embed=e)
        else:
            e = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}", color=0xff0000, type="image")
            e.set_image(url=ctx.author.avatar_url_as(format='png'))
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Info(bot))
