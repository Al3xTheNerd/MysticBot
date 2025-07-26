import discord


from atn import token
import db as db

cogs = [
    "cogs.Error",
    "cogs.RepeatingTasks",
    "cogs.ItemSearch",
    "cogs.Misc"
]

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
    bot.load_extension(cog)
@bot.event
async def on_ready():
    if bot.user:
        print(f"Logged in as {bot.user.name} with Pycord [v{discord.__version__}]")


bot.run(token)
