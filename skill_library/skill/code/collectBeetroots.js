async function collectBeetroots(bot) {
    while (True) {
        // Use the exploreUntil function to find beetroots
        const beetroots = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        const beetroots = bot.findBlocks({
            matching: block => block.name === "beetroots",
            maxDistance: 32,
            count: 1
        });
        return beetroots.length >= 1 ? beetroots : null;
        });
        if (!beetroots) {
            bot.chat("Could not find enough beetroots.");
            break;
        }
        // Mine beetroots using the mineBlock function
        await mineBlock(bot, "beetroots", 1);
    }
  }