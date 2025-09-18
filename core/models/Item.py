from dataclasses import dataclass
from typing import Dict, List
import discord




from core.env import itemImageAddress, itemSoloAddress
from core.models.Crate import Crate

@dataclass
class Item:
    """Helper class to standardize Items
    """
    id: int
    
    CrateID: int
    TagPrimary: str
    TagSecondary: str
    TagTertiary: str
    TagQuaternary: str
    TagQuinary: str
    WinPercentage: str
    RarityHuman: str
    ItemName: str    
    Notes: str
    ItemHuman: str

def dictToItem(item: Dict[str, str]):
    return Item(
            int(item["id"]),
            int(item["CrateID"]),
            item["TagPrimary"],
            item["TagSecondary"],
            item["TagTertiary"],
            item["TagQuaternary"],
            item["TagQuinary"],
            item["WinPercentage"],
            item["RarityHuman"],
            item["ItemName"],
            item["Notes"],
            item["ItemHuman"]
            ) # type: ignore


async def itemToEmbed(item: Item, crateList: List[Crate], timesSeen: int | None) -> discord.Embed:
    embed = discord.Embed(title = f"{item.ItemName}",
                      url=f"{itemSoloAddress}/{item.id}",
                      colour=0x00b0f4)
    if item.CrateID:
        crateName = [x for x in crateList if item.CrateID == x.id][0].CrateName
        embed.add_field(name = "Crate",
                        value = f"{crateName}",
                        inline = True)
    if item.TagPrimary:
        embed.add_field(name = "Primary Tag",
                        value = f"{item.TagPrimary}",
                        inline = True)
    if item.TagSecondary:
        embed.add_field(name = "Secondary Tag",
                        value = f"{item.TagSecondary}",
                        inline = True)
    if item.TagTertiary:
        embed.add_field(name = "Tertiary Tag",
                        value = f"{item.TagTertiary}",
                        inline = True)
    if item.TagQuaternary:
        embed.add_field(name = "Quaternary Tag",
                        value = f"{item.TagQuaternary}",
                        inline = True)
    if item.TagQuinary:
        embed.add_field(name = "Quinary Tag",
                        value = f"{item.TagQuinary}",
                        inline = True)
    if item.Notes:
        embed.add_field(name = "Notes",
                        value = f"{item.Notes}",
                        inline = False)

    embed.set_image(url=f"attachment://{item.id}.png")
    if timesSeen:
        embed.set_footer(text=f"Times Searched: {timesSeen}")
    return embed