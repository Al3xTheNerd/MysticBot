import discord, logging
from core.env import token, DEV_MODE
import core.db as db

cogs = [
    "Error",
    "RepeatingTasks",
    "ItemSearch",
    "Misc"
]

logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
if DEV_MODE:
    debugLevel = logging.DEBUG
else:
    debugLevel = logging.WARNING
logger.setLevel(debugLevel)


bot = discord.Bot(
    intents = discord.Intents.none(),
    default_command_integration_types = {
        discord.IntegrationType.user_install,
        discord.IntegrationType.guild_install
    },
    default_command_contexts = {
        discord.InteractionContextType.guild,
        discord.InteractionContextType.bot_dm,
        discord.InteractionContextType.private_channel
    }
)
for cog in cogs:
    bot.load_extension(f"core.cogs.{cog}")
@bot.event
async def on_ready():
    if bot.user:
        if DEV_MODE:
            await bot.sync_commands(force = True)
            print(DEV_MODE)
        print(f"""Logged in as {bot.user.name} with Pycord [v{discord.__version__}]\nDeveloper Mode: {DEV_MODE}\nCommand Count: {len(bot.commands)}
              """)



bot.run(token)
