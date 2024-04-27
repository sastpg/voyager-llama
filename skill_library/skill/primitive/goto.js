async function goto(bot, x, y, z) {
    await bot.pathfinder.goto(new GoalBlock(x, y, z));
}