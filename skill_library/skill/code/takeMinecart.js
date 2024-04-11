async function takeMinecart(bot) {
    // find minecart
    let minecart = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
        let minecart = bot.nearestEntity(entity => {
          return entity.name === "minecart" && entity.position.distanceTo(bot.entity.position) < 32;
        });
        return minecart;
      });
      if (!minecart) {
        bot.chat("Could not find a minecart.");
        return;
      }
    await bot.pathfinder.goto(new GoalBlock(minecart.position.x, minecart.position.y, minecart.position.z));
    bot.chat(`${minecart.position}`);
    await bot.activateEntity(minecart);
}