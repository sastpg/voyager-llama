async function summonMob(bot, n = 1, r = 8, type = "zombie") {
    // let n = 1;              number of monsters
    // let r = 8;              env size
    // let type = "zombie";    type of monsters
    for (let i = 0; i < n; i++) {
        let x = Math.random() * (2 * r - (-2 * r)) + (-2 * r);
        let z = Math.random() * (2 * r - (-2 * r)) + (-2 * r);
        await bot.chat(`/summon ~${x} ~ ~${z} minecraft:"${type}"`);
    }
}