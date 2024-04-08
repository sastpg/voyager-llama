async function summonMob(bot, n = 1, r = 8, type = "zombie") {
    for (let i = 0; i < n; i++) {
        let x = Math.random() * (2 * r - (-2 * r)) + (-2 * r);
        let z = Math.random() * (2 * r - (-2 * r)) + (-2 * r);
        await bot.chat(`/summon ~${x} ~ ~${z} minecraft:"${type}"`);
    }
}