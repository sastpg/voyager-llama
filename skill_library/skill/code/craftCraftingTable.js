async function craftCraftingTable(bot) {
  // check log or planks
  const logNames = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log"];
  const planksNames = ["oak_planks", "birch_planks", "spruce_planks", "jungle_planks", "acacia_planks", "dark_oak_planks", "mangrove_planks"]
  const planksCount = bot.inventory.count({
    matching: block => planksNames.includes(block.name),
  });
  if (planksCount >= 4) {
    // Craft a crafting table using planks
    await craftItem(bot, "crafting_table", 1);
    bot.chat("Crafted a crafting table.");
  }
  // if no enough planks
  const logInInventory = logNames.find(logName => bot.inventory.count(mcData.itemsByName[logName].id) > 0);
  // if no logs, mine logs first
  if (!logInInventory) {
    bot.chat("No wooden log in inventory. Mining a wooden log...");
    await mineWoodLog(bot);
  }
  const logInInventory1 = logNames.find(logName => bot.inventory.count(mcData.itemsByName[logName].id) > 0);
  // craft planks using correspongding logs
  const logIndex = logNames.indexOf(logInInventory1);
  const plankName = planksNames[logIndex];
  bot.chat(`Crafting 4 ${plankName}...`);
  await craftItem(bot, plankName, 1);
  bot.chat(`4 ${plankName} crafted.`);

  // Craft a crafting table using planks
  await craftItem(bot, "crafting_table", 1);
  bot.chat("Crafted a crafting table.");
}