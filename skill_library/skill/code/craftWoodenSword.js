async function craftWoodenSword(bot) {
    const plankNames = ["oak_planks", "birch_planks", "spruce_planks", "jungle_planks", "acacia_planks", "dark_oak_planks", "mangrove_planks"];
    let totalPlanksCount = 0;
    for (const plankName of plankNames) {
      const plankId = mcData.itemsByName[plankName].id;
      const plankCount = bot.inventory.count(plankId);
      totalPlanksCount += plankCount;
    }
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
    // Check if there are enough planks and sticks in the inventory
    if (totalPlanksCount < 2) {
      await craftWoodenPlanks(bot);
    }
    if (sticksCount < 1) {
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
  
    // Craft a wooden sword using the crafting table
    await craftItem(bot, "wooden_sword", 1);
    bot.chat("Crafted a wooden sword.");
  }