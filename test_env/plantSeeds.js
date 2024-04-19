async function plantSeeds(bot, type = "wheat_seed") {
    // check seeds
    const seeds = bot.inventory.findInventoryItem(mcData.itemsByName[type].id);
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
    // plant seeds
    await bot.pathfinder.goto(new GoalBlock(farmland.x, farmland.y, farmland.z));
    await bot.lookAt(farmland);
    await bot.activateItem();
}