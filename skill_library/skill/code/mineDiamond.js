async function mineDiamond(bot) {
    let ironPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.iron_pickaxe.id);
    if (!ironPickaxe) {
      await craftIronPickaxe(bot);
      ironPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.iron_pickaxe.id);
      await bot.equip(ironPickaxe, "hand");
    }
    await exploreUntil(bot, new Vec3(0, -1, 0), 60, () => {
      const foundDiamond = bot.findBlock({
        matching: mcData.blocksByName.diamond_ore.id,
        maxDistance: 32
      });
      return foundDiamond;
    });
    await mineBlock(bot, "diamond_ore", 1);
    bot.chat("1 diamond mined.");
  }