Zhiwei Hao\*1, Jianyuan Guo\*2, Chengcheng Wang\*3 Yehui Tang³, Han $\mathsf { W } \mathsf { u } ^ { 2 }$ ，Han ${ \mathsf { H } } { \mathsf { u } } ^ { 1 }$ ,Kai Han³, Chang ${ \tt X } { \tt U } ^ { 2 }$

\*Equal contribution 1School of information and Electronics, Beijing Institute of Technology. 2School of Computer Science, Faculty of Engineering, The University of Sydney. 3Huawei Noah's Ark Lab.

THEUNIVERSITYOF SYDNEY

# Introduction

Training general-purpose large multimodal foundation modelsonpurely sequential data,similar to linguistic inputs,has heralded anew frontier in visual perception. However,current endeavors are hamstrung by an over-reliance on colossal models，exemplified by the necesity foran extensive corpus of data，often comprising staggering 400B tokens.Inthis work,we delve intothe developmentofaneficient,autoregressionbased foundationmodel,innovativelyarchitected tooperateonalimiteddataset.Ourevaluationsdemonstrate how this model achieves proficiency in a spectrum of visual tasks spanning both high-level and low-level semanticunderstanding.With a significant reduction in parameter footprint,andamarked decrease in training data requirements，we pave the way for more sustainable and accessible advancements in the field of generalist visual models.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_1.jpg)  
Part-1: Data-efficient Training: Data Augmentation Strategy

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_2.jpg)  
Single task

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_3.jpg)  
Multiple tasks.“-"indicatescollapsed results.

# Part-2: Low Power Consumption & Tiny Model: Knowledge Distillation

The introduction of KD proves beneficial in enhancing the single-task performance of LVMs.

<table><tr><td>Model</td><td>KD</td><td>loss↓</td><td>accuracy↑</td><td>perplexity↓</td></tr><tr><td colspan="5">Image Segmentation (10% of SA-1B)</td></tr><tr><td>LLaMA-1B</td><td>-</td><td>4.50</td><td>20.18</td><td>90.04</td></tr><tr><td>LLaMA-300M</td><td>X</td><td>4.64</td><td>19.17</td><td>103.24</td></tr><tr><td>LLaMA-300M</td><td>√</td><td>4.59</td><td>19.48</td><td>98.72</td></tr><tr><td colspan="5">Pose Estimation( (COCO-Pose)</td></tr><tr><td>LLaMA-1B</td><td>-</td><td>4.90</td><td>20.96</td><td>134.07</td></tr><tr><td>LLaMA-300M</td><td>X</td><td>4.97</td><td>20.46</td><td>144.08</td></tr><tr><td>LLaMA-300M</td><td>√</td><td>4.91</td><td>20.80</td><td>135.91</td></tr></table>

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_4.jpg)

The introduction of KD proves beneficial in enhancing the multi-task performance of LVMs.

<table><tr><td rowspan="2">Model</td><td rowspan="2">KD</td><td colspan="3">Image Segmentation</td><td rowspan="2">loss</td><td colspan="2">Pose Estimation</td><td rowspan="2">loss↓</td><td colspan="2">Image Deraining</td></tr><tr><td>loss</td><td>accuracy↑</td><td>perplexity</td><td>accuracy↑</td><td>perplexity</td><td>accuracy↑</td><td>perplexity↓</td></tr><tr><td>LLaMA-1B</td><td>-</td><td>4.55</td><td>19.72</td><td>94.75</td><td>4.86</td><td>20.77</td><td>129.95</td><td>5.53</td><td>12.20</td><td>245.33</td></tr><tr><td>LLaMA-300M</td><td>X</td><td>4.68</td><td>18.79</td><td>107.76</td><td>4.94</td><td>20.24</td><td>140.39</td><td>5.63</td><td>11.57</td><td>271.38</td></tr><tr><td>LLaMA-300M</td><td>/</td><td>4.67</td><td>18.84</td><td>106.81</td><td>4.93</td><td>20.32</td><td>139.27</td><td>5.62</td><td>11.93</td><td>269.04</td></tr></table>

# LLaMA-300Mw/o KD vs.w/KD on LSP dataset.

LLaMA-300M w/o KD vs.w/KD on OCHuman dataset.

NNN

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_5.jpg)

Query Image,LLaMA-300M w/o KD,LLaMA-300Mw/KD,GroundTruthon therain100Hde-raining dataset.

# Beyond Perception: Generation Ability

Next frame prediction: zoom in, zoom out,camera motion.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_6.jpg)

Image completion.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Data-efficient Large Vision Models through Sequential Autoregression_poster/auto/images/images/fig_7.jpg)