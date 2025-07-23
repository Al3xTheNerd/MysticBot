import discord


from atn import token, cogs
import db as db


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
