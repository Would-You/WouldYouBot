"""
Copyright (C) 2019 Diniboy
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from traceback import print_exc

import discord
from aiohttp import ClientSession
from discord.ext import commands

import config
import motor.motor_asyncio

bot = commands.AutoShardedBot(
    command_prefix=commands.when_mentioned_or(*config.prefix),
    owner_id=config.owner_id,
    activity=discord.Game(name=f"{config.prefix[0]} help"),
)
bot.config = config


@bot.event
async def on_ready():
    print(
        f"I am logged in as {bot.user} | {len(bot.guilds)} guilds | {len(bot.users)} users"
    )


@bot.command(hidden=True)
@commands.is_owner()
async def kill(ctx):
    await ctx.send("Bye Felicia...")
    await bot.logout()


async def create_session():
    bot.session = ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
        }
    )
    client = motor.motor_asyncio.AsyncIOMotorClient()
    bot.db = client.wouldyou


if __name__ == "__main__":
    bot.loop.create_task(create_session())
    for module in config.modules:
        try:
            bot.load_extension(module)
        except Exception:
            print_exc()
    bot.run(config.token)
