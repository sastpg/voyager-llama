async function combatEnv(bot) {
    let h = 10;
    let r = 20;
    let y = 150;
    if (y + 2 * r >= 320) {
        bot.chat("upper bound exceeded.");
        return;
    } else if (y <= -64) {
        bot.chat("lower bound exceeded.");
        return;
    } else if ((2*r + 1) * (2*r + 1) * (h + 1) >= 32768) {
        bot.chat("Too many blocks."); // fill max 32768
        return;
    }
    // kill potential mobs and set difficulty to easy for summoning
    await bot.chat("/difficulty peaceful")
    await bot.chat("/difficulty easy")
    // env set
    await bot.chat(`/fill ~${-r} ${y} ~${-r} ~${r} ${y+h} ~${r} minecraft:sea_lantern`);
    await bot.chat(`/fill ~${-(r-1)} ${y+1} ~${-(r-1)} ~${r-1} ${y+h-1} ~${r-1} minecraft:air`);
    await bot.chat(`/tp @p ~ ${y+1} ~`);
}