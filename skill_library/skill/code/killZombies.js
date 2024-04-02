async function killZombies(bot) {
    do {
      await equipSword(bot);
      await equipIronArmor(bot);
      // Kill the zombie
      await killMob(bot, "zombie", 300);
      bot.chat("Killed a zombie.");
      } while (true);
  }
  