import discord
import random
from discord.ext import commands


class Economy(commands.Cog):
    """Fun economy game that everyone can play"""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["start"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def register(self, ctx):
        """Registers an account to play"""
        ctx.command.usage = f"{ctx.prefix}{ctx.command.name}"
        user = await self.bot.db.fetch("SELECT * FROM money WHERE user_id = $1", ctx.author.id)
        if not user:
            await self.bot.db.execute("INSERT INTO money (amount, user_id) VALUES ($1, $2)", 100, ctx.author.id)
            await ctx.send(f"Account registered. Use the balance command to check your balance. Current Balance: 100")
        else:
            await ctx.send("You already have an account")

    @commands.command(aliases=["bal"], brief="**Cooldown:** None\n**Permissions Required:** `None`")
    async def balance(self, ctx):
        """Checks your balance"""
        if not await ctx.open_wallet():
            await ctx.send("You need to register an account first. Use the register command to start")
        else:
            await ctx.send(f"You currently have `{await ctx.open_wallet()}` dollars")

    @commands.command(brief="**Cooldown:** 45 seconds\n**Permissions Required:** `None`")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def search(self, ctx):
        """Searches a random location for spare change"""
        amount = await ctx.open_wallet()
        if amount:
            statusmsg = random.choice(("FIND!", "LOSS!"))
            locations = random.choice(("laundromat", "vending machine", "grocery store", "bathroom", "bush", "park", "trash can", "dumpster"))
            if statusmsg == "FIND!":
                outcome = random.randint(1, 300)
                await self.bot.db.execute("UPDATE money SET amount = $1 WHERE user_id = $2", outcome + amount, ctx.author.id)
                await ctx.send(f'{statusmsg} You found {outcome} dollars in a {locations}')
            elif statusmsg == "LOSS!":
                outcome = random.randint(0, 200)
                msg = f"{statusmsg} You dropped {outcome} dollars in a {locations} and now you can\'t find it"
                newoutcome = amount - outcome
                if amount < outcome:
                    newoutcome = outcome + amount
                    msg = f'FIND! You found {outcome} dollars in a {locations}'
                await self.bot.db.execute("UPDATE money SET amount = $1 WHERE user_id = $2", newoutcome, ctx.author.id)
                await ctx.send(msg)
        else:
            await ctx.send(f"You need to register an account first. Please type `{ctx.prefix}register` to get started")

    @commands.command(aliases=["bet"], brief="**Cooldown:** 5 seconds\n**Permissions Required:** `None`")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gamble(self, ctx, amount: int):
        """Gambles specific amount of money"""
        user = await ctx.open_wallet()
        if user:
            if amount <= 0:
                return await ctx.send("Please place a higher bet than 0")
            if amount > user:
                return await ctx.send("You placed a bet higher than your amount of money")
            EpicGamerOutcome = random.randint(1, 10)
            UserOutcome = random.randint(1, 10)
            status = None
            color = None
            if EpicGamerOutcome > UserOutcome:
                new = user - amount
                status = 'Lose'
                color = 0xff0000
            elif UserOutcome > EpicGamerOutcome:
                new = user + amount
                status = 'Win'
                color = 0x00ff00
            elif UserOutcome == EpicGamerOutcome:
                color = 0xffff00
                status = 'Tie. Lost nothing'
            await ctx.set_money(new)
            embed = discord.Embed(title=status, description=f"You now have {new} dollars", color=color)
            embed.add_field(name="Epic Gamer", value=f"Rolled a {EpicGamerOutcome}")
            embed.add_field(name=ctx.author.name, value=f"Rolled a {UserOutcome}")
            await ctx.send(embed=embed)
        else:
            return await ctx.send(f"You need to register an account first. Use {ctx.prefix}register to register.")


def setup(bot):
    bot.add_cog(Economy(bot))
