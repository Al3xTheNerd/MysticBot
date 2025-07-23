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






@bot.slash_command(
    guild_ids = guild_ids,
    name = "hello",
    description = "Says hello to you!"
)
@commands.cooldown(
    1, 15, commands.BucketType.user
)
async def hello(
        ctx: discord.ApplicationContext
    ):
    items: List[Item] | None = await db.getItemList()
    crates: List[Crate] | None = await db.getCrateList()
    if items and crates:
        item = items[1]
        crate = [x for x in crates if x.id == item.CrateID][0]
        
        await ctx.respond(f"`{item.ItemName}` comes from the `{crate.CrateName}` Crate")
    else:
        await ctx.respond("None")


bot.run(token)
