from dataclasses import dataclass
from typing import Dict, List
import discord
import os




from core.env import itemImageAddress, itemSoloAddress
from core.models.MiscGroup import MiscGroup

@dataclass
class MiscItem:
    """Helper class to standardize Miscellaneous Items
    """
    id: int
    
    GroupID: int
    ItemName: str
    Notes: str
    ItemHuman: str

def dictToMiscItem(item: Dict[str, str]):
    return MiscItem(
            int(item["id"]),
            int(item["GroupID"]),
            item["ItemName"],
            item["Notes"],
            item["ItemHuman"]
            ) # type: ignore


async def miscItemToEmbed(item: MiscItem, groupList: List[MiscGroup], timesSeen: int | None) -> discord.Embed:
    embed = discord.Embed(title = f"{item.ItemName}",
                      url=f"{itemSoloAddress}/{item.id}",
                      colour=0x00b0f4)
    if item.GroupID:
        groupName = [x for x in groupList if item.GroupID == x.id][0].GroupName
        embed.add_field(name = "Group",
                        value = f"{groupName}",
                        inline = True)
    if item.Notes:
        embed.add_field(name = "Notes",
                        value = f"{item.Notes}",
                        inline = False)

    embed.set_image(url=f"{itemImageAddress.replace("Icons", "Misc_Descriptions")}/{item.id}.png")
    embed.set_thumbnail(url=f"{itemImageAddress.replace("Icons", "Misc_Icons")}/{item.id}.png")
    if timesSeen:
        embed.set_footer(text=f"Times Searched: {timesSeen}")
    return embed