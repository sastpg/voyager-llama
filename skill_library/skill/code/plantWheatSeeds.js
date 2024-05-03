async function plantWheatSeeds(bot) {
  // check seeds
  const seeds = bot.inventory.findInventoryItem(mcData.itemsByName.wheat_seeds.id);
  if (!seeds) {
    await collectWheatSeeds(bot);
  }
  await plantSeeds(bot, "wheat_seeds");
}