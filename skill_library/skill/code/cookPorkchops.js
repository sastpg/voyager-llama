async function cookPorkchops(bot) {
  // Check if there is a furnace and some coals and porks in the inventory
  const furnaceItem = bot.inventory.findInventoryItem(mcData.itemsByName.furnace.id);
  const coal = bot.inventory.findInventoryItem(mcData.itemsByName.coal.id);
  const pork = bot.inventory.findInventoryItem(mcData.itemsByName.porkchop.id);
  // If not, craft a furnace using the available cobblestone
  if (!pork)
    await killOnePig(bot);
  if (!furnaceItem) 
    await craftFurnace(bot);
  if (!coal)
    await mineFiveCoalOres(bot); 
  // Place the furnace near the bot, Smelt 1 porkchops using the available coal as fuel
  const furnacePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "furnace", furnacePosition);
  await smeltItem(bot, "porkchop", "coal", 1);
  bot.chat("1 porkchops cooked.");
}