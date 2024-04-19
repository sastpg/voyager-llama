async function placeRail(bot, railPosition = (0, 0, 0)) {
    // Check rail
    const rail = bot.inventory.findInventoryItem(mcData.itemsByName.rail.id);
    if (!rail) {
        bot.chat("No rail found in inventory.");
        return;
    }
    // Place the rail
    await placeItem(bot, "rail", railPosition);
}