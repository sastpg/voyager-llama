async function craftCopperBlock(bot) {
    // smelt all raw copper first
    await smeltAllRawCopper(bot);
    // Check if there are enough copper ingots in the inventory
    let copperIngotsCount = bot.inventory.count(mcData.itemsByName.copper_ingot.id);
    // If not enough copper ingots, mine copper ores and smelt them into copper ingots
    while (copperIngotsCount < 9) {
      await minecopperOre(bot);
      copperIngotsCount += 1;
    }
    await smeltAllRawCopper(bot);
    // check if crafting table is in the inventory
    const craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);
    // If not, craft a crafting table
    if (craftingTableCount === 0) {
      await craftCraftingTable(bot);
    }
    // Place the crafting table near the bot
    const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "crafting_table", craftingTablePosition);
    // Craft an copper block using the crafting table
    await craftItem(bot, "copper_block", 1);
    bot.chat("Crafted an copper block.");
}