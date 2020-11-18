import discord
import random
import aiohttp
from discord.ext import commands


class Fun(commands.Cog):
    """Fun commands that everyone can use"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="8ball")
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

    @commands.command()
    async def choose(self, ctx, option1, option2):
        """Chooses between two things"""
        e = discord.Embed(color=0xff0000)
        e.add_field(name="Options:", value=f'{option1} or {option2}', inline=False)
        e.add_field(name="Outcome", value=random.choice([option1, option2]))
        await ctx.send(embed=e)

    @commands.command(aliases=["flip", "coinflip"])
    async def coin(self, ctx):
        """Flips a coin"""
        await ctx.send(random.choice(["Heads!", "Tails!"]))

    @commands.command(aliases=["memes"])
    @commands.guild_only()
    async def meme(self, ctx):
        """Chooses a meme from r/memes"""
        async with aiohttp.ClientSession() as session:
            sub = random.choice(["memes", "dankmemes", "funny"])
            async with session.get(f'https://www.reddit.com/r/{sub}/new.json?sort=hot') as r:
                res = await r.json()
                embed = discord.Embed(title=f"r/{sub}", color=0xff0000)
                embed.set_image(url=res['data']['children'][random.randint(0, 20)]['data']['url'])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
