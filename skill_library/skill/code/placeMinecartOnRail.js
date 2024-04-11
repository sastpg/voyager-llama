async function placeMinecartOnRail(bot) {
    // check minecart
    const minecart = bot.inventory.findInventoryItem(mcData.itemsByName.minecart.id);
    if (!minecart) {
        bot.chat("No minecart found in inventory.");
        return;
    }
    // find rail
    const rail = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        const rails = bot.findBlocks({
          matching: block => block.name === "rail",
          maxDistance: 32,
          count: 1
        });
        return rails.length >= 1 ? rails[0] : null;
      });
      if (!rail) {
        bot.chat("Could not find rail.");
        return;
      }
    // place the minecart
    // bot.chat(`found rail at ${rail}`);
    bot.chat(`${rail.x} ${rail.y + 1} ${rail.z}`);
    await bot.pathfinder.goto(new GoalBlock(rail.x, rail.y + 1, rail.z));
    await placeItem(bot, minecart, new Vec3(rail.x, rail.y + 1, rail.z));
}