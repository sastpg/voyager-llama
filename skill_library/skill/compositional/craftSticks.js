async function craftSticks(bot) {
    const requiredPlanks = 2;
    const logNames = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log"];
    let totalPlanksCount = await getPlanksCount(bot);;
    const logInInventory = logNames.find(logName => bot.inventory.count(mcData.itemsByName[logName].id) > 0);
    // If not enough planks
    if (totalPlanksCount < requiredPlanks) {
      await craftWoodenPlanks(bot);
      bot.chat("Planks crafted.");
    }
    await craftItem(bot, "stick", 1);
    bot.chat("4 sticks crafted.");
  }