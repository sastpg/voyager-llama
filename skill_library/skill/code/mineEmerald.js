async function mineEmerald(bot) {
    let diamondPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.diamond_pickaxe.id);
    let ironPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.iron_pickaxe.id);
    if (diamondPickaxe) {
        await bot.equip(diamondPickaxe, "hand");
    } else if (ironPickaxe) {
        await bot.equip(ironPickaxe, "hand");
    } else {
      await craftIronPickaxe(bot);
      ironPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.iron_pickaxe.id);
      await bot.equip(ironPickaxe, "hand");
    }
    await exploreUntil(bot, new Vec3(0, -1, 0), 60, () => {
      const foundEmerald = bot.findBlock({
        matching: mcData.blocksByName.Emerald_ore.id,
        maxDistance: 32
      });
      return foundEmerald;
    });
    await mineBlock(bot, "emerald_ore", 1);
    bot.chat("1 emerald mined.");
  }