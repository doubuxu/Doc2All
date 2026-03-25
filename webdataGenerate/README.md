# 网页数据说明

## 原始数据

url.csv文件中存储着原始的web url数据以及是否已经生成训练数据的信息

## 数据生成

1. 使用batchIMGGenerate批量处理url，获取一批网页截图数据，将生成的图片数据放入webData文件夹下，并标注处批次
2. 使用mineru_batch对生成的图片进行布局解析，解析结果也放在本批次文件夹下
3. 使用finetuneDataGenerate生成htmlcode和输入的json数据，将此数据放入finetuneData下的web中，并标注批次
4. posterDataGenerate中有dataset_create，用来生成jsonl文件，可选择单一类型数据或混合数据