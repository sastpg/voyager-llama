async function shearOneSheep(bot) {
    // check shears
    let shears = bot.inventory.findInventoryItem(mcData.itemsByName.shears.id);
    if (!shears) {
        await craftShears(bot);
    }
    // Equip the shears
    await bot.equip(shears, "hand");
    // Find the nearest sheep
    let sheep = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      let sheep = bot.nearestEntity(entity => {
        return entity.name === "sheep" && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return sheep;
    });
    if (!sheep) {
      bot.chat("Could not find a sheep.");
      return;
    }
  
    // shear the sheep using the shears
    sheep = bot.nearestEntity(entity => {return entity.name === "sheep" && entity.position.distanceTo(bot.entity.position) < 32;});
    await bot.pathfinder.goto(new GoalBlock(sheep.position.x, sheep.position.y, sheep.position.z));
    await bot.activateEntity(sheep);

    // Collect the dropped items
    await bot.pathfinder.goto(new GoalBlock(sheep.position.x, sheep.position.y, sheep.position.z));
    bot.chat("Collected wools.");
  }