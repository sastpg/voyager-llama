async function cookFood(bot, type = null) {
    // Check if there is a furnace and some coals and food in the inventory
    const furnaceItem = bot.inventory.findInventoryItem(mcData.itemsByName.furnace.id);
    const coal = bot.inventory.findInventoryItem(mcData.itemsByName.coal.id);
    const food = bot.inventory.findInventoryItem(mcData.itemsByName[type].id);
    // If not, craft a furnace using the available cobblestone
    if (!food) {
      await bot.chat(`No ${type} found in inventory.`);
      return;
    }
    if (!furnaceItem) {
      await bot.chat(`No furnace found in inventory.`);
      return;
    }
    if (!coal) {
      await bot.chat(`No coal found in inventory.`);
    }
    // Place the furnace near the bot, Smelt 1 porkchops using the available coal as fuel
    const furnacePosition = await findSuitablePosition(bot);
    await placeItem(bot, "furnace", furnacePosition);
    await smeltItem(bot, type, "coal", 1);
    bot.chat(`1 ${type} cooked.`);
  }