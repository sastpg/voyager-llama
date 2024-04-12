async function constructionEnv(bot) {
    let r = 5;      // env size
    let y_ofs = 0;  // y offset relative to bot's position
    // params above
    // kill potential monsters
    await bot.chat("/difficulty peaceful")
    await bot.chat(`/fill ~${-r} ~${y_ofs} ~${-r} ~${r} ~${y_ofs} ~${r} minecraft:sea_lantern`);
    await bot.chat(`/fill ~${-r} ~${y_ofs + 1} ~${-r} ~${r} ~${y_ofs + 3} ~${r} minecraft:air`);
    await bot.chat(`/setblock ~${-r} ~${y_ofs} ~${-r} minecraft:diamond_block`);
    await bot.chat(`/setblock ~${r} ~${y_ofs} ~${r} minecraft:diamond_block`);
    await bot.chat("Task: Build a railway between two diamond blocks");
}