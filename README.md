# Voyager-llama

Mine wood log:

<video id="video" controls="" preload="none" poster="">
      <source id="webm" src="./images/MineWoodLog.webm" type="video/webm">
</videos>

Craft a crafting table:

<video id="video" controls="" preload="none" poster="">
      <source id="webm" src="./images/CraftTable.webm" type="video/webm">
</videos>



1. 由于回家了，调用服务器上部署的llama需要校网，所以暂时先用阿里云的llama API 替换一下。申请链接：[LLaMa2大语言模型有哪些API接口_模型服务灵积(DashScope)-阿里云帮助中心 (aliyun.com)](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-11)。初次会给一定的使用额度，在voyager/llama.py文件夹中替换API key。

2. 架构图

   ![](./images/arch.svg)

   3. prompt

      具体示例，或许有些设计还有点冗长，但是至少现在llama2-13b能够回答。

      - Planner Agent:

        `System Message`:

        ```
        You are a helpful assistant that generates a curriculum of subgoals to complete any Minecraft task specified by me.
        
        I'll give you a final task and my current inventory, you need to decompose the task into a list of subgoals based on my inventory.
        
        You must follow the following criteria:
        1) Return a Python list of subgoals that can be completed in order to complete the specified task.
        2) Each subgoal should follow a concise format, such as "Mine [quantity] [block]", "Craft [quantity] [item]", "Smelt [quantity] [item]", "Kill [quantity] [mob]", "Cook [quantity] [food]", "Equip [item]".
        3) Include each level of necessary tools as a subgoal, such as wooden, stone, iron, diamond, etc.
        
        You should only respond in JSON format as described below:
        ["subgoal1", "subgoal2", "subgoal3", ...]
        Ensure the response can be parsed by Python `json.loads`, e.g.: no trailing commas, no single quotes, etc.
        ```

        `Huamn Message`:

        ```
        Inventory (0/36): ...
        
        Task: ...
        ```

      - Action Agent:

        `System Message`:

        ```
        You are a helpful assistant that decides Mineflayer javascript code to complete any Minecraft task specified by me.
        
        I will give you
        Task: The task I need to complete in this stage.
        Programs: The description of relevant programs that may use to complete the task.
        
        You will choose only one program based on the description. You should only respond in the format as described below:
        RESPONSE FORMAT:
            1) ```your selected program name```
            2) Reason you choose the program.
        ```

        `Huamn Message`:

        ```
        Task: Craft a crafting table
        
        Programs:
        Name: craftCraftingTable; Description: The function crafts a crafting table using oak planks. It first checks if there are enough oak planks in the inventory, and if not, crafts oak planks from oak logs. Then, it crafts a crafting table using the oak planks.
        
        Name: craftWoodenPickaxe; Description: The function crafts a wooden pickaxe using oak planks, sticks, and a crafting table. It checks if there are enough oak planks and sticks in the inventory, and crafts them if necessary. Then, it places a crafting table near the bot and uses it to craft a wooden pickaxe.
        
        Name: craftWoodenHoe; Description: The function crafts a wooden hoe using oak planks and sticks. If there are not enough oak planks, it crafts them from oak logs. If there are not enough sticks, it crafts them from oak planks. Then, it places a crafting table near the bot and uses it to craft a wooden hoe.
        
        Name: craftChest; Description: The function crafts a chest using a crafting table and oak planks. If there are not enough oak planks in the inventory, it crafts oak planks from oak logs. Once there are enough oak planks, it places a crafting table near the bot and crafts a chest using the crafting table.
        
        Name: craftAcaciaPlanksAndSticks; Description: The function is about crafting 20 acacia planks and 10 sticks. It checks if there are enough acacia logs in the inventory, and if not, it mines more acacia logs. Then it crafts 20 acacia planks from the acacia logs. If there are not enough acacia planks in the inventory to craft 10 sticks, it mines more acacia logs and crafts more acacia planks. Finally, it crafts 10 sticks from the acacia planks.
        ```

      - Comment Agent:

        `System Message`:

        ```
        You are required to evaluate if I have met the task requirements in Minecraft. Exceeding the task requirements is also considered a success while failing to meet them requires you to provide critique to help me improve.
        
        I will give you the following information:
        
        Equipment: My final equipment. For crafting tasks, I sometimes equip the crafted item.
        Inventory (xx/36): My final inventory. For mining and smelting tasks, you only need to check inventory.
        Chests: If the task requires me to place items in a chest, you can find chest information here.
        Task: The objective I need to accomplish.
        
        You should only respond in JSON format as described below:
        {
            "reasoning": "reasoning",
            "success": boolean,
            "critique": "critique",
        }
        Ensure the response can be parsed by Python `json.loads`, e.g.: no trailing commas, no single quotes, etc.
        ```

        `Human Message`:

        ```
        Equipment: [None, None, None, None, 'oak_log', None]
        
        Inventory (5/36): {'oak_planks': 8, 'oak_log': 9, 'crafting_table': 2, 'oak_sapling': 4, 'stick': 1}
        
        Chests: None
        
        Task: Craft a crafting table
        ```

   4. 未来工作

      技能图？排列组合？
