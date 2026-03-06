# Document2ALL

*基于agent把输入的通用文档转换为PPT、Poster、Web和Video等展示形式*

## Baseline1模型

完成了一个可以运行的测试模型，具体模型见下图

![alt text](baseline1.svg)

## baseline2模型

**在baseline1的基础上为contentPlan加上了check**

check提示词效果不好

![alt text](baseline2.svg)

## 微调layout模型

生成海报、网页和ppt的json->html数据对来微调大模型

![alt text](dataGenerate2.drawio.svg)


## 数据集

### 海报

1. Paper2Poster: Towards Multimodal Poster Automation from Scientific Papers提供的测试集 
https://huggingface.co/datasets/Paper2Poster/Paper2Poster

2. f1000research网站批量下载

### 学术网页

1. PAPER2WEB: LET’S MAKE YOUR PAPER ALIVE! 

https://huggingface.co/datasets/FrancisChen1/Paper2Web

### ppt数据

1. 从slideshare和slidescarnival上下载，但是不好搞批量下载。可能得手动下载

2. DOC2PPT: Automatic Presentation Slides Generation from Scientific Documents

提供了论文ppt的每一帧截图，很难处理



## 创新方向

* 通用文档的解析
* 基于HTML文件使用一个模型完成PPT、Poster和Web的展示
* 文档解析阶段用Scene Graph的思路解析文档
* 把parser和plan阶段合并起来，参考VQA的做法
* 输入多文档，输出一个展示文件
* 将文档中的表格等数据转换为更适合展示的数据形式，例如表格->柱状图
* 设计layout模型，对poster人为设定二维阅读顺序
* 智能体的概念，为什么是多智能体，与传统方法的区别。通过多智能体的思路解决多种格式的输出数据