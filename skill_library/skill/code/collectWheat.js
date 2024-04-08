async function collectWheat(bot) {
    while (True) {
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
            break;
        }
        // Mine wheat using the mineBlock function
        await mineBlock(bot, "wheat", 1);
    }
  }