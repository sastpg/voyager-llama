import { equipSword } from './skill_library/skill/code/equipSword.js';
import { equipArmor } from './skill_library/skill/code/equipArmor.js';
async function killMonsters(bot, type = "zombies") {
    do {
      await equipSword(bot);
      await equipArmor(bot);
      await killMob(bot, `${type}`, 300);
      bot.chat(`Killed a ${type}.`);
      } while (true);
  }