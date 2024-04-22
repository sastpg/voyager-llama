async function craftBed(bot) {
    // Check if there are enough planks and wools in the inventory
    const planksNames = ["oak_planks", "birch_planks", "spruce_planks", "jungle_planks", "acacia_planks", "dark_oak_planks", "mangrove_planks"]
    let planksCount = bot.inventory.count({matching: block => planksNames.includes(block.name)});
    let woolsCount = bot.inventory.count(mcData.itemsByName.white_wool.id);
    // If not, craft planks from logs
    if (planksCount < 3) {
        await craftWoodenPlanks(bot);
    }
    while (woolsCount < 3) {
        await killOneSheep(bot);
        woolsCount = bot.inventory.count(mcData.itemsByName.white_wool.id);
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
    // Craft a bed using the crafting table
    await craftItem(bot, "bed", 1);
    bot.chat("Crafted a bed.");
  }