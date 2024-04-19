async function getAnimal(bot, type = "sheep", position = (0,0,0)) {
    // let type = "sheep"   type of animals
    // let position = (0,0,0)   dest pos
    let wheatSeedsCount = bot.inventory.count(mcData.itemsByName.wheat_seeds.id);
    let wheatCount = bot.inventory.count(mcData.itemsByName.wheat.id);
    let carrotsCount = bot.inventory.count(mcData.itemsByName.carrot.id);
    let wheatSeed = bot.inventory.findInventoryItem(mcData.itemsByName.wheat_seeds.id);
    let wheat = bot.inventory.findInventoryItem(mcData.itemsByName.wheat.id);
    let carrot = bot.inventory.findInventoryItem(mcData.itemsByName.carrot.id);
    if (type = "sheep" || "cow") {
        if (wheatCount <= n) {
            bot.chat("Not enough wheat for feeding.");
            return;
        }
        await bot.equip(wheat, "hand");
    } else if (type = "chichken") {
        if (wheatSeedsCount <= n) {
            bot.chat("Not enough wheat seeds for feeding.");
            return;
        }
        await bot.equip(wheatSeed, "hand");
    } else if (type = "pig") {
        if (carrotsCount <= n) {
            bot.chat("Not enough carrots for feeding.");
            return;
        }
        await bot.equip(carrot, "hand");
    } else {
        bot.chat("undefined type.");
        return;
    }
    
    let animal = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        let entity = bot.nearestEntity(entity => {
            return entity.name === type && entity.position.distanceTo(bot.entity.position) < 32;
        });
        return entity;
    });
    if (!animal) {
        bot.chat(`Could not find a ${type}.`);
        return;
    }
    await bot.pathfinder.goto(new GoalBlock(position.x, position.y, position.z));
}