async function smeltAllRawGold(bot) {
    // Check if there is a furnace and some coals in the inventory
    const furnaceItem = bot.inventory.findInventoryItem(mcData.itemsByName.furnace.id);
    const coal = bot.inventory.findInventoryItem(mcData.itemsByName.coal.id);
    let rawGoldCount = bot.inventory.count(mcData.itemsByName.raw_gold.id)
    // check raw gold
    if (!rawGoldCount) {
        return;
    }
    // If not, craft a furnace using the available cobblestone
    if (!furnaceItem) {
        await craftFurnace(bot);
    }
    // Place the furnace near the bot
    const furnacePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "furnace", furnacePosition);
    if (!coal)
        await mineFiveCoalOres(bot);
    // Smelt all raw gold using the available coal as fuel
    await smeltItem(bot, "raw_gold", "coal", rawGoldCount);
    bot.chat("Raw gold smelted.");
}