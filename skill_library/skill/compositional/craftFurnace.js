async function craftFurnace(bot) {
  // Check if there are enough cobblestones in the inventory
  const cobblestoneCount = bot.inventory.count(mcData.itemsByName.cobblestone.id);

  // If not, check wooden pickaxe and mine the required cobblestones
  const woodenPickaxe = bot.inventory.count(mcData.itemsByName.wooden_pickaxe.id)
  if (cobblestoneCount < 8) {
    if (woodenPickaxe < 1)
      await craftWoodenPickaxe(bot);
    await mineBlock(bot, "stone", 8 - cobblestoneCount);
    bot.chat("Collected cobblestone.");
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

  // Craft a furnace using the crafting table
  await craftItem(bot, "furnace", 1);
  bot.chat("Crafted a furnace.");
}