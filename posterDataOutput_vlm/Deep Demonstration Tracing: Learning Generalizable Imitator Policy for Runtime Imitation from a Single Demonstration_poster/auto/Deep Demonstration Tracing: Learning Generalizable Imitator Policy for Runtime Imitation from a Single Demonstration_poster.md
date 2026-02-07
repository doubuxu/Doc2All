# DeepDemonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation fromaSingle Demonstration

Xiong-HuiChen\*12Junyin Ye\*12Hang Zhao\*32Yi-ChenLi1² Xu-HuiLiu1² Haoran Shi²Yu-Yan Xu² ZhihaoYe12 Si-Hang Yang12YangYu12AnqiHuang42Kai $\mathbf { X } \mathbf { u } ^ { 3 }$ Zongzhang Zhang1

# Introduction

# Methodology

# Major Experiments

# The vision of Runtime One-shot imitation Learning

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_1.jpg)  
Achieve any tasks directly “prompted”by corresponding demonstration.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_2.jpg)  
Popular paradigm: Transformer +behavior cloning

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_3.jpg)  
Our focus: Generlization Challenges of runtime OSIL

(c)Policy trained by DDT.   
Unseen demonstrations in unseenenvirnoments. ->incorrect representationcausedbytransformer.   
·Unforseen changes afterdemonstrationscollection. ->limitation of behaviorcloning.

KEY1: Inject the induective bias of "how human make decisions in runtime OSIL”into the imitator policy network.

a MLP demo-otertion CK Retape-rurent state and take the optimalaction sum 0 t towe2-Anlze:   
expert-state-action encoder point-wise behavesin these multiplication states   
[a..,..a,.   
[s...... Wo aaa- Wi Wt Stage1-ldentify: which states to   
k.kk. atention weigingg follow Inputs expert-state shared weights visited stote encoder encoder Vectors   
[s..s..s sj Layers

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_4.jpg)

An example of 3-stage OSIL of humans.

·Stage 1: Identify relevant states within the trajectory based on the current state. ·Stage 2:Analyze the expert's behavior patterns associated with these states. Stage 3:Trace the expert's demonstrations based on the relationship between the current state and the expert's behavior patterns in the demonstrations.

# KEY2: Solve runtime one-shot imitation learning by context-based meta-RL, instead of supervised learning

set simulator configuration ωi trainwithcontext-based sim.Moi meta-RLtoachieve thetask Twi reward defined inωi One-shot Tw2 sample Twi imitator I(a/s,t) demos Twn demo Twi demonstrations

·The unforeseen changeswill randomly apprear in the simulators $( \mathcal { M } )$ .   
·With meta-RL,the imitator policy willtry to achieve all ofthe targets the same to the demonstration guided by O-1 task rewards.   
·In the process,the imitator policy willsuffer from the unforseen changes and have to handlethem beforeachievethe targets.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_5.jpg)  
Q1: One-shot imitation ability in unseen situations

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_6.jpg)  
Group resultsaverged by8settings with 3 seeds (VPAMenv).

# Q2: Does DDT imitating via tracing the demos

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_7.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Deep Demonstration Tracing: Learning Generalizable Imitator Policy for Runtime Imitation from a Single Demonstration_poster/auto/images/images/fig_8.jpg)  
Q3: The“Scaling Law” of DDT in the OSIL setting