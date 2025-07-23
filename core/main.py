import discord
from discord.ext import commands
from typing import List


from atn import token, guild_ids, cogs
import db as db
from models.Item import Item
from models.Crate import Crate


bot = discord.Bot(
    intents = discord.Intents.none()
)
for cog in cogs:
    bot.load_extension(cog)
@bot.event
async def on_ready():
    if bot.user:
        print(f"Logged in as {bot.user.name}")




bot.run(token)
