async function depositIntoChest(bot) {
    let pos = await placeChest(bot);
    for (let slot = 0; slot < bot.inventory.slots.length; slot++) {
        let item = bot.inventory.slots[slot];
        if (item) {
            let item_name = item.name;
            // deposit none-iron and none-diamond items into chest
            if (!item_name.includes('diamond') && !item_name.includes('iron')) {
                await depositItemIntoChest(bot, pos, item_name);
            }
        }
    }
}