async function depositIntoChest(bot) {
    let pos = await placeChest(bot);
    await bot.chat(JSON.stringify(bot.inventory))
    for (let slot = 0; slot < bot.inventory.slots.length; slot++) {
        let item = bot.inventory.slots[slot];
        if (item) {
            let item_name = item.name;
            // deposit non-iron and non-diamond items into chest
            if (!item_name.includes('diamond') && !item_name.includes('iron')) {
                await depositItemIntoChest(bot, pos, item);
            }
        }
    }
}