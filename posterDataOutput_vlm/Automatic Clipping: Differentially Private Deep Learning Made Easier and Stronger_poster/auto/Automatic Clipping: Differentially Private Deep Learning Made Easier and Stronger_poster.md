# AUTOMATICCLIPPING:DIFFERENTIALLYPRIVATE DEEP LEARNINGMADEEASIERANDSTRONGER

Zhiqi Bu, Yu-Xiang Wang,Sheng Zha,George Karypis

zhiqibu@amazon.com;yuxiangw@cs.ucsb.edu;zhasheng@amazon.com; gkarypis@amazon.com

# ABSTRACT

# CONTRIBUTIONS

# CONVERGENCE ANALYSIS OF AUTOMATIC DP-SGD

Per-example gradient clipping is a key algorithmic step that enables practical differential private (DP) training for deep learning models.The choice of clipping threshold $R$ is shown to be vital for achieving high accuracy under DPbut difficult to tune (must be tuned jointly with learning rate).

![](/data/huangyc/Document2All/posterDataOutput_vlm/Automatic Clipping: Differentially Private Deep Learning Made Easier and Stronger_poster/auto/images/images/fig_1.jpg)  
Figure1: Ablationstudyoflipping thresholdandTearingrate thatachievesSOTA results.Left:GPT2 on E2E dataset usingDP-AdamW.Right:ResNet18 on ImageNet dataset using DP-SGD with momentum.

We propose an easy-to-use replacement, called Automatic Clipping,that eliminates the need to tune $R$ forany DPoptimizers,whilebeingas private and computationally efficient as existing DP optimizers.

# DIFFERENTIAL PRIVACY IN DEEP LEARNING

ferentialprivacy(DP;Dworketal.)isaformaldefinitionofprivacythathasbeenshowntopreventheprivacyrisksindeeplear

Definition1. Arandomized algorithm $M$ is $( \varepsilon , \delta )$ DPifforany neighboringdatasets $S , S ^ { \prime }$ thatdiffer byonesample,andforanyeoent $E$ ：

$$
\mathbb { P } [ M ( S ) \in E ] \leqslant \mathrm { e } ^ { \varepsilon } \mathbb { P } \left[ M \left( S ^ { \prime } \right) \in E \right] + \delta .
$$

ThekeydiferecebeeeteDplagdtlaroiseterteadtisprvatelyeleasdIerodleadd optimizers update on the summed gradient $\textstyle \sum _ { i } { g _ { i } }$ ,and DP optimizers update on the prioate gradient:

·We propose a new per-sample gradient clipping function does not require the clipping threshold $R ,$ making hyperparameter tuning of DP deep learningas easy as the regular non-private one. ·We give a convergence analysis of automatic DP-SGD in the nonconvex setting,which shows that it enjoysan asymptotic convergence rate $O ( T ^ { - 1 / 4 } )$ that matches the standard non-private SGD. ·We demonstrate onextensivelanguage (SST-2,QNLI,MNLI,QQP, E2E)and visiontasks (MNT,FashionMNT,IFAR10,ImageNet, CelebA) that automatic clipping outperforms or matches the state-ofthe-art accuracy. · We demonstrate minimal changes to adopt our automatic clipping in existingcodebases,e.g.Opacus,ObJAX,PrivateTransformers,etc.

$$
\begin{array} { l } { { \mathrm { ~ { \small D P ~ O p t i m i z e r } } ( \{ g _ { i } \} _ { i = 1 } ^ { B } ) = \mathrm { { \small O p t i m i z e r } } ( \overbrace { \sum _ { i } g _ { i } \cdot \mathrm { { \small C l ~ i p } } ( \| g _ { i } \| ; R ) + \sigma R \cdot \mathcal { N } ( 0 , I ) } ^ { = \mathrm { { \small C l ~ C l ~ i p } } ( \| g _ { i } \| ; R ) } ) } ^ { = \mathrm { { \small C p t i m i z e r } } ( \{ g _ { i } \} _ { i = 1 } ^ { B } ) = \mathrm { { \small C o p t i m i z e r } } ( \overbrace { \sum _ { i } g _ { i } ) } ^ { = \mathrm { { \small C l o } } _ { i } ^ { B } . } } } \end{array}
$$

Here $\pmb { g } _ { i } \in \mathbb { R } ^ { d }$ is the per-sample gradient of loss $l _ { i } , { \mathcal { N } }$ is the standard normal random variable, $\sigma$ is the noise multiplier,and $R$ is the clipping threshold. The clipping function $\mathbb { C } \textrm { l i p } : \mathbb { R } ^ { d }  \mathbb { R }$ is defined such that $\| \pmb { g } _ { i } \cdot \mathbb { C } \mathrm { 1 i p } ( \pmb { g } _ { i } ; \pmb { R } ) \| \le R$

WeanalyzetheoergeeoonelssitaddssutiosinGDlieaurendssuingtsetryfpeslediet.

Assumption 3(Lower bound of loss).Forall w and some constant $\mathcal { L } _ { * } ,$ wehave $\mathcal { L } ( w ) \geq \mathcal { L } _ { * }$

Assumption 4 (Smoothness).Let $g ( w )$ denotethegradientof theobjective $\mathcal { L } ( w )$ Then $\forall w , v ,$ there isan non-negative constant $L$ such that $\mathcal { L } ( v )$ 1 $\begin{array} { r } { \left[ \mathscr { L } ( \pmb { w } ) + g ( \pmb { w } ) ^ { \top } ( \pmb { v } - \pmb { w } ) \right] \leq \frac { L } { 2 } \| \pmb { w } - \pmb { v } \| ^ { 2 } } \end{array}$

Assumption 5(Gradient noise).The per-sample gradient noise $\hat { g } _ { t , i } - g _ { t }$ is i.i.d.fromsomeditributionsuch that $\mathbb { E } ( \tilde { { \bf g } } _ { t , i } - { \bf g } _ { t } ) = 0 , \mathbb { E } \| \tilde { { \bf g } } _ { t , i } - { \bf g } _ { t } \| ^ { 2 } \leq \xi ^ { 2 }$ ,and $\tilde { g } _ { t , i }$ is centrally symmetric about $\scriptstyle g _ { t }$ indistribution: $\tilde { { \mathbf g } } _ { t , i } - { \mathbf g } _ { t } \overset { \mathcal { D } } { = } { \mathbf g } _ { t } - \tilde { { \mathbf g } } _ { t , i }$

Theorem 3. Under Assumption 3- 5,running automatic DP-SGD for $T$ iterations with learning rate $\eta \propto 1 / \sqrt { T }$ give

$$
\operatorname* { m i n } _ { 0 \le t \le T } \mathbb { E } ( \| g _ { t } \| ) \le \mathcal { G } \left( \frac { 4 } { \sqrt { T } } \sqrt { ( \mathcal { L } _ { 0 } - \mathcal { L } _ { * } ) L \left( 1 + \frac { \sigma ^ { 2 } d } { B ^ { 2 } } \right) } ; \xi , \gamma \right) : = \operatorname* { m i n } _ { r > 0 } \frac { \xi } { r } + \mathcal { F } \left( \cdots ; r , \xi , \gamma \right) .
$$

Here...is theargumentofG,whichisincreasingand positie.As $T \to \infty$ ,we get mint $\mathbb { E } ( \| g _ { t } \| ) = O ( T ^ { - 1 / 4 } ) \boldsymbol { j }$ forAuTO-S,thesamerateasstandardSGL

Wefurther take the privacy into consideration to understand how hyperparameters affect theconvergence.

Theorem 4. Under Assumption 3-5andfixed prioacy budget $\mu ( \epsilon , \delta )$ ,running automatic DP-SGD for $T$ iterations with learning rate $\eta \propto 1 / \sqrt { T }$ gioe

$$
\operatorname* { m i n } _ { 0 \leq t \leq T } \mathbb { E } ( \| g _ { t } \| ) \leq \mathcal { G } \left( 4 \sqrt { ( \mathcal { L } _ { 0 } - \mathcal { L } _ { * } ) L \left( \frac { 1 } { T } + \frac { d } { \mu ^ { 2 } n ^ { 2 } } + O \big ( \frac { 1 } { B ^ { 2 } T } \big ) \right) } ; \xi , \gamma \right)
$$

LeveragingTeorem4uraalysisprovidesgudelistoDPrngthatatchtheempiicalobervatio:weinimizethfirstgntof $\mathcal { G }$ in (0.5) denoted as $X ( B , T , \mu , d , L , \mathcal { L } _ { 0 } )$ .

1. [Train longer with larger noiseFixing the expected batch size $B$ $X$ is decreasing in $T$ . Hence larger $T$ and consequently larger $\sigma$ are preferred.

2.[Larger batch size helps] Fixing number of iterations $T$ or epochs, $X$ is decreasing in $B$ .Hence larger $B$ and consequently larger $\sigma$ are preferred.

[Pretraining is criticall Pretraining can leads toa much smallerinitial loss $\mathcal { L } _ { 0 }$ and from asmooth (small $L$ )and flat (smallε) initialization.

4.LearigatedsngOsodseggteoalodelaervcygerallhze.

# AUTOMATIC CLIPPING IS EASY TO CODE

# PER-SAMPLE GRADIENT CLIPPING

Abadi'sclipping is the most widely applied clipping function,which requiresa hyperparameter-theclipping threshold $R$

$$
\mathrm { C l } \ i \mathrm { p _ { A b a d i } } ( { \pmb g } _ { i } ; R ) = \operatorname* { m i n } \left( R / | | { \pmb g } _ { i } | | , 1 \right)
$$

Recent advances have observed small clipping threshold works best,which motivates our automatic clipping:

$$
\begin{array} { r } { \mathbb { C } \mathbb { 1 } \dot { \mathbb { 2 } } \mathbb { P } _ { \mathrm { A U T O - V } } ( \pmb { g } _ { i } ; \boldsymbol { R } ) : = \boldsymbol { R } / | | \pmb { g } _ { i } | | . } \end{array}
$$

We notice that AUTO-Vloses the magnitude information of per-sample gradients.Weadditionally proposeAUTO-Swithapositivestability constant $\gamma$ that is set to 0.01 across tasks.

$$
\mathrm { C 1 } \mathrm { i p _ { A U T O - S } } ( g _ { i } ; R ) : = R / ( | | g _ { i } | | + \gamma ) .
$$

We show that using automatic clipping, it suffices to tune learning rate and weight decay in DP training as in the regular training.

# R-INDEPENDENCE OF AUTOMATIC CLIPPING

Theorem 1. Non-adaptioe $R$ -dependent automatic DP-SGD (possibly usingmomentum) with learning rate $\eta$ and weight decay $\lambda ,$ isequivalent to R-independentautomaticDPoptimizers,with learningrate $\eta ^ { \prime } = \eta R$ and weight decay $\lambda ^ { \prime } = \lambda / R$

Finally,we can always set $R \ : = \ : 1$ whichleadsto theactual automatic clipping,which is $R \cdot$ -independent.

Theorem 2. Adaptioe R-dependent automatic DPoptimizers (including AdaGradAdaDelta，AdaMax/Adam，Ndam，dam，AR,), with learning rate $\eta$ and weight decay $\lambda$ is equivalent to $R$ -independent automatic $D P$ optimizers with learning rate n and weight decay $\lambda ^ { \prime } = \lambda / R$

$$
\mathrm { C 1 } \overset { . } { \operatorname { i p } } _ { \mathrm { A U T O } - S } ( \pmb { g } _ { i } ) : = 1 / ( | | \pmb { g } _ { i } | | + \gamma ) .
$$

Swichngodel inhttps://github.com/pytorch/opacus/blob/main/opacus/optimizers/optimizer.py to

Notice that all clipping functions have the same noise-to-sensitivity ratio,hence they have the same DP guarantee.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Automatic Clipping: Differentially Private Deep Learning Made Easier and Stronger_poster/auto/images/images/fig_2.jpg)  
Figure2:Gradient norms before and afterdifferent clippingat $R = 1$

per_sample_clip_factor= self.max_grad_norm /(per_sample_norms +0.01)

# EMPIRICAL RESULTS

Autoaticefbli otibly

Remark2.Withdecoupledweightdecay,R-dependentautomaticDP-AdamWis equioalent to $R ^ { }$ -independentautomatic DP-AdamW with the samen andX.

To provethis,theidea is tocouple $R$ with learning rate:

$$
\begin{array} { r } { \boxed { R \mathrm { - } \mathrm { d e p } \mathrm { D P \mathrm { - } S G D _ { A U T O \mathrm { - } S } } : \quad w _ { t + 1 } = w _ { t } - \eta \Big ( \displaystyle \sum _ { i \in B _ { t } } g _ { i } \cdot \frac { R } { \| g _ { i } \| + 0 . 0 1 } + \sigma R \cdot \mathcal { N } ( 0 , I ) \Big ) } } \\ { R \mathrm { - } \mathrm { i n d e p } \mathrm { D P \mathrm { - } S G D _ { A U T O \mathrm { - } S } } : \quad w _ { t + 1 } = w _ { t } - \eta ^ { \prime } \Big ( \displaystyle \sum _ { i \in B _ { t } } \frac { g _ { i } } { \| g _ { i } \| + 0 . 0 1 } + \sigma \cdot \mathcal { N } ( 0 , I ) \Big ) } \end{array}
$$

<table><tr><td rowspan=2 colspan=1>Task</td><td rowspan=2 colspan=1>Model</td><td rowspan=2 colspan=1>（c,8）</td><td rowspan=1 colspan=3>Accuracy%</td></tr><tr><td rowspan=1 colspan=1>Abadi&#x27;sclipping</td><td rowspan=1 colspan=1>AUTO-S clipping</td><td rowspan=1 colspan=1>non-DP（=∞）</td></tr><tr><td rowspan=1 colspan=1>MNIST</td><td rowspan=1 colspan=1>4-layerCNN</td><td rowspan=1 colspan=1>（3,1e-5）)</td><td rowspan=1 colspan=1>98.04±0.09</td><td rowspan=1 colspan=1>98.15±0.07</td><td rowspan=1 colspan=1>99.11±0.07</td></tr><tr><td rowspan=1 colspan=1>FashionMNIST</td><td rowspan=1 colspan=1>4-layerCNN</td><td rowspan=1 colspan=1>(3,1e-5)</td><td rowspan=1 colspan=1>86.04±0.26</td><td rowspan=1 colspan=1>86.36±0.18</td><td rowspan=1 colspan=1>89.57±0.13</td></tr><tr><td rowspan=1 colspan=1>CIFAR10 pretrained</td><td rowspan=1 colspan=1>SimCLRv2</td><td rowspan=1 colspan=1>(2,1e-5)</td><td rowspan=1 colspan=1>92.44±0.13</td><td rowspan=1 colspan=1>92.70±0.02</td><td rowspan=1 colspan=1>94.42±0.01</td></tr><tr><td rowspan=1 colspan=1>ImageNette</td><td rowspan=1 colspan=1>ResNet9</td><td rowspan=1 colspan=1>(8,1e-4</td><td rowspan=1 colspan=1>60.29±0.53</td><td rowspan=1 colspan=1>60.71±0.48</td><td rowspan=1 colspan=1>71.11 ± 0.37</td></tr><tr><td rowspan=1 colspan=1>CelebA [Smiling]</td><td rowspan=1 colspan=1>ResNet9</td><td rowspan=1 colspan=1>(8,5e-6)</td><td rowspan=1 colspan=1>90.75±0.11</td><td rowspan=1 colspan=1>91.08±0.08</td><td rowspan=1 colspan=1>92.61±0.20</td></tr><tr><td rowspan=1 colspan=1>CelebA[Male]</td><td rowspan=1 colspan=1>ResNet9</td><td rowspan=1 colspan=1>(8,5e-6)</td><td rowspan=1 colspan=1>95.54±0.14</td><td rowspan=1 colspan=1>95.70±0.07</td><td rowspan=1 colspan=1>97.90±0.04</td></tr><tr><td rowspan=1 colspan=1>CelebAMulti-label</td><td rowspan=1 colspan=1>ResNet9</td><td rowspan=1 colspan=1>（3,5e-6)</td><td rowspan=1 colspan=1>86.81±0.03</td><td rowspan=1 colspan=1>87.05±0.01</td><td rowspan=1 colspan=1>90.30±0.02</td></tr><tr><td rowspan=1 colspan=1>CelebAMulti-label</td><td rowspan=1 colspan=1>ResNet9</td><td rowspan=1 colspan=1>(8,5e-6)</td><td rowspan=1 colspan=1>87.52±0.15</td><td rowspan=1 colspan=1>87.58±0.04</td><td rowspan=1 colspan=1>90.30±0.02</td></tr></table>

Table 1: Average test accuracy and $9 5 \%$ confidence interval over 5 runs   

<table><tr><td rowspan="2">Method</td><td colspan="4">e=3</td><td colspan="3">e=8</td><td colspan="3">∈=8(non-DP)</td></tr><tr><td>MNLI</td><td>QQPQNLI SST2</td><td></td><td>MNLI</td><td>QQP</td><td>QNLI SST2</td><td></td><td>MNLI</td><td>QQPQNLI SST2</td><td></td></tr><tr><td>RGP</td><td>-</td><td>-</td><td>- -</td><td>86.1/86.0</td><td>86.7</td><td>90.0 93.0</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>full Abadi</td><td>86.43/86.46 86.43 90.76 93.04</td><td></td><td></td><td>87.02/87.26 87.47</td><td></td><td>91.10 93.81</td><td></td><td></td><td></td><td></td></tr><tr><td>full AUTO-V</td><td>85.33/85.61 86.61 89.99 93.12</td><td></td><td></td><td></td><td>85.91/86.10 86.86 90.55 93.35</td><td></td><td></td><td>90.33/90.03 87.90 93.61 96.21</td><td></td><td></td></tr><tr><td>full AUTO-S</td><td>86.27/86.67 86.76 91.01 93.92</td><td></td><td></td><td></td><td>87.07/87.16 87.47 91.4594.61</td><td></td><td></td><td></td><td></td><td></td></tr></table>

Table 2: Test accuracy on language tasks with RoBERTa-large (407M parameters).

<table><tr><td rowspan="2">Metric</td><td rowspan="2">DP guarantee</td><td>GPT2 large</td><td>GPT2 medium</td><td colspan="8">GPT2</td></tr><tr><td>full AUTO-S</td><td>full AUTO-S</td><td>full AUTO-SAUTO-VAbadi</td><td>full</td><td>fullLoRA RGP prefix top2 retrain</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">BLEU</td><td>=3</td><td>64.180</td><td>63.850</td><td>61.340</td><td>61.519</td><td></td><td>61.519 58.15358.48247.77225.92015.457</td><td></td><td></td><td></td><td></td></tr><tr><td>e=8 non-DP</td><td>64.640</td><td>64.220</td><td>63.600</td><td>63.189</td><td></td><td>63.189 63.389 58.45549.26326.88524.247</td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2"></td><td></td><td>66.840</td><td>68.500</td><td>69.463</td><td>69.463</td><td></td><td>69.463 69.682 68.328 68.845 65.752 65.731</td><td></td><td></td><td></td><td></td></tr><tr><td>E=3</td><td>67.857</td><td>67.071</td><td>65.872</td><td>65.670</td><td></td><td>65.670 65.77365.560 58.96444.53635.240</td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">ROGUE-L</td><td>∈=8</td><td>68.968</td><td>67.533</td><td>67.073</td><td>66.429</td><td></td><td>66.429 67.525 65.030 60.73046.421 39.951</td><td></td><td></td><td></td><td></td></tr><tr><td>non-DP</td><td>70.384</td><td>71.458</td><td>71.359</td><td>71.359</td><td></td><td>71.35971.709 68.84470.80568.704 68.751</td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">NIST</td><td>e=3</td><td>7.937</td><td>7.106</td><td>7.071</td><td>6.697</td><td>6.697</td><td>5.463</td><td>5.775</td><td>5.249</td><td>1.510</td><td>0.376</td></tr><tr><td>e=8 non-DP</td><td>8.301</td><td>8.172 8.628</td><td>7.714 8.780</td><td>7.444</td><td>7.444</td><td>7.449</td><td>6.276</td><td>5.525</td><td>1.547</td><td>1.01</td></tr><tr><td rowspan="2">METEOR</td><td></td><td>8.730</td><td></td><td></td><td>8.780</td><td>8.780</td><td>8.822</td><td>8.722</td><td>8.722</td><td>8.418</td><td>8.286</td></tr><tr><td>∈=3 E=8</td><td>0.403 0.420</td><td>0.387 0.418</td><td>0.387 0.404</td><td>0.384</td><td>0.384 0.400</td><td>0.370 0.407</td><td>0.331 0.349</td><td>0.363</td><td>0.197</td><td>0.113 0.145</td></tr><tr><td rowspan="2"></td><td>non-DP</td><td>0.460</td><td>0.449</td><td>0.461</td><td>0.400 0.461</td><td>0.461</td><td>0.463</td><td>0.456</td><td>0.364 0.445</td><td>0.207 0.443</td><td>0.429</td></tr><tr><td>∈=3</td><td>2.008</td><td>1.754</td><td>1.801</td><td></td><td>1.761</td><td>1.581</td><td>1.300</td><td></td><td></td><td></td></tr><tr><td rowspan="2">CIDEr</td><td>(=8</td><td>2.163</td><td>2.081</td><td>1.938</td><td>1.761 1.919</td><td>1.919</td><td>1.948</td><td>1.496</td><td>1.507 1.569</td><td>0.452 0.499</td><td>0.116 0.281</td></tr><tr><td>non-DP</td><td>2.356</td><td>2.137</td><td>2.422</td><td>2.422</td><td>2.422</td><td>2.491</td><td>2.418</td><td>2.345</td><td>2.180</td><td>2.004</td></tr></table>

Table3:Test performance on E2E dataset with GPT2.