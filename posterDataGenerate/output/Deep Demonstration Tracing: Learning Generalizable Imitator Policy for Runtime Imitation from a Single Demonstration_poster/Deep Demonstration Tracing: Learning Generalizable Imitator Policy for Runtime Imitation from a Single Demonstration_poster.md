# Introduction

# The vision of Runtime One-shot imitation Learning

![](visuals/images/fig_1.jpg)

![](visuals/images/fig_2.jpg)

![](visuals/images/fig_3.jpg)

![](visuals/images/fig_4.jpg)

![](visuals/images/fig_5.jpg)

![](visuals/images/fig_6.jpg)

![](visuals/images/fig_7.jpg)

![](visuals/images/fig_8.jpg)

# Popular paradigm: Transformer +behavior cloning

![](visuals/images/fig_9.jpg)

# Our focus: Generlization Challenges of runtime OSIL

![](visuals/images/fig_10.jpg)

![](visuals/images/fig_11.jpg)  
(a)Provided demonstration.

![](visuals/images/fig_12.jpg)  
(b)Policy trained byatraditional OSIL method.   
(c)Policy trained by DDT.

·Unseen demonstrations in unseen envirnoments.   
->incorrect representation caused bytransformer.   
·Unforseen changes after demonstrationscollection.   
->limitation of behavior cloning.

![](visuals/images/fig_13.jpg)

![](visuals/images/fig_14.jpg)

![](visuals/images/fig_15.jpg)  
(A) Valet Parking Assist in Maze(VPAM)   
Trained byDDT

![](visuals/images/fig_16.jpg)  
Trained by traditional OSIL

# Methodology

KEY1: Inject the induective bias of "how human make decisions in runtime OsiL”into the imitator policy network.

![](visuals/images/fig_17.jpg)  
An example of3-stage OSIL of humans.

![](visuals/images/fig_18.jpg)

·Stage 1: Identify relevant states within the trajectory based on the current state.   
·Stage 2: Analyze the expert's behavior patterns associated with these states.   
Stage 3: Trace the expert's demonstrations based on the relationship between the current state and the expert's behavior patterns in the demonstrations.

# KEY2: Solve runtime one-shot imitation learning by context-based meta-RL,instead of supervised ling

![](visuals/images/fig_19.jpg)

·The unforeseen changes willrandomly apprear in the simulators (M).   
·With meta-RL,the imitator policy will try to achieve allofthe targets the same to the demonstration guided by O-1 task rewards.   
·In the process,the imitator policy will suffer from the unforseen changes and have to handlethembeforeachievethe targets.

# Major Experiments

# Q1: One-shot imitation ability in unseen situations

![](visuals/images/fig_20.jpg)  
Groupresultsavergedby8settings with3seeds(VPAMenv).

![](visuals/images/fig_21.jpg)

![](visuals/images/fig_22.jpg)

![](visuals/images/fig_23.jpg)

![](visuals/images/fig_24.jpg)  
buttonpre topdown

![](visuals/images/fig_25.jpg)  
button press topdown wall

![](visuals/images/fig_26.jpg)  
window open   
Table4:Performanceonunseen heterogeneousdemonstra tions.   
EnvironmentButton Press Door Close Reach   
Performance 0.78 1.00 0.75

# Q2: Does DDT imitating via tracing the demos

![](visuals/images/fig_27.jpg)  
(a)Trajectory of DDT.

![](visuals/images/fig_28.jpg)  
(b) Attention score.

![](visuals/images/fig_29.jpg)

# Q3: The “Scaling Law” of DDT in the OSIL seting

![](visuals/images/fig_30.jpg)  
scaling-uprate