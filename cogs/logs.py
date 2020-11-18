import discord
from io import StringIO
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        channel = discord.utils.get(message.guild.channels, name="message-logs")
        if channel is None:
            return
        e = discord.Embed(
                    description=f"**Message Deleted in {message.channel.mention}**\n**User:** {message.author.mention}\n**Content:** {message.content}",
                    color=0xff0000, timestamp=message.created_at)
        e.set_footer(text=f"{message.author.name}#{message.author.discriminator}",
                     icon_url=message.author.avatar_url_as(format='png'))
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        ctx = await self.bot.get_context(messages[0])
        f = StringIO()
        msglist = [f"{m.author} ({m.author.id}): {m.content}" for m in messages]
        content = f"\n".join(msglist)
        f.write(content)
        f.seek(0)
        channel = discord.utils.get(ctx.guild.channels, name="message-logs")
        if channel is None:
            return print("channel not found")
        await channel.send(f"{len(messages)} messages purged from {ctx.channel.mention}", file=discord.File(filename=f"bulk-delete-log.txt", fp=f))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        channel = discord.utils.get(before.guild.channels, name="message-logs")
        if channel is None:
            return
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

        if logchannel is None:
            return
        e = discord.Embed(
            description=f"**New Channel Created:** {channel.mention}",
            color=0x61ff61, timestamp=channel.created_at)
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        logchannel = discord.utils.get(channel.guild.channels, name="server-logs")
        if logchannel is None:
            return
        e = discord.Embed(
            description=f"**Channel Deleted:** `{channel.name}`",
            color=0xff0000, timestamp=channel.created_at)
        await logchannel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        logchannel = discord.utils.get(before.guild.channels, name="server-logs")
        if logchannel is None:
            return
        if before.name != after.name:
            e = discord.Embed(
                description=f"**Channel Name Edited:** {before.mention}\n**Before:** {before.name}\n**After:** {after.name}",
                color=0xffc800)
            await logchannel.send(embed=e)
        if before.topic != after.topic:
            e = discord.Embed(
                description=f"**Channel Topic Edited:** {before.mention}\n**Before:** {before.topic}\n**After:** {after.topic}",
                color=0xffc800)
            await logchannel.send(embed=e)
        if before.position:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="user-logs")
        if channel is None:
            return
        e = discord.Embed(
            description=f"{member.mention} has joined\n\u200b\n**Creation Date:** {member.created_at.strftime('%A, %B %e, %Y %I:%M %p')}",
            color=0x61ff61)
        e.set_footer(text=f"There is now {member.guild.member_count} members")
        e.set_thumbnail(url=member.avatar_url_as(format='png'))
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name="user-logs")
        if channel is None:
            return
        e = discord.Embed(
                    description=f"{member.name}#{member.discriminator} has left",
                    color=0xff0000)
        e.set_thumbnail(url=member.avatar_url_as(format='png'))
        e.set_footer(text=f"There is now {member.guild.member_count} members")
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            channel = discord.utils.get(before.guild.channels, name="user-logs")
            if channel is None:
                return
            e = discord.Embed(title="Nickname Change", description=f"**Member:** {before.name}#{before.discriminator}\n**Before:** {before.nick}\n**After:** {after.nick}", color=0xffc800)
            await channel.send(embed=e)
        if before.roles != after.roles:
            rbefore = [role for role in before.roles if role != before.guild.default_role]
            rafter = [role for role in after.roles if role != before.guild.default_role]
            channel = discord.utils.get(before.guild.channels, name="user-logs")
            if channel is None:
                return
            e = discord.Embed(title="Role Change", description=f"**Member:** {before.mention}", color=0xffc800)
            e.add_field(name=f"Before ({len(rbefore)})", value=" ".join([role.mention for role in rbefore]), inline=False)
            e.add_field(name=f"After ({len(rafter)})", value=" ".join([role.mention for role in rafter]))
            e.set_thumbnail(url=before.avatar_url_as(format='png'))
            await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = discord.utils.get(user.guild.channels, name="mod-logs")
        if channel is None:
            return
        e = discord.Embed(title="Member Banned!", description=f"**Name:** {user.name}#{user.discriminator}\n**ID:** `({user.id})`", color=0xff0000)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = discord.utils.get(guild.channels, name="mod-logs")
        if channel is None:
            return
        e = discord.Embed(title="Member Unbanned!", description=f"**Name:** {user.name}#{user.discriminator}\n**ID:** `({user.id})`", color=0xff0000)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return
        if before.channel is None:
            channel = discord.utils.get(member.guild.channels, name="server-logs")
            if channel is None:
                return
            e = discord.Embed(title="Member Joined Voice Channel", description=f"Member: {member.mention}\nVoice Channel: {after.channel}", color=0xff0000)
            await channel.send(embed=e)
        elif before.channel is not None:
            channel = discord.utils.get(member.guild.channels, name="server-logs")
            if channel is None:
                return
            e = discord.Embed(title="Member Left Voice Channel", description=f"Member: {member.mention}\nVoice Channel: {before.channel}", color=0xff0000)
            await channel.send(embed=e)


def setup(bot):
    bot.add_cog(Logging(bot))