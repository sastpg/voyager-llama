async function hoeFarmland(bot) {
    // check hoe
    const hoe = bot.inventory.findInventoryItem(mcData.itemsByName.diamond_hoe.id)  ||
                bot.inventory.findInventoryItem(mcData.itemsByName.iron_hoe.id)     ||
                bot.inventory.findInventoryItem(mcData.itemsByName.stone_hoe.id)    ||
                bot.inventory.findInventoryItem(mcData.itemsByName.golden_hoe.id)   ||
                bot.inventory.findInventoryItem(mcData.itemsByName.wooden_hoe.id);
    if (!hoe) {
        bot.chat("No hoe found in inventory.");
        return;
    } else {
        await bot.equip(hoe, "hand");
    }

    // hoe a farmland
    const hoePositon = bot.entity.position;
    await bot.lookAt(hoePositon);
    await bot.activateItem();
    bot.chat(`hoed block at ${hoePositon}`);
}