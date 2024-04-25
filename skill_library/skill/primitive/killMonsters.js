async function killMonsters(bot, type = null) {
  do {
    await equipSword(bot);
    await equipArmor(bot);
    await killMob(bot, `${type}`, 300);
    bot.chat(`Killed a ${type}.`);
    } while (true);
}