async function craftMinecart(bot) {
    // Check if there are enough iron_ingots in the inventory
    let ironIngotsCount = bot.inventory.count(mcData.itemsByName.iron_ingot.id);
    // If not, explore to find and mine iron ores
    if (ironIngotsCount < 5) {
      await mineFiveIronOres(bot);
      await smeltAllRawIron(bot);
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
  
    // Craft a minecart using the crafting table
    await craftItem(bot, "minecart", 1);
    bot.chat("Crafted a minecart.");
  }