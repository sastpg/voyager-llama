async function shearOneSheep(bot) {
    // check shears
    let shears = bot.inventory.findInventoryItem(mcData.itemsByName.shears.id);
    // Equip the shears
    await bot.equip(shears, "hand");
    // Find the nearest sheep
    const sheep = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const sheep = bot.nearestEntity(entity => {
        return entity.name === "sheep" && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return sheep;
    });
    if (!sheep) {
      bot.chat("Could not find a sheep.");
      return;
    }
  
    // shear the sheep using the shears
    await bot.lookAt(sheep.position);
    await bot.activateItem();
    
    // Collect the dropped items
    await bot.pathfinder.goto(new GoalBlock(sheep.position.x, sheep.position.y, sheep.position.z));
    bot.chat("Collected wools.");
  }