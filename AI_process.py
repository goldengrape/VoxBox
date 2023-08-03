import openai 
from pydantic import BaseModel
from typing import List
import json

from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: str
    parent_id: str
    name: str

class ItemList(BaseModel):
    items: List[Item]

def better_human_input(human_input, model='gpt-4'):
    prompt=f"""
你将按照物品容纳的顺序整理我的语音输入记录。
例如
铅笔放在铅笔盒里，铅笔盒放在书包里，书包放在桌子上，桌子有抽屉，抽屉里还放着书，桌子是书房里的。
应当整理成：
书房里有桌子，桌子里有书包，桌子里有抽屉，书包里有铅笔盒，铅笔盒里有铅笔，抽屉里有书。

以下是我的输入记录：
{human_input}

物品收纳记录如下：
"""

    answer=openai.ChatCompletion.create(
        model=model,
        messages=[
        {'role':'system',"content":"You are a helpful assistant with IQ=120"},
        {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    better_input=answer.choices[0].message.content
    return better_input

def structured_input(human_input,
        model1='gpt-4',
        model2="gpt-3.5-turbo-16k",
        current_id=10, 
        known_containers="",
        debug=False
        ):
    better_input=better_human_input(human_input, model=model1)

    if debug:
        print(better_input)

    prompt=prompt=f"""
你是一位专业的仓库保管员，负责记录物品的存放位置。我将提供物品存放记录，你的任务是：

* 将记录整理为CSV文件，用于描述物品的存放位置。CSV文件中，每个节点代表一个容器（如房间、柜子等）或物品，通过树形结构表示物品的存放位置。每个节点有唯一标识符（id）、父节点标识符（parent_id）、名称（name）。
下面是一个CSV文件示例：

id,parent_id,name
1,,卧室
2,1,柜子
3,2,抽屉
4,3,手机

这表示"手机"被存放在"卧室"的"柜子"的"抽屉"中。

现在，你需要将以下记录整理为CSV文件。新的物品或容器应有新的id，当前id已用到{current_id}，之前的序号已经被占用。

已知的容器有：

{known_containers}

请注意，新的物品或容器必须放入已知的容器中，已知的容器无需重复描述。

新的记录如下：
{better_input}
"""
    response=openai.ChatCompletion.create(
        model=model2,
        messages=[
        {"role": "user", 
        "content": prompt}],
        functions=[
            {"name":"get_storage_recorder",
            "description": "Getting a record of what a user has stored",
            "parameters":ItemList.schema()
            }
        ],
        function_call={"name":"get_storage_recorder"},
        temperature=0,
    )
    output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
    return output['items']