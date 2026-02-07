# Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression

Adam Block，Dylan Foster\*，Akshay Krishnamurthy\*，Max Simchowitz\*，Cyril Zhang\* MIT\*Microsoft Research NYC

# Behavior cloning & feedback loops

# Gradient Variance Amplification

# Algorithmic mitigations for GVA

![](/data/huangyc/Document2All/posterDataOutput_vlm/Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression_poster/auto/images/images/fig_1.jpg)

BC: fit $\theta$ to a collection of demonstrations from expert policy $\pi ^ { \star }$ ,minimizing $\Lsh$ -step loss

$$
\ell _ { \mathrm { B C } } ( \theta ) = \underset { \mathrm { e x p e r t s } ( s _ { t } , a _ { t } ) } { \mathbb { E } } \left[ \| \pi _ { \theta } ( s _ { t } ) - \pi ^ { \star } ( s _ { t } ) \| ^ { 2 } \right]
$$

Usual view:BC reduces offline imitation learning to supervised learning

eBc（0）≤ε JH(π）≥JH(π\*）-C.ε train on 1-step loss evaluatemulti-steprollout rewards

Q1: When BC works, how big is $C$ in practice?

Q2: When BC fails, must we improve the data? Or can we improve upon standard training?

Special case: pretraining vs. generation in LLMs

$s _ { t }$ : sequence of $t$ tokens $a _ { t }$ :appenda single token $\pi _ { \theta }$ :autoregressive languagemodel

A1: Long-horizon rollouts can be extremely sensitive to small SGD fluctuations.

GVA:an empirical pathology in BC with NNs

small changes in 0 due to minibatch noise

...causing small changes in 1-step $\ell _ { \mathrm { B C } } ( \theta ) \ldots$

...and chaotic long-rollout rewards $J _ { H } ( \pi _ { \theta } )$

# Evidence: (across locomotion tasks & archs)

Instochastic gradientdirections: W small changes in $\ell _ { \mathrm { B C } }$ largechangesinWalker2Dreward

![](/data/huangyc/Document2All/posterDataOutput_vlm/Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression_poster/auto/images/images/fig_2.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression_poster/auto/images/images/fig_3.jpg)

fractal reward landscape oscillations during training (in thepaper:accompanying quantitative studies)

Theory: vignettes in toy models

-marginally stable linear dynamics,linear $\pmb { \pi }$ ， $\pi ^ { \star }$ - "CliffLQR": halfspace reward $ G V A$ - SDE limit: EMA&LR schedules both work

A2:Variance reduction techniques mitigate the oscillations;EMAishighlyeffective

![](/data/huangyc/Document2All/posterDataOutput_vlm/Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression_poster/auto/images/images/fig_4.jpg)

# Exponential Moving Average

01←0-nVBc(0）（orAdam,etc.）$\bar { \theta } _ { t + 1 }  ( 1 - \beta _ { t } ) \bar { \theta } _ { t } + \beta _ { t } \cdot \theta _ { t }$ ， use $\bar { \theta } _ { t }$ for inference

# Bonus: GVA & EMA in language generation

Every-iteratevalidation losses

![](/data/huangyc/Document2All/posterDataOutput_vlm/Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression_poster/auto/images/images/fig_5.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Butterfly Effects of SGD Noise: Error Amplification in Behavior Cloning and Autoregression_poster/auto/images/images/fig_6.jpg)  
EMA improves& stabilizes LM iterates before learningrate cooldown