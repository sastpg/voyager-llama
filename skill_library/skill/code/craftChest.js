async function craftChest(bot) {
    // Check if there are enough planks in the inventory
    const planksNames = ["oak_planks", "birch_planks", "spruce_planks", "jungle_planks", "acacia_planks", "dark_oak_planks", "mangrove_planks"]
    let planksCount = bot.inventory.count({matching: block => planksNames.includes(block.name)});
    // If not, craft planks from logs
    while (planksCount < 8) {
      await craftWoodenPlanks(bot);
      planksCount = bot.inventory.count({matching: block => planksNames.includes(block.name)});
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
    // Craft a chest using the crafting table
    await craftItem(bot, "chest", 1);
    bot.chat("Crafted a chest.");
  }