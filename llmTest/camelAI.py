# -*- coding: utf-8 -*-
import sys, pathlib
# 把“源码根目录”插到第一位
sys.path.insert(0, str(pathlib.Path('/data/huangyc/Document2All/camel').resolve()))
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.agents import ChatAgent
from camel.toolkits import SearchToolkit
from camel.messages import BaseMessage
from jinja2 import Template
from PIL import Image
test="""
please summary the paper blow

{{paper}}
"""

tem=Template(test)

paper_path="/data/huangyc/Document2All/fullPipeline/output/demo2/demo2.md"


with open(paper_path,'r',encoding='utf-8') as f:
    paper_info=f.read()

prompt=tem.render(paper=paper_info)


model = ModelFactory.create(
  model_platform=ModelPlatformType.QWEN,
  model_type=ModelType.QWEN_VL_MAX,
  model_config_dict={"temperature": 0.0},
)

agent = ChatAgent(model=model)
#search_tool = SearchToolkit().search_duckduckgo

#url = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
img = Image.open("./test.jpg")

# 4. 构造带图的用户消息
user_msg = BaseMessage.make_user_message(
    role_name="User",
    content="please describe this image",
    image_list=[img]          # 关键：把 PIL.Image 列表传进来
)

# 5. 发送并打印结果
response = agent.step(user_msg)
print(response.msg.content)
#agent = ChatAgent(model=model)

#response_1 = agent.step(prompt)
#print(response_1.msgs[0].content)
# CAMEL-AI is the first LLM (Large Language Model) multi-agent framework
# and an open-source community focused on finding the scaling laws of agents.
# ...

#response_2 = agent.step("i am doubuxu,and who are you?")
#print(response_2.msgs[0].content)

#response_3=agent.step("who am i?")
#print(response_3.msgs[0].content)
# The GitHub link to the CAMEL framework is
# [https://github.com/camel-ai/camel](https://github.com/camel-ai/camel).