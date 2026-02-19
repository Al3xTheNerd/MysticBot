import discord, aiohttp, random
from discord.ext import commands, tasks
from typing import List


import core.db as db
from core.env import webAddress
from core.models.Item import Item, dictToItem
from core.models.Crate import Crate, dictToCrate
from core.utils import symbolsToRemove, updateFromSite



class RepeatingTasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.pullData.start()

    @tasks.loop(minutes=1)
    async def updateStatus(self):
        rand = random.randint(1, 4)
        status = ""
        match rand:
            case 1:
                cratesList = await db.getCrateList()
                if cratesList:
                    crateToUse = random.choice(cratesList)
                    options = [
                        f"{crateToUse.CrateName} came out {crateToUse.ReleaseDate}!"
                    ]
                    status = random.choice(options)
            case 2:
                tagsList = await db.getTagList()
                if tagsList:
                    tagToUse = random.choice(tagsList)
                    options = [
                        f"Thinking about {tagToUse}s."
                    ]
                    status = random.choice(options)
            case 3:
                itemsList = await db.getItemList()
                if itemsList:
                    itemToUse = random.choice(itemsList)
                    for symbol in symbolsToRemove:
                        itemToUse.ItemName = itemToUse.ItemName.replace(f"{symbol} ", "").replace(f" {symbol}", "")
                    options = [
                        f"{itemToUse.ItemName} is pretty cool.",
                        f"{itemToUse.ItemName} - {itemToUse.WinPercentage}%"
                    ]
                    status = random.choice(options)
            case 4:
                options = [
                    "Am I alive?",
                    "Playin' with fire.",
                    "Not a nerd!",
                    "Made by Alex!",
                    "Yo!"
                ]
                status = random.choice(options)
        await self.bot.change_presence(activity = discord.Activity(name = "custom", state = f"{status}", type=discord.ActivityType.custom),
                                       status = discord.Status.online)
        
    
    @tasks.loop(minutes=60)
    async def pullData(self):
        if self.updateStatus.is_running():
            self.updateStatus.stop()
        await updateFromSite()

        await self.updateStatus.start()
def setup(bot: discord.Bot):
    bot.add_cog(RepeatingTasksCog(bot))