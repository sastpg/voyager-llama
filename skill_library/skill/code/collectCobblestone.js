async function collectCobblestone(bot, n) {
    await equipPickaxeOrCraftOne(bot);
    // Use the exploreUntil function to find cobblestone blocks
    const cobblestoneBlocks = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const cobblestoneBlocks = bot.findBlocks({
        matching: block => block.name === "stone",
        maxDistance: 32,
        count: n
      });
      return cobblestoneBlocks.length >= 10 ? cobblestoneBlocks : null;
    });
    if (!cobblestoneBlocks) {
      bot.chat("Could not find enough cobblestone.");
      return;
    }
    // Mine n cobblestone blocks using the mineBlock function
    await mineBlock(bot, "stone", n);
    bot.chat(`${n} cobblestone mined.`);
  }