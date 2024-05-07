async function craftIronPickaxe(bot) {
  // smelt all raw iron first
  await smeltAllRawIron(bot);
  // Check if there are enough iron ingots and sticks in the inventory
  const ironIngotsCount = bot.inventory.count(mcData.itemsByName.iron_ingot.id);
  const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);
  // If not enough iron ingots or sticks, collect the required items.
  if (sticksCount < 2) {
    await craftSticks(bot);
  }
  while (ironIngotsCount < 3) {
    await mineIronOre(bot);
    ironIngotsCount += 1;
  }
  await smeltAllRawIron(bot);
  // check if crafting table is in the inventory
  const craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
  // If not, craft a crafting table
  if (craftingTableCount === 0) {
    await craftCraftingTable(bot);
  }
  // Place the crafting table near the bot
  const craftingTablePosition = await findSuitablePosition(bot);
  await placeItem(bot, "crafting_table", craftingTablePosition);
  // Craft an iron pickaxe using the crafting table
  await craftItem(bot, "iron_pickaxe", 1);
  bot.chat("Crafted an iron pickaxe.");
}