async function depositIntoChest(bot) {
    let pos = await placeChest(bot);
    for (let slot = 0; slot < bot.inventory.slots.length; slot++) {
        let item = bot.inventory.slots[slot];
        await bot.chat(JSON.stringify(item));
        if (item) {
            let item_name = item.name;
            // deposit non-iron and non-diamond items into chest
            if (!item_name.includes('diamond') && !item_name.includes('iron')) {
                await depositItemIntoChest(bot, pos, item);
            }
        }
    }
}