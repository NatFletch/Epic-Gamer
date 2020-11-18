import discord
from discord.ext import commands
import typing
import aiohttp
from zalgo_text import zalgo as z


class Manipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `None`")
    @commands.guild_only()
    async def say(self, ctx, *, text):
        """Repeats a message back"""
        await ctx.send(f"{text}\n\u200b\n**Sent from {ctx.author.mention}**",
                       allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def zalgo(self, ctx, *, text):
        """Repeats a message in zalgo"""
        message = z.zalgo().zalgofy(f'{text}')
        await ctx.send(f"{message}\n**Sent from {ctx.author}**",
                       allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def reverse(self, ctx, *, text):
        """Says what you say in reverse"""
        sentence = None
        for char in text:
            sentence.append(char)
            newList = reversed(sentence)
            joinList = "".join(newList)
        await ctx.send(f"{joinList}\nSent from {ctx.author}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))


def setup(bot):
    bot.add_cog(Manipulation(bot))
