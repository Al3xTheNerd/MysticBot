import discord
from discord.ext import pages
from typing import List, Tuple

from core.db import getCrateList
from core.models.Item import Item
from core.env import server_name
import os

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
    crateList = await getCrateList()
    if crateList:
        return [x for x in crateList if id == x.id][0].CrateName
    return None

