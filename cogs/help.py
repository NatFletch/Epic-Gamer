import discord
from discord.ext import commands


class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'hidden': True})

    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

    def command_formatter(self, embed, command):
        embed.title = self.get_command_signature(command)
        if command.description:
            embed.description = f'{command.description}\n\n{command.help}'
        else:
            embed.description = command.help or 'No help found...'

    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(description="To get help on a command type `!help command`", color=0xff0000)
        bot = self.context.bot
        filtered = await self.filter_commands(bot.commands, sort=True)
        for cog, cog_commands in mapping.items():
            filtered = await self.filter_commands(cog_commands)
            if filtered:
                embed.add_field(name=f"{cog.qualified_name} Commands", value=cog.description or 'No description',
                                inline=False)
                for command in filtered:
                    embed.add_field(name=f"`{self.get_command_signature(command)}`",
                                    value=f"{command.description}\n\n{command.help}", inline=False)
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command),
                              description=command.short_doc or 'No description', color=0xff0000)
        embed.set_footer(text=f'Category: {command.cog_name}')
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(color=0xff0000)
        self.command_formatter(embed, group)

        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f'Category: {cog.qualified_name}', description=cog.description or 'No description',
                              color=0xff0000)
        filtered = await self.filter_commands(cog.get_commands())
        if filtered:
            for command in filtered:
                self.add_command_field(embed, command)
        await self.context.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self


def cog_unload(self):
    self.bot.help_command = self.old_help_command


def setup(bot):
    bot.add_cog(Help(bot))
