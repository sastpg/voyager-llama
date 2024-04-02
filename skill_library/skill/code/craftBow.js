async function craftBow(bot) {
    // Check if there are enough strings and sticks in the inventory
    const stringsCount = bot.inventory.count(mcData.itemsByName.string.id);
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
    // If not enough strings or sticks, collect the required items
    if (stringsCount < 3) {
      bot.chat("Not enough strings.")
      return;
    }
    if (sticksCount < 3) {
      await craftSticks(bot);
      bot.chat("Crafted sticks.");
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
    const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "crafting_table", craftingTablePosition);
    // Craft a bow using the crafting table
    await craftItem(bot, "bow", 1);
    bot.chat("Crafted a bow.");
  }