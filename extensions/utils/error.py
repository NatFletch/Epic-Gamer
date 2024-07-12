import discord
import traceback
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You are missing permissions. You require `{error.missing_perms}` to use this")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f"Your arguments are not correct. Please view help on this command using `;help {ctx.invoked_with}` to see how to use it")
            print(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You missed a required argument. Make sure to add `{error.param}` when using this command")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Only developers can use this command :)")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"I am missing permissions to perform this operation. I am missing {error.missing_perms} permissions")
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(
                f"Woah, I'm not getting banned anytime soon! You need to be in an NSFW channel to execute this command!")
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send("I already loaded that cog. No need to load it again")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send(f"Hmmm I can't seem to find {error.name}")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You are using this command too fast! You have {round(error.retry_after)} seconds until you can use this command again")
        else:
            text = "".join(traceback.format_exception_only(type(error), error))
            embed = discord.Embed(title="An Unknown Error Occurred!",
                                  description=f'```py\nIgnoring exception in command {ctx.command}:\n{text}\n```',
                                  color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Error(bot))