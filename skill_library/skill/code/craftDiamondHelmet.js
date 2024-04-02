async function craftDiamondHelemt(bot) {
    // Check if there are enough diamond in the inventory
    let diamondsCount = bot.inventory.count(mcData.itemsByName.diamond_ingot.id);
  
    // If not enough diamonds, collect some
    while (diamondsCount < 5) {
      await mineDiamond(bot);
      diamondsCount = bot.inventory.count(mcData.itemsByName.diamond_ingot.id);
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
  
    // Craft an diamond helemt using the crafting table
    await craftItem(bot, "diamond_helemt", 1);
    bot.chat("Crafted an diamond helemt.");
  }