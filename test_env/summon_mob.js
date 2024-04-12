async function summonMob(bot) {
    let n = 1;              // number of monsters
    let r = 8;              // env size
    let type = "zombie";    // type of monsters
    // params above
    for (let i = 0; i < n; i++) {
        let x = Math.random() * (2 * r - (-2 * r)) + (-2 * r);
        let z = Math.random() * (2 * r - (-2 * r)) + (-2 * r);
        await bot.chat(`/summon ~${x} ~ ~${z} minecraft:"${type}"`);
    }
}