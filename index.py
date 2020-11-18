import discord
from secret import token
from discord.ext import commands

extensions = ["cogs.fun", "cogs.help", "cogs.info", "cogs.config", "cogs.logs"]


class MEE7(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"), case_insensitive=True, help_command=None)
        self.load_extension("jishaku")
        jsk = self.get_command("jishaku")
        jsk.hidden = True
        for extension in extensions:
            self.load_extension(extension)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(f"An unknown error has appeared\n`{error}`")

    async def on_ready(self):
        print(f"MEE7 is up and running at {round(self.latency * 1000)}ms")
        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))


if __name__ == "__main__":
    MEE7().run("token")
