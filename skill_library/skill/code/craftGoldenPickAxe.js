async function craftGoldPickaxe(bot) {
    // smelt all raw gold first
    await smeltAllRawGold(bot);
    // Check if there are enough gold ingots and sticks in the inventory
    const goldIngotsCount = bot.inventory.count(mcData.itemsByName.gold_ingot.id);
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
    // If not enough gold ingots or sticks, collect the required items.
    if (goldIngotsCount < 3) {
      await mineGoldOre(bot);
      goldIngotsCount += 1;
    }
    await smeltAllRawgold(bot);
    if (sticksCount < 2) {
      await craftSticks(bot);
    }
    // check if crafting table is in the inventory
    const craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
    // If not, craft a crafting table
    if (craftingTableCount === 0) {
      await craftCraftingTable(bot);
    }
    // Place the crafting table near the bot
    const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "crafting_table", craftingTablePosition);
    // Craft an gold pickaxe using the crafting table
    await craftItem(bot, "gold_pickaxe", 1);
    bot.chat("Crafted an gold pickaxe.");
  }