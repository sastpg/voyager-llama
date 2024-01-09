# README

1. 原本chatgpt调用的模式如：

   ```python
   ai_message = self.action_agent.llm(self.messages)
   ```

   其中`ai_message`是chatGPT给出的回答，内容用`AIMessage`这个类“包裹”；`self.messages` 是给chatGPT的输入，是一个数组，包括提示词(也就是我们通常说的内置人格设定，内容用`SystemPrompt`这个类“包裹“)和环境信息等(内容用`HumanPrompt`这个类“包裹“)。这是[langchain](https://zhuanlan.zhihu.com/p/620529542)框架下独有的组件和接口，我们的llama并不支持这样的参数输入。

   原本项目`self.messages`长这个样子：

   ````
   [SystemMessage(content='You are a helpful assistant that writes Mineflayer javascript code to complete any Minecraft task specified by me.
   
   Here are some useful programs written with Mineflayer APIs.
   
   /*
   Explore until find an iron_ore, use Vec3(0, -1, 0) because iron ores are usually underground
   await exploreUntil(bot, new Vec3(0, -1, 0), 60, () => {
       const iron_ore = bot.findBlock({
           matching: mcData.blocksByName["iron_ore"].id,
           maxDistance: 32,
       });
       return iron_ore;
   });
   
   Explore until find a pig, use Vec3(1, 0, 1) because pigs are usually on the surface
   let pig = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
       const pig = bot.nearestEntity((entity) => {
           return (
               entity.name === "pig" &&
               entity.position.distanceTo(bot.entity.position) < 32
           );
       });
       return pig;
   });
   */
   async function exploreUntil(bot, direction, maxTime = 60, callback) {
       /*
       Implementation of this function is omitted.
       direction: Vec3, can only contain value of -1, 0 or 1
       maxTime: number, the max time for exploration
       callback: function, early stop condition, will be called each second, exploration will stop if return value is not null
   
       Return: null if explore timeout, otherwise return the return value of callback
       */
   }
   
   
   // Mine 3 cobblestone: mineBlock(bot, "stone", 3);
   async function mineBlock(bot, name, count = 1) {
       const blocks = bot.findBlocks({
           matching: (block) => {
               return block.name === name;
           },
           maxDistance: 32,
           count: count,
       });
       const targets = [];
       for (let i = 0; i < Math.min(blocks.length, count); i++) {
           targets.push(bot.blockAt(blocks[i]));
       }
       await bot.collectBlock.collect(targets, { ignoreNoPath: true });
   }
   
   
   // Craft 8 oak_planks from 2 oak_log (do the recipe 2 times): craftItem(bot, "oak_planks", 2);
   // You must place a crafting table before calling this function
   async function craftItem(bot, name, count = 1) {
       const item = mcData.itemsByName[name];
       const craftingTable = bot.findBlock({
           matching: mcData.blocksByName.crafting_table.id,
           maxDistance: 32,
       });
       await bot.pathfinder.goto(
           new GoalLookAtBlock(craftingTable.position, bot.world)
       );
       const recipe = bot.recipesFor(item.id, null, 1, craftingTable)[0];
       await bot.craft(recipe, count, craftingTable);
   }
   
   
   // Place a crafting_table near the player, Vec3(1, 0, 0) is just an example, you shouldn't always use that: placeItem(bot, "crafting_table", bot.entity.position.offset(1, 0, 0));
   async function placeItem(bot, name, position) {
       const item = bot.inventory.findInventoryItem(mcData.itemsByName[name].id);
       // find a reference block
       const faceVectors = [
           new Vec3(0, 1, 0),
           new Vec3(0, -1, 0),
           new Vec3(1, 0, 0),
           new Vec3(-1, 0, 0),
           new Vec3(0, 0, 1),
           new Vec3(0, 0, -1),
       ];
       let referenceBlock = null;
       let faceVector = null;
       for (const vector of faceVectors) {
           const block = bot.blockAt(position.minus(vector));
           if (block?.name !== "air") {
               referenceBlock = block;
               faceVector = vector;
               break;
           }
       }
       // You must first go to the block position you want to place
       await bot.pathfinder.goto(new GoalPlaceBlock(position, bot.world, {}));
       // You must equip the item right before calling placeBlock
       await bot.equip(item, "hand");
       await bot.placeBlock(referenceBlock, faceVector);
   }
   
   
   // Smelt 1 raw_iron into 1 iron_ingot using 1 oak_planks as fuel: smeltItem(bot, "raw_iron", "oak_planks");
   // You must place a furnace before calling this function
   async function smeltItem(bot, itemName, fuelName, count = 1) {
       const item = mcData.itemsByName[itemName];
       const fuel = mcData.itemsByName[fuelName];
       const furnaceBlock = bot.findBlock({
           matching: mcData.blocksByName.furnace.id,
           maxDistance: 32,
       });
       await bot.pathfinder.goto(
           new GoalLookAtBlock(furnaceBlock.position, bot.world)
       );
       const furnace = await bot.openFurnace(furnaceBlock);
       for (let i = 0; i < count; i++) {
           await furnace.putFuel(fuel.id, null, 1);
           await furnace.putInput(item.id, null, 1);
           // Wait 12 seconds for the furnace to smelt the item
           await bot.waitForTicks(12 * 20);
           await furnace.takeOutput();
       }
       await furnace.close();
   }
   
   
   // Kill a pig and collect the dropped item: killMob(bot, "pig", 300);
   async function killMob(bot, mobName, timeout = 300) {
       const entity = bot.nearestEntity(
           (entity) =>
               entity.name === mobName &&
               entity.position.distanceTo(bot.entity.position) < 32
       );
       await bot.pvp.attack(entity);
       await bot.pathfinder.goto(
           new GoalBlock(entity.position.x, entity.position.y, entity.position.z)
       );
   }
   
   
   // Get a torch from chest at (30, 65, 100): getItemFromChest(bot, new Vec3(30, 65, 100), {"torch": 1});
   // This function will work no matter how far the bot is from the chest.
   async function getItemFromChest(bot, chestPosition, itemsToGet) {
       await moveToChest(bot, chestPosition);
       const chestBlock = bot.blockAt(chestPosition);
       const chest = await bot.openContainer(chestBlock);
       for (const name in itemsToGet) {
           const itemByName = mcData.itemsByName[name];
           const item = chest.findContainerItem(itemByName.id);
           await chest.withdraw(item.type, null, itemsToGet[name]);
       }
       await closeChest(bot, chestBlock);
   }
   // Deposit a torch into chest at (30, 65, 100): depositItemIntoChest(bot, new Vec3(30, 65, 100), {"torch": 1});
   // This function will work no matter how far the bot is from the chest.
   async function depositItemIntoChest(bot, chestPosition, itemsToDeposit) {
       await moveToChest(bot, chestPosition);
       const chestBlock = bot.blockAt(chestPosition);
       const chest = await bot.openContainer(chestBlock);
       for (const name in itemsToDeposit) {
           const itemByName = mcData.itemsByName[name];
           const item = bot.inventory.findInventoryItem(itemByName.id);
           await chest.deposit(item.type, null, itemsToDeposit[name]);
       }
       await closeChest(bot, chestBlock);
   }
   // Check the items inside the chest at (30, 65, 100): checkItemInsideChest(bot, new Vec3(30, 65, 100));
   // You only need to call this function once without any action to finish task of checking items inside the chest.
   async function checkItemInsideChest(bot, chestPosition) {
       await moveToChest(bot, chestPosition);
       const chestBlock = bot.blockAt(chestPosition);
       await bot.openContainer(chestBlock);
       // You must close the chest after opening it if you are asked to open a chest
       await closeChest(bot, chestBlock);
   }
   
   
   await bot.pathfinder.goto(goal); // A very useful function. This function may change your main-hand equipment.
   // Following are some Goals you can use:
   new GoalNear(x, y, z, range); // Move the bot to a block within the specified range of the specified block. `x`, `y`, `z`, and `range` are `number`
   new GoalXZ(x, z); // Useful for long-range goals that don't have a specific Y level. `x` and `z` are `number`
   new GoalGetToBlock(x, y, z); // Not get into the block, but get directly adjacent to it. Useful for fishing, farming, filling bucket, and beds. `x`, `y`, and `z` are `number`
   new GoalFollow(entity, range); // Follow the specified entity within the specified range. `entity` is `Entity`, `range` is `number`
   new GoalPlaceBlock(position, bot.world, {}); // Position the bot in order to place a block. `position` is `Vec3`
   new GoalLookAtBlock(position, bot.world, {}); // Path into a position where a blockface of the block at position is visible. `position` is `Vec3`
   
   // These are other Mineflayer functions you can use:
   bot.isABed(bedBlock); // Return true if `bedBlock` is a bed
   bot.blockAt(position); // Return the block at `position`. `position` is `Vec3`
   
   // These are other Mineflayer async functions you can use:
   await bot.equip(item, destination); // Equip the item in the specified destination. `item` is `Item`, `destination` can only be "hand", "head", "torso", "legs", "feet", "off-hand"
   await bot.consume(); // Consume the item in the bot's hand. You must equip the item to consume first. Useful for eating food, drinking potions, etc.
   await bot.fish(); // Let bot fish. Before calling this function, you must first get to a water block and then equip a fishing rod. The bot will automatically stop fishing when it catches a fish
   await bot.sleep(bedBlock); // Sleep until sunrise. You must get to a bed block first
   await bot.activateBlock(block); // This is the same as right-clicking a block in the game. Useful for buttons, doors, etc. You must get to the block first
   await bot.lookAt(position); // Look at the specified position. You must go near the position before you look at it. To fill bucket with water, you must lookAt first. `position` is `Vec3`
   await bot.activateItem(); // This is the same as right-clicking to use the item in the bot's hand. Useful for using buckets, etc. You must equip the item to activate first
   await bot.useOn(entity); // This is the same as right-clicking an entity in the game. Useful for shearing sheep, equipping harnesses, etc. You must get to the entity first
   
   
   
   At each round of conversation, I will give you
   Code from the last round: ...
   Execution error: ...
   Chat log: ...
   Biome: ...
   Time: ...
   Nearby blocks: ...
   Nearby entities (nearest to farthest):
   Health: ...
   Hunger: ...
   Position: ...
   Equipment: ...
   Inventory (xx/36): ...
   Chests: ...
   Task: ...
   Context: ...
   Critique: ...
   
   You should then respond to me with
   Explain (if applicable): Are there any steps missing in your plan? Why does the code not complete the task? What does the chat log and execution error imply?
   Plan: How to complete the task step by step. You should pay attention to Inventory since it tells what you have. The task completeness check is also based on your final inventory.
   Code:
       1) Write an async function taking the bot as the only argument.
       2) Reuse the above useful programs as much as possible.
           - Use `mineBlock(bot, name, count)` to collect blocks. Do not use `bot.dig` directly.
           - Use `craftItem(bot, name, count)` to craft items. Do not use `bot.craft` or `bot.recipesFor` directly.
           - Use `smeltItem(bot, name count)` to smelt items. Do not use `bot.openFurnace` directly.
           - Use `placeItem(bot, name, position)` to place blocks. Do not use `bot.placeBlock` directly.
           - Use `killMob(bot, name, timeout)` to kill mobs. Do not use `bot.attack` directly.
       3) Your function will be reused for building more complex functions. Therefore, you should make it generic and reusable. You should not make strong assumption about the inventory (as it may be changed at a later time), and therefore you should always check whether you have the required items before using them. If not, you should first collect the required items and reuse the above useful programs.
       4) Functions in the "Code from the last round" section will not be saved or executed. Do not reuse functions listed there.
       5) Anything defined outside a function will be ignored, define all your variables inside your functions.
       6) Call `bot.chat` to show the intermediate progress.
       7) Use `exploreUntil(bot, direction, maxDistance, callback)` when you cannot find something. You should frequently call this before mining blocks or killing mobs. You should select a direction at random every time instead of constantly using (1, 0, 1).
       8) `maxDistance` should always be 32 for `bot.findBlocks` and `bot.findBlock`. Do not cheat.
       9) Do not write infinite loops or recursive functions.
       10) Do not use `bot.on` or `bot.once` to register event listeners. You definitely do not need them.
       11) Name your function in a meaningful way (can infer the task from the name).
   
   You should only respond in the format as described below:
   RESPONSE FORMAT:
   Explain: ...
   Plan:
   1) ...
   2) ...
   3) ...
   ...
   Code:
   ```javascript
   // helper functions (only if needed, try to avoid them)
   ...
   // main function after the helper functions
   async function yourMainFunctionName(bot) {
     // ...
   }
   ```
   '), HumanMessage(content="Code from the last round: No code in the first round
   
   Execution error: No error
   
   Chat log: None
   
   Biome: forest
   
   Time: noon
   
   Nearby blocks: grass, oak_leaves, oak_log, grass_block, dirt, birch_leaves, birch_log
   
   Nearby entities (nearest to farthest): bat
   
   Health: 20.0/20
   
   Hunger: 20.0/20
   
   Position: x=6.4, y=70.0, z=1.6
   
   Equipment: [None, None, None, None, 'oak_log', None]
   
   Inventory (1/36): {'oak_log': 4}
   
   Chests: None
   
   Task: Mine 1 wood log
   
   Context: You can mine one of oak, birch, spruce, jungle, acacia, dark oak, or mangrove logs.
   
   Critique: None
   
   ")]
   ````

   简化来看，也就是：

   ```
   [SystemMessage(content='You are a helpful assistant ...'),
    HumanMessage(content="Abaab...")
   ]
   ```

   所以说这是一个数组，是原来项目输入给使用了langchain架构的chatGPT的参数。chatGPT返回的消息格式如下：

   ```
   [AIMessage(content=' ...')]
   ```

2. llama参数必须使用下面的格式：

   ```json
   messages = {"messages": [
       {
           "role": 'system',
           "content": "You are a helpful assistant.",
       },  /* role是system，这个就相当于上面的SystemMessage，设定内置人格 */
       {
           "role": 'user',
           "content": "I want to travel to Beijing. Where should I see?",
       }, /* role是user，这个就相当于上面的HumanMessage，用户输入的信息如环境等 */
   ]
   }
   ```

3. 所以在将原来 chatGPT换成llama的时候，我们要将传入的参数改造成符合llama的格式：

   `SystemMessage`和`HumanMessage`类都有`content`成员变量，存储原始的文本。将(1)中的self.messages转化成llama需要的格式：

   ```python
   messages = {"messages": 
       [{'role': 'system', 'content': self.messages[0].content}, 
        # self.messages[0]就是SystemMessage类的一个实例，.content就获得原始的内容
        {'role': 'user', 'content': self.messages[1].content},
        # self.messages[1]就是HumanMessage类的一个实例，.content就获得原始的内容
       ]
   }
   ```

   转换后的messages格式如下：

   ```json
   messages = {"messages": [
       {
           "role": 'system',
           "content": "You are a helpful assistant that writes Mineflayer javascript code to complete any Minecraft task specified by me ...",
       },
       {
           "role": 'user',
           "content": "Code from the last round: No code in the first round ...",
       },
   ]
   }
   ```

4. 经过转换后就可以输入给llama了，直接调用`chat_completion`函数，传入messages参数即可：

   ```python
   from .llama import chat_completion
   ai_message = chat_completion(messages)
   ```

   llama返回的`ai_messages`是纯文本，没有用任何类包裹。

5. 另外我感觉所有的prompt都是预加载好了后调用不同agent的self.llm，不同agent的self.llm其实都是chatGPT，感觉不需要这么多不同的llm啊？

6. 修改一部分的地方：

   `voyager.py -> step()` , `circulumn.py -> run_qa_step2_answer_questions()`

