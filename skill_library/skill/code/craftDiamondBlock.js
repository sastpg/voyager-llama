async function craftDiamondBlock(bot) {
    // Check if there are enough diamonds in the inventory
    let diamondsCount = bot.inventory.count(mcData.itemsByName.diamond.id);
    // If not enough diamonds, mine some
    while (diamondsCount < 9) {
      await mineDiamond(bot);
      diamondsCount = bot.inventory.count(mcData.itemsByName.diamond.id);
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
    // Craft an diamond block using the crafting table
    await craftItem(bot, "diamond_block", 1);
    bot.chat("Crafted an diamond block.");
}