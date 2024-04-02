async function mineFiveIronOres(bot) {
  const ironPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.iron_pickaxe.id);
  if (ironPickaxe) {
    await bot.equip(ironPickaxe, "hand");
  } else {
    // Equip the stone pickaxe
    const stonePickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.stone_pickaxe.id);
    if (!stonePickaxe) {
      await craftStonePickaxe(bot);
      const stonePickaxe1 = bot.inventory.findInventoryItem(mcData.itemsByName.stone_pickaxe.id);
      await bot.equip(stonePickaxe1, "hand");
    }
    await bot.equip(stonePickaxe, "hand");
  }

  // Find 5 iron_ore blocks
  const ironOres = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
    const ironOres = bot.findBlocks({
      matching: block => block.name === "iron_ore",
      maxDistance: 32,
      count: 5
    });
    return ironOres.length >= 5 ? ironOres : null;
  });
  if (!ironOres) {
    bot.chat("Could not find enough iron ores.");
    return;
  }

  // Mine the 5 iron_ore blocks
  await mineBlock(bot, "iron_ore", 5);
  bot.chat("5 iron ores mined.");
}