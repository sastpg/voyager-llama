async function collectWheat(bot) {
    // Use the exploreUntil function to find wheat
    const wheat = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
    const wheat = bot.findBlocks({
        matching: block => block.name === "wheat",
        maxDistance: 32,
        count: 1
    });
    return wheat.length >= 1 ? wheat : null;
    });
    if (!wheat) {
        bot.chat("Could not find enough wheat.");
        return;
    }
    const block = bot.blockAt(wheat[0]);
    await bot.pathfinder.goto(new GoalBlock(wheat[0].x, wheat[0].y, wheat[0].z));
    await bot.dig(block);
  }