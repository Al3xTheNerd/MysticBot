import discord
from discord.ext import pages

import core.db as db
from core.models.Item import Item, dictToItem
from core.models.Crate import Crate, dictToCrate
from core.models.Item import Item
from core.env import server_name, webAddress

import os, aiohttp
from typing import List, Tuple


symbolsToRemove = [
    "✦", 
    "❂", 
    "■", 
    "☀", 
    "☠", 
    "▲", 
    "❃", 
    "◇", 
    "✿", 
    "♦",
    "❀",
    "♆",
    "๑",
    "⊱",
    "⊰",
    "⋗",
    "⋖",
    "❤",
    "❉",
    "✲",
    "◈"
    ]

def makeFile(item: Item):
    return discord.File(f"img/{server_name}/{item.id}.png", filename = f"{item.id}.png", description = f"{item.ItemName}")

def makeIcon(item: Item):
    path = f"img/{server_name}_Icons/{item.id}.png"
    if os.path.isfile(path):
        return discord.File(path, filename = f"{item.id}_icon.png", description = f"{item.ItemName} Icon")
    else: return None

def buildPaginator(pageList: List[Tuple[discord.Embed, discord.File, discord.File | None]]):
    pagelist = [
        pages.PaginatorButton("first", label="⏪", style=discord.ButtonStyle.green),
        pages.PaginatorButton("prev", label="⬅️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
        pages.PaginatorButton("next", label="➡️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", label="⏩", style=discord.ButtonStyle.green)
    ]
    prettyPages = []
    for embed, file, maybeIcon in pageList:
        if maybeIcon:
            prettyPages.append(pages.Page(embeds=[embed], files = [file, maybeIcon]))
        else:
            prettyPages.append(pages.Page(embeds=[embed], files = [file]))
    inator = pages.Paginator(
                pages = prettyPages, # type: ignore
                show_disabled = True,
                show_indicator = True,
                use_default_buttons = False,
                custom_buttons = pagelist,
                loop_pages = True
            )
    inator.pages
    return inator

async def crateIDToCrateName(id: int) -> str | None:
    crateList = await db.getCrateList()
    if crateList:
        return [x for x in crateList if id == x.id][0].CrateName
    return None

async def updateFromSite():
    async with aiohttp.ClientSession() as session:
        # Get Item List
        infoPieces = ["id", "CrateID", "TagPrimary", "TagSecondary", "TagTertiary", "TagQuaternary", "TagQuinary", "TagSenary", "TagSeptenary", "WinPercentage", "RarityHuman", "ItemName", "Notes", "ItemHuman"]
        headers = { "I-INCLUDED-INFO" : ";".join(infoPieces)}
        async with session.get(f"{webAddress}/items", headers = headers) as response:
            itemRes = await response.json()
        items: List[Item] = []
        if itemRes["data"]:
            items = [dictToItem(x) for x in itemRes["data"]]
        await db.updateItemList(items)
        # Get Crate List
        async with session.get(f"{webAddress}/crates") as response:
            crateRes = await response.json()
        crates: List[Crate] = []
        if crateRes:
            crates = [dictToCrate(x) for x in crateRes]
        await db.updateCrateList(crates)
        # Get Tag List
        async with session.get(f"{webAddress}/tags") as response:
            tagRes = await response.json()
        tags = []
        if tagRes:
            tags = tagRes
        await db.updateTagList(tagRes)