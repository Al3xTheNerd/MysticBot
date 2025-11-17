import discord
from discord.ext import commands
from discord.commands import option, SlashCommandGroup

from core.db import getItemListTabComplete, getItemList, getCrateList, getTagList, addOneToItemCounter, getItemCounter
from core.models.Item import itemToEmbed
from core.cogs.ErrorDefinitions import *
from core.utils import buildPaginator, makeFile

async def itemNameTabComplete(ctx: discord.AutocompleteContext):
    itemsList = await getItemListTabComplete()
    itemCounts = await getItemCounter()
    returnInfo = []
    if itemsList:
        if itemCounts:
            if ctx.value == "":
                mostPopular = list(dict(sorted(itemCounts.items(), key=lambda item: item[1])).keys())
                mostPopular.reverse()
                returnInfo += [x for x in mostPopular]
                returnInfo += [x for x in itemsList if x not in returnInfo]
                return returnInfo
        return [item for item in itemsList if ctx.value.lower() in item.lower()]
    
    return None

async def tagNameTabComplete(ctx: discord.AutocompleteContext):
    tagsList = await getTagList()
    if tagsList:
        return [tag for tag in tagsList if ctx.value.lower() in tag.lower()]
    return None

async def crateNameTabComplete(ctx: discord.AutocompleteContext):
    cratelist = await getCrateList()
    if cratelist:
        return [crate.CrateName for crate in cratelist if ctx.value.lower() in crate.CrateName.lower()]
    return None


class ItemSearch(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
    
    search = SlashCommandGroup("search",
                               description = "Commands relating to searching.")
    
    
    @search.command(
        name = "item",
        description = "Search for an item by name.")
    @option("item", description="Pick an item!", autocomplete = itemNameTabComplete)
    async def itemSearchCommand(self,
                          ctx: discord.ApplicationContext,
                          item: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        itemNameList = [x.ItemName for x in itemsList]
        if item not in itemNameList:
            raise ItemNotInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        itemObject = [x for x in itemsList if x.ItemName == item][0]
        timesRequested = await addOneToItemCounter(item)
        embed = await itemToEmbed(itemObject, crateList, timesRequested)
        await ctx.respond(embed = embed, file=makeFile(itemObject))
        
    
    @search.command(
        name = "tag",
        description = "Search for items with a designated tag.")
    @option("tag", description = "Pick a tag!", autocomplete = tagNameTabComplete)
    async def tagSearchCommand(self,
                               ctx: discord.ApplicationContext,
                               tag: str):
        tagsList = await getTagList()
        if not tagsList:
            raise NoTagsInDatabaseError
        if tag not in tagsList:
            raise TagNotInDatabaseError
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        itemsWithTag = [(await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName)), makeFile(item)) for item in itemsList if tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary] and "Repeat Appearance" not in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary]]

        paginator = buildPaginator(itemsWithTag)
        await paginator.respond(ctx.interaction, ephemeral = False)
        
    @search.command(
        name = "term",
        description = "Search for a word or phrase through the item's lore."
    )
    @option("term", description = "Enter a phrase!", input_type = str)
    async def termSearchCommand(self,
                                ctx: discord.ApplicationContext,
                                term: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        itemsFound = [(await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName)), makeFile(item)) for item in itemsList if term.lower() in item.ItemHuman.lower() and "Repeat Appearance" not in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary]]
        if not itemsFound:
            raise NoResultsFoundError
        
        paginator = buildPaginator(itemsFound)
        await paginator.respond(ctx.interaction, ephemeral = False)
        
    @search.command(
        name = "crate",
        description = "Search by Crate."
    )
    @option("crate", description = "Pick a crate!", autocomplete = crateNameTabComplete)
    async def crateSearchCommand(self,
                                 ctx: discord.ApplicationContext,
                                 crate: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        if crate not in [potCrate.CrateName for potCrate in crateList]:
            raise CrateNotInDatabaseError
        crateID = [potCrate.id for potCrate in crateList if potCrate.CrateName == crate][0]
        itemsFound = [(await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName)), makeFile(item)) for item in itemsList if item.CrateID == crateID]
        if not itemsFound:
            raise NoResultsFoundError
        paginator = buildPaginator(itemsFound)
        await paginator.respond(ctx.interaction, ephemeral = False)
    
    @search.command(
        name = "advanced",
        description = "Search by multiple constraints."
    )
    @option("crate", description = "Pick a crate!", autocomplete = crateNameTabComplete, required=False, default="")
    @option("term", description = "Enter a phrase!", required=False, default="", input_type=str)
    @option("tag", description = "Pick a tag!", autocomplete = tagNameTabComplete, required=False, default="", input_type=str)
    async def advancedSearchCommand(self,
                                 ctx: discord.ApplicationContext,
                                 crate: str,
                                 term: str,
                                 tag: str):
        itemsList = await getItemList()
        if not itemsList:
            raise NoItemsInDatabaseError
        crateList = await getCrateList()
        if not crateList:
            raise NoCratesInDatabaseError
        if crate == "" and term == "" and tag == "":
            raise MinimumConstraintError
        
        if crate != "":
            if crate not in [potCrate.CrateName for potCrate in crateList]:
                raise CrateNotInDatabaseError
            crateID = [potCrate.id for potCrate in crateList if potCrate.CrateName == crate][0]

        if tag != "":
            tagsList = await getTagList()
            if not tagsList:
                raise NoTagsInDatabaseError
            if tag not in tagsList:
                raise TagNotInDatabaseError

        
        sortedItems = []
        for item in itemsList:
            meetsAllConditions = False
            itemTags = [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary]
            if "Repeat Appearance" in itemTags:
                continue
            if crate != "":
                if item.CrateID != crateID: # type: ignore
                    continue
            if tag != "":
                if tag not in itemTags:
                    continue
            if term != "":
                if term.lower() not in item.ItemHuman.lower():
                    continue
            embedPage = await itemToEmbed(item, crateList, await addOneToItemCounter(item.ItemName)), makeFile(item)
            sortedItems.append(embedPage)
        
        
        if not sortedItems:
            raise NoResultsFoundError
        paginator = buildPaginator(sortedItems)
        await paginator.respond(ctx.interaction, ephemeral = False)
    
def setup(bot: discord.Bot):
    bot.add_cog(ItemSearch(bot))