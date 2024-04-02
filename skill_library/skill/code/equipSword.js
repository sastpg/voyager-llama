async function equipSword(bot) {
    // Find the best sword in the bot's inventory
    const diamondSword = bot.inventory.findInventoryItem(mcData.itemsByName.diamond_sword.id);
    const ironSword = bot.inventory.findInventoryItem(mcData.itemsByName.iron_sword.id);
    const stoneSword = bot.inventory.findInventoryItem(mcData.itemsByName.stone_sword.id);
    const woodenSword = bot.inventory.findInventoryItem(mcData.itemsByName.wooden_sword.id);
    // Equip the best sword
    if (diamondSword) {
        await bot.equip(diamondSword, "hand");
    } else if (ironSword) {
        await bot.equip(ironSword, "hand");
    } else if (stoneSword) {
        await bot.equip(stoneSword, "hand");
    } else if (woodenSword) {
        await bot.equip(woodenSword, "hand");
    } else {
        bot.chat("No sword in inventory.");
        return;
    }
    bot.chat("Sword equipped.");
  }