async function collectDirt(bot) {
    // Check if the bot has a shovel in the inventory
    const shovel = bot.inventory.items().find(item => item.name.endsWith("_shovel"));
    // If not, craft a wooden shovel using the available resources in the inventory
    if (!shovel) {
      await craftWoodenshovel(bot);
    } else {
      // Equip the shovel
      await bot.equip(shovel, "hand");
    }
    // Use the exploreUntil function to find dirt blocks
    const dirtBlocks = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const dirtBlocks = bot.findBlocks({
        matching: block => block.name === "dirt",
        maxDistance: 32,
        count: 10
      });
      return dirtBlocks.length >= 10 ? dirtBlocks : null;
    });
    if (!dirtBlocks) {
      bot.chat("Could not find enough dirt.");
      return;
    }
    // Mine 10 dirt blocks using the mineBlock function
    await mineBlock(bot, "dirt", 10);
    bot.chat("10 dirt mined.");
  }