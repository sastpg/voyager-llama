async function findSuitablePosition(bot) {
    const offsets = [
      new Vec3(1, 0, 0),
      new Vec3(-1, 0, 0),
      new Vec3(0, 0, 1),
      new Vec3(0, 0, -1),
    ];
    for (const offset of offsets) {
      const position = bot.entity.position.offset(offset.x, offset.y, offset.z);
      const block = bot.blockAt(position);
      if (block.name === "air") {
        return position;
      }
    }
    return null;
  }