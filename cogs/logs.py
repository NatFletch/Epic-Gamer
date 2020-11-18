import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        channel = discord.utils.get(message.guild.channels, name="message-logs")
        e = discord.Embed(description=f"**Message Deleted in {message.channel.mention}**\n**User:** {message.author.mention}\n**Content:** {message.content}", color=0xff0000, timestamp=message.created_at)
        e.set_footer(text=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url_as(format='png'))
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = discord.utils.get(before.guild.channels, name="message-logs")
        if before.author == self.bot.user:
            return
        if before.content == after.content:
            return
        e = discord.Embed(description=f"**Message Edited in {before.channel.mention}**\n**User:** {before.author.mention}\n**Before:** {before.content}\n**After:** {after.content}\n[Jump to Message]({after.jump_url})", color=0xff0000, timestamp=after.created_at)
        e.set_footer(text=f"{before.author.name}#{before.author.discriminator}", icon_url=before.author.avatar_url_as(format='png'))
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logchannel = discord.utils.get(channel.guild.channels, name="server-logs")
        e = discord.Embed(
            description=f"**New Channel Created:** {channel.mention}",
            color=0x61ff61, timestamp=channel.created_at)
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        logchannel = discord.utils.get(channel.guild.channels, name="server-logs")
        e = discord.Embed(
            description=f"**Channel Deleted:** `{channel.name}`",
            color=0xff0000, timestamp=channel.created_at)
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        logchannel = discord.utils.get(before.guild.channels, name="server-logs")
        if before == after:
            return
        e = discord.Embed(
            description=f"**Channel Edited:** {before.mention}\n**Before:** {before}\n**After:** {after}",
            color=0xffc800, timestamp=after.created_at)
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="user-logs")
        e = discord.Embed(
            description=f"{member.mention} has joined\n\u200b\n**Creation Date:** {member.created_at.strftime('%A, %B %e, %Y %I:%M %p')}",
            color=0x61ff61)
        e.set_footer(text=f"There is now {member.guild.member_count} members")
        e.set_thumbnail(url=member.avatar_url_as(format='png'))
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name="user-logs")
        e = discord.Embed(
            description=f"{member.name}#{member.discriminator} has left",
            color=0xff0000)
        e.set_thumbnail(url=member.avatar_url_as(format='png'))
        e.set_footer(text=f"There is now {member.guild.member_count} members")
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        logchannel = discord.utils.get(before.guild.channels, name="server-logs")
        if before == after:
            return
        e = discord.Embed(
            description=f"**Member Edited:** {before.mention}\n**Before:** {before}\n**After:** {after}",
            color=0xffc800, timestamp=after.created_at)
        e.set_thumbnail(url=before.avatar_url_as(format='png'))
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_ban(self, member, guild):
        ...



def setup(bot):
    bot.add_cog(Logging(bot))