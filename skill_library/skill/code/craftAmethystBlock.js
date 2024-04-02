async function craftAmethystBlock(bot) {
    // Check if there are enough amethyst shards in the inventory
    let amethystsCount = bot.inventory.count(mcData.itemsByName.amethyst_shard.id);
    // If not enough amethyst shards, mine some
    while (amethystsCount < 4) {
      await mineAmethystCluster(bot);
      amethystsCount = bot.inventory.count(mcData.itemsByName.amethyst.id);
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
    // Craft an amethyst block using the crafting table
    await craftItem(bot, "amethyst_block", 1);
    bot.chat("Crafted an amethyst block.");
}