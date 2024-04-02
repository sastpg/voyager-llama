async function eatCookedPorkchop(bot) {
  // Equip the cooked porkchop in the bot's hand
  const cookedPorkchop = bot.inventory.findInventoryItem(mcData.itemsByName.cooked_porkchop.id);
  if (cookedPorkchop)
    await bot.equip(cookedPorkchop, "hand");
  else
    await cookPorkchops(bot);
  // Equip the cooked porkchop in the bot's hand
  const cookedPorkchop1 = bot.inventory.findInventoryItem(mcData.itemsByName.cooked_porkchop.id);
  await bot.equip(cookedPorkchop1, "hand");
  // Consume the cooked porkchop
  await bot.consume();

  // Send a chat message to indicate the task is completed
  bot.chat("Ate 1 cooked porkchop.");
}