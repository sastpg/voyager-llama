async function craftDiamondShovel(bot) {
    // Check if there are enough diamonds and sticks in the inventory
    let diamondsCount = bot.inventory.count(mcData.itemsByName.diamond.id);
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
  
    // If not enough diamonds or sticks, collect the required items.
    if (sticksCount < 2) {
      await craftSticks(bot);
      bot.chat("Crafted sticks.");
    }
    while (diamondsCount < 1) {
      await mineDiamond(bot);
      diamondsCount = bot.inventory.count(mcData.itemsByName.diamond.id);
    }
    bot.chat("Collected diamonds.");
    // check if crafting table is in the inventory
    const craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
    // If not, craft a crafting table
    if (craftingTableCount === 0) {
      await craftCraftingTable(bot);
    }
    // Place the crafting table near the bot
    const craftingTablePosition = await findSuitablePosition(bot);
    await placeItem(bot, "crafting_table", craftingTablePosition);
  
    // Craft an diamond shovel using the crafting table
    await craftItem(bot, "diamond_shovel", 1);
    bot.chat("Crafted an diamond shovel.");
  }