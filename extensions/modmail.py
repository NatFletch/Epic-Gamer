import discord
from discord.ext import commands


class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
            channel = self.bot.get_channel(1208195461152776203)
            embed = discord.Embed(description=f"{message.content}", color=0xff0000,
                                  timestamp=message.created_at)
            if message.attachments:

                return embed.set_image(url=str(message.attachments[0].url))
            embed.set_author(name=message.author, icon_url=message.author.avatar.with_format("png"))
            await channel.send(embed=embed)

    @commands.command(aliases=["message"], brief="**Cooldown:** None\n**Permissions Required:** Manage Messages")
    @commands.has_guild_permissions(manage_messages=True)
    async def reply(self, ctx, member: discord.Member, *, message):
        """Replies back to a specifc user"""
        embed = discord.Embed(description=f"{message}", color=0xff0000,
                              timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.with_format("png"))
        await member.send(embed=embed)
        await ctx.send(f"Sent to: {member}\n{message}")


async def setup(bot):
    await bot.add_cog(Modmail(bot))
