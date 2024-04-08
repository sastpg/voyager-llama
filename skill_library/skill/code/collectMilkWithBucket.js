async function collectMilkWithBucket(bot) {
    // check bucket
    let bucket = bot.inventory.findInventoryItem(mcData.itemsByName.bucket.id);
    if (!bucket) {
        await craftBucket(bot);
    }
    // Equip the bucket
    await bot.equip(bucket, "hand");
    // Find the nearest cow
    let cow = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        let cow = bot.nearestEntity(entity => {
            return entity.name === "cow" && entity.position.distanceTo(bot.entity.position) < 32;
            });
            return cow;
        });
        if (!cow) {
            bot.chat("Could not find a cow.");
            return;
        }
    // collect milk
    cow = bot.nearestEntity(entity => {return entity.name === "cow" && entity.position.distanceTo(bot.entity.position) < 32;});
    await bot.pathfinder.goto(new GoalBlock(cow.position.x, cow.position.y, cow.position.z));
    await bot.activateEntity(cow);
  }