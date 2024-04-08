async function collectSand(bot) {
    // Check if the bot has a shovel in the inventory
    let shovel = bot.inventory.items().find(item => item.name && item.name.endsWith("_shovel"));
    // If not, craft a wooden shovel using the available resources in the inventory
    if (!shovel) {
      await craftWoodenshovel(bot);
    } else {
      // Equip the shovel
      shovel = bot.inventory.items().find(item => item.name && item.name.endsWith("_shovel"));
      await bot.equip(shovel, "hand");
    }
    // Use the exploreUntil function to find sand blocks
    const sandBlocks = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const sandBlocks = bot.findBlocks({
        matching: block => block.name === "sand",
        maxDistance: 32,
        count: 10
      });
      return sandBlocks.length >= 10 ? sandBlocks : null;
    });
    if (!sandBlocks) {
      bot.chat("Could not find enough sand.");
      return;
    }
    // Mine 10 sand blocks using the mineBlock function
    await mineBlock(bot, "sand", 10);
    bot.chat("10 sand mined.");
  }