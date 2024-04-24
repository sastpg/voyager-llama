async function craftStoneSword(bot) {
    // Check if there are enough cobblestone and sticks in the inventory
    const cobblestoneCount = bot.inventory.count(mcData.itemsByName.cobblestone.id);
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
    // If not enough cobblestone or sticks, collect the required items
    if (sticksCount < 1) {
      await craftSticks(bot);
      bot.chat("Crafted sticks.");
    }
    if (cobblestoneCount < 2) {
      await collectCobblestone(bot, 2 - cobblestoneCount);
    }
    // check if crafting table is in the inventory
    const craftingTableCount = bot.inventory.count(
      mcData.itemsByName.crafting_table.id
    );
    // If not, craft a crafting table
    if (craftingTableCount === 0) {
      await craftCraftingTable(bot);
    }
    // Place the crafting table near the bot
    const craftingTablePosition = await findSuitablePosition(bot);
    await placeItem(bot, "crafting_table", craftingTablePosition);
    // Craft a stone sword using the crafting table
    await craftItem(bot, "stone_sword", 1);
    bot.chat("Crafted a stone sword.");
  }