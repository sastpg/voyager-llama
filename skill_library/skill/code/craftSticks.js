async function craftSticks(bot) {
    const requiredPlanks = 2;
    const logNames = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log"];
    const plankNames = ["oak_planks", "birch_planks", "spruce_planks", "jungle_planks", "acacia_planks", "dark_oak_planks", "mangrove_planks"];
    let totalPlanksCount = 0;
    const logInInventory = logNames.find(logName => bot.inventory.count(mcData.itemsByName[logName].id) > 0);
    for (const plankName of plankNames) {
      const plankId = mcData.itemsByName[plankName].id;
      const plankCount = bot.inventory.count(plankId);
      totalPlanksCount += plankCount;
    }
    // If not enough planks
    if (totalPlanksCount < requiredPlanks) {
      bot.chat("Not enough planks. Mining a log and crafting more...");
      if (!logInInventory) {
        await MineWoodLog(bot);
      } else {
        await craftWoodenPlanks(bot);
      }
      bot.chat("Planks crafted.");
    }
  
    await craftItem(bot, "stick", 1);
    bot.chat("4 sticks crafted.");
  }