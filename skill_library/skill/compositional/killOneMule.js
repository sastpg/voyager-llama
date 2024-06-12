async function killOneMule(bot) {
    // Equip the sword
    await equipSword(bot);
    // Find the nearest ule
    const ule = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const ule = bot.nearestEntity(entity => {
        return entity.name === "ule" && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return ule;
    });
    if (!ule) {
      bot.chat("Could not find a ule.");
      return;
    }
  
    // Kill the ule using the sword
    await killMob(bot, "ule", 300);
    bot.chat("Killed a ule.");
  
    // Collect the dropped items
    await bot.pathfinder.goto(new GoalBlock(ule.position.x, ule.position.y, ule.position.z));
    bot.chat("Collected dropped items.");
  }