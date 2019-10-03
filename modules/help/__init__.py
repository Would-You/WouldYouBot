import discord
from discord.ext import commands


async def _can_run(cmd, ctx):
    try:
        return await cmd.can_run(ctx)
    except:
        return False


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, command_name: str = None):
        """A little bit help is always helpful!"""
        if command_name:
            command = self.bot.get_command(command_name)
            if not command:
                return await ctx.send("No such command!")
            return await ctx.send(
                f"```\n{ctx.prefix}{command.name} {command.signature}\n\n{command.help or 'Missing description'}```"
            )
        description = []
        for name, cog in self.bot.cogs.items():
            entries = [
                " - ".join([cmd.name, cmd.short_doc or "Missing description"])
                for cmd in cog.get_commands()
                if await _can_run(cmd, ctx) and not cmd.hidden
            ]
            if entries:
                description.append(f"**{name}**:")
                description.append("• " + "\n• ".join(entries))
        await ctx.send(
            embed=discord.Embed(
                description="\n".join(description), color=ctx.me.color
            ).set_thumbnail(
                url="https://cdn.discordapp.com/attachments/546021486901723148/627928707948085289/leaves.png"
            )
        )

    @commands.command()
    async def ping(self, ctx):
        """Displays the Discord websocket latency"""
        await ctx.send(f"Pong! It took {round(self.bot.latency * 1000, 2)} ms.")

    @commands.command(aliases=["inv"])
    async def invite(self, ctx):
        """Invite me to your server kthx love"""
        await ctx.send(
            f"<https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=0>"
        )


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))
