async function cookBeef(bot) {
    // Check if there is a furnace and some coals and beef in the inventory
    const furnaceItem = bot.inventory.findInventoryItem(mcData.itemsByName.furnace.id);
    const coal = bot.inventory.findInventoryItem(mcData.itemsByName.coal.id);
    const beef = bot.inventory.findInventoryItem(mcData.itemsByName.beef.id);
    // If not, craft a furnace using the available cobblestone
    if (!beef)
        await killOneCow(bot);
    if (!furnaceItem) 
        await craftFurnace(bot);
    if (!coal)
        await mineFiveCoalOres(bot); 
    await cookFood(bot, "beef");
}