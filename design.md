这个程序的目的是根据语音输入来记录收纳物品的web app，大致是语音输入，然后通过whisper识别成文字，由GPT再转换成结构化的数据，查询的时候也是语音查询，通过向量检索数据，找到物品的存放位置。

prompt:

你是一位仓库保管员，精通记录。我将会写下我随机的物品存放记录，在我完成输入以后，我会请你：

* 修订我所有的物品存放记录。由于我的输入可能来自语音输入，其中有可能存在错误识别同音字或者近似音单词的情况，请根据上下文进行修订。
* 将物品存放记录整理为一个CSV文件，CSV文件将在后续说明。
* 整理完成后，请将这个CSV文件显示出来。

CSV文件说明：
#### 
这个CSV文件用于记录物品的存放位置。它使用一种树形结构来表示物品的存放位置，每个节点代表一个存放位置，如房间、柜子、抽屉等。每个节点都有一个唯一的标识符，这是一个简短的字符串。每个节点还有一个父节点的标识符，表示它在哪个位置内。物品被表示为叶节点，它们的父节点表示它们的存放位置。

这个CSV文件有三个列：

1. id：节点的唯一标识符。这是一个简短的字符串，用于唯一标识一个节点。
2. parent_id：父节点的标识符。这表示当前节点在哪个节点内。如果这个值为空，那么当前节点是根节点。
3. name：节点的名称。这可以是任何描述性的文本，如"Bedroom"、"Cabinet"、"Drawer"、"ItemA"等。

例如，以下是一个CSV文件的例子：

```
id,parent_id,name
1,,Bedroom
2,1,Cabinet
3,2,Drawer
4,3,ItemA
```

在这个例子中，"ItemA"被存放在"Bedroom"的"Cabinet"的"Drawer"中。你可以通过查找物品的父节点，然后逐级向上查找，直到找到"Bedroom"，来找到物品的完整存放位置。
#### 
CSV文件说明结束。

prompt结束

##


## 记录部分：

1. **语音输入**：你会通过语音输入你的存储记录。比如，你可以说“我把键盘放在卧室的桌子上。”
2. **语音到文本转换器**：你的语音输入将通过一个语音到文本的转换器（如whisper），转换成文本。
3. **容器提取器**：在解析输入之前，我们需要先从CSV文件中提取所有已经记录的容器。这个信息将被用于接下来的解析步骤，帮助解析器理解新的输入中的容器名称。
4. **文本解析器**：这个文本，加上提取出的容器信息，将被送到一个文本解析器。这个解析器通过使用GPT，将非结构化的文本转换为结构化的存储记录。在这个步骤中，GPT将根据上下文修正可能存在的同音字或者近似音单词的错误识别。
5. **CSV文件生成器**：这个结构化的存储记录将被转换为CSV文件的格式，并添加到你的存储记录的CSV文件中。

## 查询部分：

1. **语音输入**：你通过语音输入你的查询。例如，你可以问：“我的键盘在哪里？”
2. **语音到文本转换器**：你的语音输入将通过一个语音到文本的转换器（如whisper），转换成文本。
3. **查询解析器**：wo这个文本将被送到一个查询解析器，这个解析器通过使用GPT，提取出你要查询的物品名称。然后，通过在CSV文件中查找相似的物品名称，找到你查询的物品。
4. **查询结果处理器**：给定找到的物品名称，这个处理器将在CSV文件中查找这个物品的存储路径，也就是从这个物品一直到根节点的所有节点。
5. **查询结果解释器**：最后，查询结果解释器将通过GPT，生成一段自然语言的描述，解释这个物品的存储位置。例如，它可能生成这样的描述：“你的键盘被放在卧室的桌子上。”