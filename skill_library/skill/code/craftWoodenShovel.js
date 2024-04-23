async function craftWoodenShovel(bot) {
    let totalPlanksCount = await getPlanksCount(bot);
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
    // Check if there are enough planks and sticks in the inventory
    if (totalPlanksCount < 1) {
      await craftWoodenPlanks(bot);
    }
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
    const craftingTablePosition = await findSuitablePosition(bot);
    await placeItem(bot, "crafting_table", craftingTablePosition);
  
    // Craft a wooden shovel using the crafting table
    await craftItem(bot, "wooden_shovel", 1);
    bot.chat("Crafted a wooden shovel.");
  }