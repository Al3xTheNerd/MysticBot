import discord
from discord.ext import commands


from core.cogs.ErrorDefinitions import *
from core.db import getItemListTabComplete, getItemList, getCrateList, getTagList, addOneToItemCounter, getItemCounter
from core.utils import symbolsToRemove




class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    @commands.slash_command(
        name = "popularity",
        description = "Shows a list of some of the most popular searched items!")
    async def topItems(self,
                       ctx: discord.ApplicationContext):   
        currentItemCounter = await getItemCounter()
        returnText = "```ansi\n"
        if currentItemCounter:
            mostPopular = list(dict(sorted(currentItemCounter.items(), key=lambda item: item[1])).keys())
            mostPopular.reverse()
            for counter, itemName in enumerate(mostPopular, 1):
                prettyName = itemName
                for symbol in symbolsToRemove:
                    prettyName = prettyName.replace(f"{symbol} ", "").replace(f" {symbol}", "")
                potentialAddition = f"\u001b[0;32m{counter:>2}\u001b[0;0m - \u001b[0;35m{prettyName:<29}\u001b[0;0m (\u001b[0;36m{currentItemCounter[itemName]}\u001b[0;0m)\n"
                if len(returnText + potentialAddition) <= 4096:
                    returnText += potentialAddition
                else: break
            returnText += "```"
        else:
            returnText += "No items searched yet!```"
        
        embed = discord.Embed(color=0x3c7186)
        embed.title = "Most popular searches!"
        embed.description = returnText
        await ctx.respond(embed = embed)
        
    @commands.slash_command(
        name = "stats",
        description = "Stats and general info about the bot!")
    async def itemSearchCommand(self,
                          ctx: discord.ApplicationContext):
        appInfo = await self.bot.application_info()
        embed = discord.Embed(colour=0x3c7186)

        embed.add_field(name="Bot Manager",
                        value=f"{appInfo.owner.mention}",
                        inline=False)
        embed.add_field(name="Latency",
                        value=f"{round(self.bot.latency*1000, 2)}ms",
                        inline=False)
        embed.add_field(name="Guild Count",
                        value=f"{appInfo.approximate_guild_count}",
                        inline=True)
        embed.add_field(name="User Count",
                        value=f"{appInfo.approximate_user_install_count}",
                        inline=True)
        searchCounter = 0
        currentItemCounter = await getItemCounter()
        if currentItemCounter:
            for itemName in currentItemCounter.keys():
                searchCounter += currentItemCounter[itemName]
            
            embed.add_field(name="Search Count",
                            value=f"{searchCounter}",
                            inline=True)
        
        
        await ctx.respond(embed = embed)

    
    
    
def setup(bot: discord.Bot):
    bot.add_cog(Misc(bot))