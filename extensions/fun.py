import discord
import random
import aiohttp
import typing
from discord.ext import commands


class Fun(commands.Cog):
    """Fun commands that everyone can use"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="8ball", brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def advice(self, ctx, *, question):
        """Answers questions in a typical magic 8ball format"""
        e = discord.Embed(color=0xff0000)
        e.add_field(name="Question:", value=question, inline=False)
        e.add_field(name="Answer:", value=random.choice(
            ["As I see it, yes", "Ask again later", "Better not tell you now", "Cannot predict now",
             "Concentrate and ask again", "Don’t count on it", "It is certain", "It is decidedly so", "Most likely",
             "My reply is no", "My sources say no", "Outlook not so good", "Outlook good", "Reply hazy, try again",
             "Signs point to yes", "Very doubtful", "Without a doubt", "Yes", "Yes – definitely",
             "You may rely on it"]), inline=False)
        await ctx.send(embed=e)

    @commands.command(aliases=["dice"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def roll(self, ctx, *, sides: int = None):
        """Rolls a dice"""
        if sides:
            if sides > 1000000000:
                await ctx.send("Please choose a smaller number")
            else:
                outcome = random.randint(1, sides)
                await ctx.send(outcome)
        else:
            outcome = random.randint(1, 6)
            await ctx.send(outcome)

    @commands.command(brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def choose(self, ctx, option1, option2):
        """Chooses between two things"""
        e = discord.Embed(color=0xff0000)
        e.add_field(name="Options:", value=f'{option1} or {option2}', inline=False)
        e.add_field(name="Outcome", value=random.choice([option1, option2]))
        await ctx.send(embed=e)

    @commands.command(aliases=["flip", "coinflip"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def coin(self, ctx):
        """Flips a coin"""
        await ctx.send(random.choice(["Heads!", "Tails!"]))

    @commands.command(aliases=["memes"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    @commands.guild_only()
    async def meme(self, ctx):
        """Chooses a meme from various subreddits"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/meme") as cs:
                js = await cs.json()
                embed = discord.Embed(title=js['caption'], color=0xff0000)
                embed.set_image(url=js["image"])
                embed.set_footer(text=f"Category: {js['category']}")
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
