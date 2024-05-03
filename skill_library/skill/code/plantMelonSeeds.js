async function plantMelonSeeds(bot) {
  // check seeds
  const seeds = bot.inventory.findInventoryItem(mcData.itemsByName.melon_seeds.id);
  if (!seeds) {
    await collectMelonSeeds(bot);
  }
  await plantSeeds(bot, "melon_seeds");
}