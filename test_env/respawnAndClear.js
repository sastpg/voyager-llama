async function respawnAndClear(bot) {
    await bot.chat("/tp @a ~1000 ~ ~1000");
    await bot.chat("/kill @a");
    await bot.chat("/clear @a");
    await bot.chat("Teleported to new location and reset inventory.");
}