import discord
from discord.ext import pages
from typing import List, Tuple

from core.db import getCrateList
from core.models.Item import Item


def makeFile(item: Item):
    return discord.File(f"img/{item.id}.png", filename = f"{item.id}.png", description = f"{item.ItemName}")


def buildPaginator(pageList: List[Tuple[discord.Embed, discord.File]]):
    pagelist = [
        pages.PaginatorButton("first", label="⏪", style=discord.ButtonStyle.green),
        pages.PaginatorButton("prev", label="⬅️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
        pages.PaginatorButton("next", label="➡️", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", label="⏩", style=discord.ButtonStyle.green)
    ]
    prettyPages = []
    for embed, file in pageList:
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

