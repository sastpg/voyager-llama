async function killSkeletons(bot) {
    do {
      await equipSword(bot);
      await equipIronArmor(bot);
      // Kill the skeleton
      await killMob(bot, "skeleton", 300);
      bot.chat("Killed a skeleton.");
      } while (true);
  }
  