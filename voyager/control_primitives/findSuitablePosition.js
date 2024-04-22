async function findSuitablePosition(bot) {
  const offsets = [
      new Vec3(1, 0, 0),
      new Vec3(-1, 0, 0),
      new Vec3(0, 0, 1),
      new Vec3(0, 0, -1),
      new Vec3(1, 0, 1),
      new Vec3(-1, 0, 1),
      new Vec3(-1, 0, 1),
      new Vec3(-1, 0, -1),
      new Vec3(1, 1, 0),
      new Vec3(-1, 1, 0),
      new Vec3(0, 1, 1),
      new Vec3(0, 1, -1),
      new Vec3(1, 1, 1),
      new Vec3(-1, 1, 1),
      new Vec3(-1, 1, 1),
      new Vec3(-1, 1, -1),
      new Vec3(0, 2, 0)
  ]
  for (const offset of offsets) {
      const pos = bot.entity.position.offset(offset.x, offset.y, offset.z);
      const block = bot.blockAt(pos);
      // bot.chat(`offset: ${offset}; block name: ${block.name}`);
      if (block.name == "air") {
          return pos;
      }
  }
  return null;
}