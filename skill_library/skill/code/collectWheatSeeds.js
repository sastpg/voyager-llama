async function collectWheatSeeds(bot) {
    // Check seeds
    let seedsCount = bot.inventory.count(mcData.itemsByName.wheat_seeds.id);
    // Use the exploreUntil function to find grass
    const grass = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
    const grass = bot.findBlocks({
        matching: block => block.name === "grass",
        maxDistance: 32,
        count: 10
    });
    return grass.length >= 10 ? grass : null;
    });
    if (!grass) {
        bot.chat("Could not find enough grass.");
        return;
    }
    let newSeedsCount = bot.inventory.count(mcData.itemsByName.wheat_seeds.id);
    do {
        // Mine 10 grass using the mineBlock function
        await mineBlock(bot, "grass", 10);
        // Check seeds
        newSeedsCount = bot.inventory.count(mcData.itemsByName.wheat_seeds.id);
    } while (newSeedsCount == seedsCount)
    await bot.chat(`${newSeedsCount-seedsCount} wheat seeds collected.`)
  }