async function killOnePlayer(bot) {
    // Equip the sword
    await equipSword(bot);
    // Find the nearest player
    const player = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const player = bot.nearestEntity(entity => {
        return entity.name === "player" && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return player;
    });
    if (!player) {
      bot.chat("Could not find a player.");
      return;
    }
  
    // Kill the player using the sword
    await killMob(bot, "player", 300);
    bot.chat("Killed a player.");
  
    // Collect the dropped items
    await bot.pathfinder.goto(new GoalBlock(player.position.x, player.position.y, player.position.z));
    bot.chat("Collected dropped items.");
  }