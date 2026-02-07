# NeuPL: Neural Population Learning

Siqi Liu, Luke Marris,Daniel Hennes,Josh Merel, Nicolas Heess,Thore Graepel

# Background

# Methods

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_1.jpg)

The policy space of symmetric zero-sum Game-of-Skilsl iscomposed oftransitive skilldimensionsand intransitive strategic cycles[2].

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_2.jpg)

# Solving intransitive strategy games

Game-theoretic population learningalgorithms (e.g.FP, PSROl3l) offerconvergence guarantees toan NE,where eachpolicybest-respondstoa mixture over predecessors:

# Algorithm 1 Neural Population Learning (Ours)

1:II(-|s,σ） Conditional neural population net.   
2E=1 Initial interaction graph.   
3: F:RNXN →RNXN Meta-graph solver.   
4: while true do   
5: V $\Pi _ { \theta } ^ { \Sigma }  \{ \Pi _ { \theta } ( \cdot | s , \sigma _ { i } ) \} _ { i = 1 } ^ { N }$ Neural population.   
6: foroiEUNIQUE $( \Sigma )$ do   
7: $\Pi _ { \theta } ^ { \sigma _ { i } } \gets \Pi _ { \theta } ( \cdot | s , \sigma _ { i } )$   
8: $\Pi _ { \theta } ^ { \sigma _ { i } } \gets \mathbf { A B R } ( \Pi _ { \theta } ^ { \sigma _ { i } } , \sigma _ { i } , \Pi _ { \theta } ^ { \Sigma } )$ Self-play.   
9: U←EVAL(I） (Optional) if $\mathcal { F }$ adaptive.   
10: ∑←F(u） (Optional) if $\mathcal { F }$ adaptive.   
11:return Iθ,∑

Lack of positive transfer across policies; Suboptimal "good-"responses populating the policy population;

However,when combined with modern deep RL techniquesl4l，populationlearningcomesat significant costs,fortwo reasons:

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_3.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_4.jpg)

Canwe leverage the expressiveness ofmoderndeep NNs toenableasinglemodel toexplore,representand reason aboutdiverse strategieswhileretaininggame theoretic guaranteesusingthe same infrastructureas"self-play"?

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_5.jpg)

# Experiments (RwS)

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_6.jpg)

# Forward Transfer

Transfer from NeuPLagent atdifferent epochs to MPO agents Against Nash with n=2 Against Nash with n=7 25 fromepoch Ot 50 20 200 params.epoch Encoder …initalize·. Encoder 15 ↓ 1,000 Memory .….initialize... Memory 5 10 0 S-1 Policy S S1 Policy S -5 0 9 0k gdietstepoo -100 dientstep40

# Improved Population Learning

![](/data/huangyc/Document2All/posterDataOutput_vlm/NeuPL: Neural Population Learning_poster/auto/images/images/fig_7.jpg)

# References

[1] Czarnecki,Wojciech $\mathsf { M } _ { \cdot } ,$ et al."Real WorldGames Look Like SpinningTops."Advances inNeural Information Processing Systems 33(2020). 2]Balduividtddgtricetioereeca1 tott [4]VinyalsOrlteiftglgtefoettue7O)54