async function plantPumpkinSeeds(bot) {
  // check seeds
  const seeds = bot.inventory.findInventoryItem(mcData.itemsByName.pumpkin_seeds.id);
  await bot.equip(seeds, "hand");
  // find one farmland
  const farmland = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const farmland = bot.findBlocks({
        matching: block => block.name === "farmland",
        maxDistance: 32,
        count: 1
      });
      return farmland.length >= 1 ? farmland : null;
    });
  // plant seed
  const block = bot.blockAt(farmland[0]);
  await bot.pathfinder.goto(new GoalBlock(farmland[0].x, farmland[0].y, farmland[0].z));
  await bot.placeBlock(block, new Vec3(0, 1, 0));
}