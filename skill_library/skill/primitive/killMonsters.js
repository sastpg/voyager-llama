async function killMonsters(bot, type = null) {
  // Listen for bot's death
  bot.on('death', () => {
    bot.chat("return false.");
    return false;
  });
  do {
    await equipSword(bot);
    await equipArmor(bot);
    // Find the nearest monster
    const monster = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const monster = bot.nearestEntity(entity => {
        return entity.name === type && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return monster;
    });
    if (!monster) {
      bot.chat(`Could not find a ${type}.`);
      bot.chat("return true.");
      return true;
    }
    // Kill the animal using the sword
    await killMob(bot, type, 300);
    bot.chat(`Killed a ${type}.`);
  
    // Collect the dropped items
    await bot.pathfinder.goto(new GoalBlock(animal.position.x, animal.position.y, animal.position.z));
    bot.chat("Collected dropped items.");
    bot.chat(`Killed a ${type}.`);
    } while (true);
}