async function collectCarrots(bot) {
    while (True) {
        // Use the exploreUntil function to find carrots
        const carrots = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        const carrots = bot.findBlocks({
            matching: block => block.name === "carrots",
            maxDistance: 32,
            count: 1
        });
        return carrots.length >= 1 ? carrots : null;
        });
        if (!carrots) {
            bot.chat("Could not find enough carrots.");
            break;
        }
        // Mine carrots using the mineBlock function
        await mineBlock(bot, "carrots", 1);
    }
  }