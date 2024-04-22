async function craftIronHelmet(bot) {
  // smelt all raw iron first
  await smeltAllRawIron(bot);
  // Check if there are enough iron ingots in the inventory
  let ironIngotsCount = bot.inventory.count(mcData.itemsByName.iron_ingot.id);
  // If not enough iron ingots, mine iron ores and smelt them into iron ingots
  while (ironIngotsCount < 5) {
    await mineFiveIronOres(bot);
    await smeltAllRawIron(bot);
    ironIngotsCount = bot.inventory.count(mcData.itemsByName.iron_ingot.id);
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
  // Craft an iron helmet using the crafting table
  await craftItem(bot, "iron_helmet", 1);
  bot.chat("Crafted an iron helmet.");
}