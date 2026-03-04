# NeuPL: Neural Population Learning

Siqi Liu, Luke Marris,Daniel Hennes,Josh Merel, Nicolas Heess,Thore Graepel

# Background

![](visuals/images/fig_1.jpg)  
Transitive Skills

![](visuals/images/fig_2.jpg)  
Strategic Cycles

![](visuals/images/fig_3.jpg)  
Game-of-Skills

The policy space of symmetric zero-sum Game-of-Skillsl1l iscomposed oftransitive skilldimensionsand intransitive strategiccycles[2].

Transitive

Intransitive

![](visuals/images/fig_4.jpg)

![](visuals/images/fig_5.jpg)

![](visuals/images/fig_6.jpg)

![](visuals/images/fig_7.jpg)

# Solving intransitive strategy games

Game-theoretic population learningalgorithms (e.g.FP, PSRO[3l)offerconvergence guaranteestoan NE,where each policy best-responds toamixture over predecessors:

![](visuals/images/fig_8.jpg)  
Fictitious Play

![](visuals/images/fig_9.jpg)  
PSRO-NASH

However,whencombined withmoderndeep RL techniquesl4，population learningcomesatsignificant costs,fortworeasons:

Lack ofpositive transferacrosspolicies;   
Suboptimal "good-"responsespopulating thepolicy population;

![](visuals/images/fig_10.jpg)

![](visuals/images/fig_11.jpg)

Canwe leverage the expressiveness of moderndeep NNs toenableasinglemodel toexplore,representand reason aboutdiverse strategieswhile retaining game theoretic guaranteesusingthesame infrastructureas"self-play"?

# Methods

# Algorithm 1 Neural Population Learning (Ours)

1: IIe(-|s,σ) Conditional neural population net.   
Initial interaction graph.   
3:F:RNXN-→RNXN Meta-graph solver.   
4:while true do   
$\Pi _ { \theta } ^ { \Sigma }  \{ \Pi _ { \theta } ( \cdot | s , \sigma _ { i } ) \} _ { i = 1 } ^ { N }$ Neural population.   
6: forgiEUNIQUE(∑）do   
7: $\Pi _ { \theta } ^ { \sigma _ { i } } \gets \Pi _ { \theta } ( \cdot | s , \sigma _ { i } )$   
8: $\Pi _ { \theta } ^ { \sigma _ { i } } \gets \mathbf { A B R } ( \Pi _ { \theta } ^ { \sigma _ { i } } , \sigma _ { i } , \Pi _ { \theta } ^ { \Sigma } )$ Self-play.   
9:U←EVAL(I） (Optional) if $\mathcal { F }$ adaptive.   
10:←F（u） (Optional)ifFadaptive.   
11:return Iθ,∑

![](visuals/images/fig_12.jpg)

![](visuals/images/fig_13.jpg)

![](visuals/images/fig_14.jpg)

# Experiments (RwS)

![](visuals/images/fig_15.jpg)

![](visuals/images/fig_16.jpg)

![](visuals/images/fig_17.jpg)

![](visuals/images/fig_18.jpg)

![](visuals/images/fig_19.jpg)

![](visuals/images/fig_20.jpg)

![](visuals/images/fig_21.jpg)

![](visuals/images/fig_22.jpg)

![](visuals/images/fig_23.jpg)

![](visuals/images/fig_24.jpg)

![](visuals/images/fig_25.jpg)

![](visuals/images/fig_26.jpg)

![](visuals/images/fig_27.jpg)

![](visuals/images/fig_28.jpg)

![](visuals/images/fig_29.jpg)

![](visuals/images/fig_30.jpg)

![](visuals/images/fig_31.jpg)

# Forward Transfer

![](visuals/images/fig_32.jpg)

![](visuals/images/fig_33.jpg)

![](visuals/images/fig_34.jpg)

# Improved Population Learning

![](visuals/images/fig_35.jpg)

# References

[1]CzarneckiechaRaldmeLieSpngps"danesinuraformatiroesingStes   
[2]Baldzividtddngerimteatieren1   
tot   
[4]VinyalsOriltsteiaaftgntrmtgtur)4