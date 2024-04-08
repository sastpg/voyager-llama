async function craftStoneAxe(bot) {
    // Check if there are enough cobblestone and sticks in the inventory
    const cobblestoneCount = bot.inventory.count(mcData.itemsByName.cobblestone.id);
    const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
    // If not enough cobblestone or sticks, collect the required items
    if (cobblestoneCount < 3) {
      // Check wooden pickaxe
      const woodenPickaxe = bot.inventory.count(mcData.itemsByName.wooden_pickaxe.id)
      if (woodenPickaxe) {
        await bot.equip(woodenPickaxe, "hand");
      } else {
        await craftWoodenPickaxe(bot);
        const woodenPickaxe1 = bot.inventory.findInventoryItem(mcData.itemsByName.wooden_pickaxe.id);
        await bot.equip(woodenPickaxe1, "hand");
      }
      await mineBlock(bot, "stone", 3 - cobblestoneCount);
      bot.chat("Collected cobblestone.");
    }
    if (sticksCount < 2) {
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
    // Craft a stone axe using the crafting table
    await craftItem(bot, "stone_axe", 1);
    bot.chat("Crafted a stone axe.");
  }