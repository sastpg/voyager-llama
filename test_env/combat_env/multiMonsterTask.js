import { combatEnv } from './combatEnv.js';
import { summonMob } from './summonMob.js';
async function multiMonsterTask(bot, level = 1) {
    // level : difficulty of task
    if (level < 1 || level > 5) {
        bot.chat("No such level.");
        return;
    }
    await combatEnv(bot, 10, 5 + level * 3, 100);
    await summonMob(bot, level, 4 + level * 2, "zombie");
    await summonMob(bot, level, 4 + level * 2, "skeleton");
    await summonMob(bot, level, 4 + level * 2, "spider");
}