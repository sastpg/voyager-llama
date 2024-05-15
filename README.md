# Voyager-llama
目前llama仍然存在输出格式不能保持一致的问题。
`test.py` farming环境调用示例：
```python
voyager = Voyager(
    mc_port=7293,
    skill_library_dir="./skill_library",
    environment="farming",
)

# 如果learn传入一个参数，表示探索目标；
# 如果不传入参数，自由探索
voyager.learn("shear sheep, obtain milk")
```

`test.py`combat环境调用示例：

```python
voyager = Voyager(
    mc_port=7293,
    skill_library_dir="./skill_library",
    environment="combat",
)

voyager.inference(task="3 zombie")
```

### Skill

部分Skill打算设计成传参（MC位置坐标，Mineflayer的Vec3类，形式（x, y, z））的形式：
在直接执行函数时，相关接口应提供相应的参数解析逻辑。
在检索调用函数时，考虑设计反馈模块用于传参。
另一种可能的方式是，通过反馈模块提出执行skill的坐标，先goto对应坐标，再执行skill，解决了传参问题。

直接执行函数，构建世界地图：voyager.py -> inference -> self.run_raw_skill("函数名") e.g: mineWoodLog.js

### Benchmark

初步考虑四个测试环境：Combat, Planting, Breeding, Railway Construction.
初步设计的prompt位于llama_test目录中。
测试环境生成的JavaScript代码位于test_env目录中。

### Agent

任务分解/规划方面，对于不同环境应读取不同的prompt，并在不同的时间节点执行test_env目录中对应代码搭建测试环境（一般来说是在任务完成时，或规定时间后）。
重新设计反馈模块，同Voyager，在subgoal失败后输出失败原因等信息，可以据此检索到尚未执行的前置技能。
Critic等表现不佳的模块，继续尝试改善prompt。

### Embedding

使用 sentence_transformer 模型替代 openai 模型。

下载模型：

```git
git clone https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2.git
```

复制模型文件夹绝对路径，如 D:\\Voyager\\voyager\\agents\\paraphrase-multilingual-MiniLM-L12-v2

修改 test.py 代码：

```python
# ...

voyager = Voyager(
    mc_port=9705,
    skill_library_dir="./skill_library/trial1",
    reload=False,
    embedding_dir="Your model path"
)

# ...
```

- reload 参数为是否重新更新数据库，当增加新技能（在skills.json中）时置为 True，更新数据库；如果技能库与上次相比没有变化则置为 False
- embedding_dir 参数是向量嵌入模型的文件夹绝对路径



### Arch


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



Mine wood log:

<div>
    <video id="video" controls="" preload="none" poster="">
  <source id="webm" src="./images/MineWoodLog.webm" type="video/webm">
</videos>
</div>



Craft a crafting table:

<div>
<video id="video" controls="" preload="none" poster="">
      <source id="webm" src="./images/CraftTable.webm" type="video/webm">
	</videos>
</div>
