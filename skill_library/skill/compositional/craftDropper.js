async function craftDropper(bot) {
    // check redstone and cobblestones
    let redstoneCount = bot.inventory.count(mcData.itemsByName.redstone.id);
    let cobblestonesCount = bot.inventory.count(mcData.itemsByName.cobblestone.id);
    if (!redstoneCount) {
        await mineRedstoneOre(bot);
    }
    if (cobblestonesCount < 7) {
        await collectCobblestone(bot);
    }
    await craftItem(bot, "dropper", 1);
    bot.chat("Crafted dropper.");
  }