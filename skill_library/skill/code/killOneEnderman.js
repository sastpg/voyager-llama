async function killOneEnderman(bot) {
    // Equip the sword
    await equipSword(bot);
    // Find the nearest enderman
    const enderman = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const enderman = bot.nearestEntity(entity => {
        return entity.name === "enderman" && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return enderman;
    });
    if (!enderman) {
      bot.chat("Could not find a enderman.");
      return;
    }
  
    // Kill the enderman using the wooden sword
    await killMob(bot, "enderman", 300);
    bot.chat("Killed a enderman.");
  
    // Collect the dropped items
    await bot.pathfinder.goto(new GoalBlock(enderman.position.x, enderman.position.y, enderman.position.z));
    bot.chat("Collected dropped items.");
  }