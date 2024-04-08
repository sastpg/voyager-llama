async function collectPotatoes(bot) {
    while (True) {
        // Use the exploreUntil function to find potatoes
        const potatoes = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        const potatoes = bot.findBlocks({
            matching: block => block.name === "potatoes",
            maxDistance: 32,
            count: 1
        });
        return potatoes.length >= 1 ? potatoes : null;
        });
        if (!potatoes) {
            bot.chat("Could not find enough potatoes.");
            break;
        }
        // Mine potatoes using the mineBlock function
        await mineBlock(bot, "potatoes", 1);
    }
  }