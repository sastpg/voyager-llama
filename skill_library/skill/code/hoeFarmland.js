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
    // find water
    const water = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        const water = bot.findBlocks({
            matching: block => block.name === "water",
            maxDistance: 4,
            count: 1
        });
        return water.length >= 1 ? water : null;
    });
    if (!water) {
        bot.chat("No water nearby.");
        return;
    }
    // find dirt or grass_block near water
    const dirtNearWater = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        const dirtNearWater = bot.findBlocks({
            matching: block => (block.name === "dirt" ||  block.name === "grass_block"),
            maxDistance: 4,
            count: 10
        });
        return dirtNearWater.length >= 10 ? dirtNearWater : null;
    });
    for (pos of dirtNearWater) {
        // hoe a farmland
        const farmland = bot.blockAt(pos);
        await bot.lookAt(pos);
        await bot.activateBlock(farmland);
        bot.chat(`hoed block at ${pos}`);
    }
}