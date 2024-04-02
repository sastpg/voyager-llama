async function craftShears(bot) {
    // check if crafting table is in the inventory
    const craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
    // If not, craft a crafting table
    if (craftingTableCount === 0) {
      await craftCraftingTable(bot);
    }
    // Place the crafting table near the bot
    const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "crafting_table", craftingTablePosition);
    // If not enough iron ingots, collect the required items.
    if (ironIngotsCount < 2) {
      await mineFiveIronOres(bot);
      bot.chat("Collected iron ores.");
      await smeltFiveRawIron(bot);
      bot.chat("Smelted iron ores into iron ingots.");
    }
    // Craft a pair of shears using the crafting table
    await craftItem(bot, "shears", 1);
    bot.chat("Crafted a pair of shears.");
  }