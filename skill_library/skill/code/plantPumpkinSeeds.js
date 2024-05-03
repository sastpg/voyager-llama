async function plantPumpkinSeeds(bot) {
  // check seeds
  const seeds = bot.inventory.findInventoryItem(mcData.itemsByName.pumpkin_seeds.id);
  if (!seeds) {
    await collectPumpkinSeeds(bot);
  }
  await plantSeeds(bot, "pumpkin_seeds");
}