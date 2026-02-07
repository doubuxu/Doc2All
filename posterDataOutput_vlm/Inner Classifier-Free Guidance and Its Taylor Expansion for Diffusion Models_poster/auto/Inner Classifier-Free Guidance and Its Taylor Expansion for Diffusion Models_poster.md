# Inner Classifier-Free Guidance and Its Taylor Expansion for Diffusion Models

Shikun Sun1,Longhui Wei, Zhicai Wang, Zixuan Wang,Junliang Xing, Jia Jia, Qi Tian 1Department of Computer Science and Technology， Tsinghua University， Beijing 10o084， China Email: 1ssk52839916@gmail.com

# Abstract

Classifier-free guidance (CFG) isa pivotal technique for balancing the diversity and fidelity of samples in conditional diffusion models. This approach involves utilizing asingle model to jointly optimize the conditional score predictor and unconditional score predictor,eliminating the need for additional classifiers.It delivers impressive resultsand can be employed for continuous and discrete condition representations. However，when the condition is continuous,it prompts the question of whether the trade-off can be further enhanced. Our proposed inner classifier-free guidance (ICFG) provides an alternative perspective on the CFG method when the condition has a specific structure, demonstrating that CFG represents a first-order case of ICFG.Additionally,we offera second-order implementation,highlighting that even without altering the training policy,our second-order approach can introduce new valuable information and achieve an improved balance between fidelity and diversity for Stable Diffusion.

# Contributations

·We introduce ICFG and analyze the convergence of its Taylor expansion under specific conditions.

·We demonstrate that CFG can be regarded as a first-order ICFG and propose a second-order Taylor expansion for our ICFG.

·We apply the second-order ICFG to the Stable Diffusion model and observe that, remarkably,our new formulation yields valuable information and enhances the trade-off between fdelity and diversity, even without modifying the training policy.

# Preliminary

We assume that this diffusion process follows a SDE:

$$
\mathrm { d } \mathbf { x } = \mathbf { f } ( \mathbf { x } , t ) \mathrm { d } t + g ( t ) \mathrm { d } \mathbf { w } .
$$

The score function is defined as follows:

$$
\mathbf { s } ( \mathbf { x } , t ) = \nabla _ { \mathbf { x } _ { t } } \log q ( \mathbf { x } _ { t } ) .
$$

Then, the reverse-time SDE is:

$$
\mathrm { d } \mathbf { x } = [ \mathbf { f } ( \mathbf { x } , t ) - g ( t ) ^ { 2 } \mathbf { s } ( \mathbf { x } , t ) ] \mathrm { d } t + g ( t ) \mathrm { d } \overline { { \mathbf { w } } } .
$$

For the unconditional diffusion score $\epsilon ^ { \theta } ( \mathbf { x } , t )$ ,using the same set of classifiers, the modified diffusion score is given by:

$$
\begin{array} { r l } & { \widetilde { \epsilon } ^ { \theta } ( \mathbf { x } _ { t } , \mathbf { c } , t ) = \epsilon ^ { \theta } ( \mathbf { x } _ { t } , t ) - ( w + 1 ) \beta _ { t } \nabla _ { \mathbf { x } _ { t } } \log p _ { t } ^ { \theta } ( \mathbf { c } | \mathbf { x } _ { t } ) } \\ & { \quad \quad \quad = - \beta _ { t } \nabla _ { \mathbf { x } _ { t } } \left[ \log q ^ { \theta } ( \mathbf { x } _ { t } ) + ( w + 1 ) \log p _ { t } ^ { \theta } ( \mathbf { c } | \mathbf { x } _ { t } ) \right] . } \end{array}
$$

The main idea behind CFG is to use a single model to simultaneously fit both the conditional score predictor and the unconditional score predictor.This is achieved by randomly replacing the condition $\mathbf { c }$ with $\boldsymbol { \mathcal { Q } }$ (an empty value).By doing so, one can

obtain the conditional score predictor $\boldsymbol { \epsilon } ^ { \theta } ( \mathbf { x } , \mathbf { c } , t )$ and the unconditional score predictor $\epsilon ^ { \theta } ( \mathbf { x } , t )$ ,which is equivalent to $\epsilon ^ { \theta } ( \mathbf { x } , \theta , t )$ .Then,because

$$
\begin{array} { r l } & { \nabla _ { \mathbf { x } _ { t } } \left[ \log p _ { t } ( \mathbf { c } | \mathbf { x } _ { t } ) \right] = \nabla _ { \mathbf { x } _ { t } } \left[ \log q ( \mathbf { x } _ { t } | \mathbf { c } ) - \log q ( \mathbf { x } _ { t } ) + \log p ( \mathbf { c } ) \right] } \\ & { \qquad = \nabla _ { \mathbf { x } _ { t } } \left[ \log q ( \mathbf { x } _ { t } | \mathbf { c } ) - \log q ( \mathbf { x } _ { t } ) \right] , } \end{array}
$$

which indicates that after applying the operator $\nabla _ { \mathbf { x } _ { t } }$ ,we can replace the last term of Equation (4) with $\log q ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } ) - \log q ^ { \theta } ( \mathbf { x } _ { t } )$ to achieve a similar effect. Then we get the enhanced diffusion score:

$$
\begin{array} { r l } & { \hat { \epsilon } ^ { \theta } ( \mathbf { x } _ { t } , \mathbf { c } , t ) = ( w + 1 ) \epsilon ^ { \theta } ( \mathbf { x } _ { t } , \mathbf { c } , t ) - w \epsilon ^ { \theta } ( \mathbf { x } _ { t } , t ) } \\ & { \hphantom { \epsilon ^ { \theta } ( \mathbf { x } _ { t } , \mathbf { c } , t ) = } = - \beta _ { t } \nabla _ { \mathbf { x } _ { t } } \left[ \log { q ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } ) } + w ( \log { q ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } ) } - \log { q ^ { \theta } ( \mathbf { x } _ { t } ) } ) \right] } \\ & { \hphantom { \epsilon ^ { \theta } ( \mathbf { x } _ { t } , \mathbf { c } , t ) = } = - \beta _ { t } \nabla _ { \mathbf { x } _ { t } } \left[ \log { q ^ { \theta } ( \mathbf { x } _ { t } ) } + ( w + 1 ) ( \log { q ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } ) } - \log { q ^ { \theta } ( \mathbf { x } _ { t } ) } ) \right] , } \end{array}
$$

whose enhanced intermediate distribution is:

$$
\overline { { { q } } } ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } ) \propto q ^ { \theta } ( \mathbf { x } _ { t } ) \left[ \frac { q ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } ) } { q ^ { \theta } ( \mathbf { x } _ { t } ) } \right] ^ { w + 1 } .
$$

# Methodology

Theorem O.1.Given condition c, the enhanced transition kernel $\overline { { q } } _ { 0 t } ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } , \mathbf { c } )$ by Eq.(7) equals to the original transition kernel $q _ { 0 t } ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } , \mathbf { c } ) = q _ { 0 t } ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } )$ does not hold trivially.Specifically，when $w = 0$ ，the equation holds.

The question arises: Can we always ensure that $\beta = 1 ?$

# Assumption 0.1.

$\bullet { \mathcal { C } }$ is a cone,which means $\forall \beta \in \mathbb { R } ^ { + } , \forall \mathbf { c } \in \mathcal { C } , \beta \mathbf { c } \in \mathcal { C } .$

·For each $\mathbf { c } \in \mathcal { C } , \| \mathbf { c } \|$ represents the guidance strength and $\frac { \mathbf { c } } { \| \mathbf { c } \| }$ represents the guidance direction.

Under Assumption 0.1,we define $\bar { q } ^ { \theta } ( x _ { t } | c ) = q ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { c } , \beta ) \triangleq q ^ { \theta } ( \mathbf { x } _ { t } | \beta \mathbf { c } )$ .Based on this definition,we can state the following Corollary 0.1.1:

Corollary O.1.1. Given condition c and the guidance strength $\beta = w + 1$ ,we have:

$$
q _ { 0 t } ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } , \mathbf { c } , \beta ) = q _ { 0 t } ^ { \theta } ( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } ) .
$$

The following algorithm ofers a practical solution and can be effectively applied to mitigate the aforementioned problem.

Algorithm 3 Non-strict sample algorithm for second-order ICFG   

<table><tr><td></td><td>Require: m:middle point for estimate second-order term Require:w:first-order guidance strength on conditional score predictor</td></tr></table>

# Experiment

Evaluation Metrics.We evaluate the widely-used Frechet Inception Score (FID) between the generated images and the target domain images,and CLIP Score between generated images and captions on the MS-COCO validation set. Results.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Inner Classifier-Free Guidance and Its Taylor Expansion for Diffusion Models_poster/auto/images/images/fig_1.jpg)  
Figure 2: TheFID-CLIP Score of varying w,U and $c$

hatsune_miku scenery,village, outdoors,sky,clouds

![](/data/huangyc/Document2All/posterDataOutput_vlm/Inner Classifier-Free Guidance and Its Taylor Expansion for Diffusion Models_poster/auto/images/images/fig_2.jpg)  
1boy, bishounen,caual, indoors,sitting,coffee shop,bokeh