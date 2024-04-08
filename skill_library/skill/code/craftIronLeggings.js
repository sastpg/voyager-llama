async function craftIronLeggings(bot) {
  // smelt all raw iron first
  await smeltAllRawIron(bot);
  // Check if there are enough iron ingots in the inventory
  let ironIngotsCount = bot.inventory.count(mcData.itemsByName.iron_ingot.id);
  // If not enough iron ingots, mine iron ores and smelt them into iron ingots
  while (ironIngotsCount < 7) {
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
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);
  // Craft an iron leggings using the crafting table
  await craftItem(bot, "iron_leggings", 1);
  bot.chat("Crafted an iron leggings.");
}