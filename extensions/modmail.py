import discord
from discord.ext import commands


class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
            channel = self.bot.get_channel(778645264662528061)
            embed = discord.Embed(description=f"{message.content}", color=0xff0000,
                                  timestamp=message.created_at)
            if message.attachments:

                return embed.set_image(url=str(message.attachments[0].url))
            embed.set_author(name=message.author, icon_url=message.author.avatar_url_as(format="png"))
            await channel.send(embed=embed)

    @commands.command(aliases=["message"], brief="**Cooldown:** None\n**Permissions Required:** Manage Messages")
    @commands.has_guild_permissions(manage_messages=True)
    async def reply(self, ctx, member: discord.Member, *, message):
        """Replies back to a specifc user"""
        embed = discord.Embed(description=f"{message}", color=0xff0000,
                              timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url_as(format="png"))
        await member.send(embed=embed)
        await ctx.send(f"Sent to: {member}\n{message}")


def setup(bot):
    bot.add_cog(Modmail(bot))
