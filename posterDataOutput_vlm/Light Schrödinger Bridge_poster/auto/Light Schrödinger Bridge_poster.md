Alexander Korotin1,2

Nikita Gushchin\*1 (\*-equal contribution)

# Motivation: Unpaired Domain Translation

# Proposed Algorithm: Light Schrodinger Bridge (LightSB)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_1.jpg)

Nopairedtrainingexamplesareavailable.

The(informal) task:givensamples $\mathsf { X } ,$ Y from two domains,construct a mapTwhich can translate new samples from the input domain to the target domain.

# Unpaired setup

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_2.jpg)

1.Optimal parameterization of the Schrodinger bridge using mixtures of Gaussians:

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_3.jpg)

Good solution (keeps the content)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_4.jpg)

Ambiguity in translations Bad solution (changes the content)

X10 T（X1）T（x2）

Single-cell (SC) sequencing extracts features for individual cells fromapopulation but destroys them.Therefore, tostudy individual cell dynamics one needsa method tomapcells between different observation times.

# 1.Formulation of the Schrodinger Bridge Problem:

For two continuous distributions $\pmb { p } _ { 0 }$ and $p _ { 1 }$ on $\mathbb { R } ^ { D }$ ，isthe Schrodingerbridge problem:

# Background: Diffusion Schrodinger Bridge (SB)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_5.jpg)

# 2. Structure of the Schrodinger Bridge.

# Examples of image unpaired domain translation

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_6.jpg)  
Example II:image style transfer

Given two probability distributions $\mathsf { p } _ { 0 } , \mathsf { p } _ { 1 } ,$ how to transform $\mathsf { p } _ { 0 }$ to $\mathsf { p } _ { 1 }$ viaadiffusion processand preserve the input-output similarity?

2.New loss function for training the Schrodinger bridge:

ExampleI:image super-resolution

Advantages:

# Single-cell data domain translation

TheSchrodinger bridge problem can be fully characterized by the initial distribution $\pmb { p } _ { 0 }$ and the Schrodingerpotential $\phi ^ { * } ( x ) : \mathbb { R } ^ { D }  \mathbb { R } _ { + }$ .The optimal drift can be expressed by the Schrodingerpotentialas

$$
\mathsf { i n f } _ { T \in \mathcal { F } ( p _ { 0 } , p _ { 1 } ) } \mathsf { K L } ( T | | W ^ { \epsilon } ) ,
$$

Our solver is based on:

# Toy examples

$$
v _ { \theta } ( x _ { 1 } ) = \sum _ { k = 1 } ^ { K } \alpha _ { k } \mathcal { N } ( x _ { 1 } | r _ { k } , \epsilon S _ { k } ) , \quad c _ { \theta } ( x _ { 0 } ) = \sum _ { k = 1 } ^ { K } \alpha _ { k } \exp \big ( \frac { { x _ { 0 } ^ { T } S _ { k } x _ { 0 } + 2 r _ { k } ^ { T } x _ { 0 } } } { 2 \epsilon } \big ) .
$$

$$
\mathsf { K L } ( T ^ { * } | | T _ { \theta } ) = \underbrace { \int _ { \mathbb { R } ^ { D } } \mathsf { l o g } c _ { \theta } ( x _ { 0 } ) p _ { 0 } ( x _ { 0 } ) d x _ { 0 } - \int _ { \mathbb { R } ^ { D } } \mathsf { l o g } v _ { \theta } ( x _ { 1 } ) p _ { 1 } ( x _ { 1 } ) d x _ { 1 } } _ { \mathcal { L } ( \theta ) } + \mathsf { C o n s t }
$$

Fast training （ $\textbf { < 1 }$ minute on 4 CPU cores, not hours of training on GPU,like others).

Qualitative results of our solverapplied to 2D model distributions("Gaussian" to "swiss-roll").

Thevolatility of trajectories increaseswithε, and the distributions $\pi ( x _ { \mathit { 1 } } | x _ { \mathit { 0 } } )$ becomemore disperse.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_7.jpg)

(d)ε = 0.1.

until converged;

Samplebatches{x,..,x}\~Ppo，{x1,..,xM}\~P1; $\theta$ $\frac { \partial \widehat { \mathcal { L } } _ { \theta } } { \partial \theta }$

(a)x\~ Po,y\~ P1. (c) ε = 0.01.

Algorithm 1: Light Schrodinger Bridge (LightSB)

# repeat

# Main problem

Theoretical validity (the guaranteesof themethod's learning ability from the point of view of statistical learningand approximation theories).

# Schrodinger Bridge Benchmark

Quantitative results of our solver on the standard benchmark for the Schrodinger bridge problem.

ε=0.1 e=1 ∈=10 D=2D=16D=64 D=128 D=2 D=16 D=64 D=128D=2D=16D=64D=128   
Best solver 1.94 13.67 11.74 11.4 1.04 9.08 18.05 15.23 1.40 1.27 2.36 1.31   
LightSB] 0.03 0.08 0.28 0.60 0.05 0.09 0.24 0.62 0.07 0.11 0.21 0.37 ±std ±0.01 ±0.04 ±0.02 ±0.02 ±0.003 ±0.006 ±0.007 ±0.007 ±0.02 ±0.01 ±0.01 ±0.01 \*Themetric cBW-UVP isused for comparising build schrodinger bridge with ground-truth bridge (lower=better).

# Single cell experiment

Quantitative results in the problem of predicting single-cell trajectories in the feature space (single-cell trajectory inference).

<table><tr><td>Setup</td><td>Solver type</td><td>DIM Solver</td><td>50</td><td>100</td><td>1000</td></tr><tr><td>DiscreteEOT</td><td>Sinkhon</td><td>(Cuturi,2013)[1GPUV100]</td><td>2.34(90 s)</td><td>2.24(2.5m)</td><td>1.864（9m)</td></tr><tr><td>Continuous EOT</td><td>Langevin-based</td><td>(Mokrov etal.,2023)[1GPUV100]</td><td>2.39±0.06（19m）</td><td>2.32±0.15（19m）</td><td>1.46±0.20（15m）</td></tr><tr><td>Continuous EOT</td><td>Minimax</td><td>(Gushchin etal.,2023)[1GPUV100]</td><td>2.44±0.13（43m）</td><td>2.24±0.13（45m）</td><td>1.32±0.06（71m）</td></tr><tr><td>Continuous EOT</td><td>IPF</td><td>(Vargasetal.,2021)[1GPUV100]</td><td>3.14±0.27（8m）</td><td>2.86±0.26（8m）</td><td>2.05±0.19（11m）</td></tr><tr><td>Continuous EOT</td><td>KLminimization</td><td>LightSB(ours)[4CPU cores]</td><td>2.31 ±0.27(65 s)</td><td>2.16±0.26(66 s)</td><td>1.27±0.19(146s)</td></tr></table>

# Unpaired Image-to-image Translation

where $\mathcal { F } ( p _ { 0 } , p _ { 1 } )$ are stochastic processes with marginals $\pmb { p } _ { 0 }$ ， $_ { p _ { 1 } }$ at $t = 0$ and $t = 1$ ,respectively，while $W ^ { \epsilon }$ isthe Wiener processwith variance∈,i.e.，given by the SDE:

This problem has a unique solution,which is a diffusion process $\tau ^ { * }$ described by the SDE:

$$
W ^ { \epsilon } : \quad d X _ { t } = { \sqrt { \epsilon } } d W _ { t } .
$$

$$
T ^ { * } : \quad d X _ { t } = g ^ { * } ( X _ { t } , t ) d t + \sqrt { \epsilon } d W _ { t } .
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_8.jpg)

The minimizer T\* is called the Schrodinger Bridge.

$$
\begin{array} { r } { \pmb { g } ^ { * } ( x , t ) = \epsilon \nabla _ { x } \log \displaystyle \int _ { \mathbb R ^ { D } } \mathcal { N } ( x ^ { \prime } | x , ( 1 - t ) \epsilon I _ { D } ) \phi ^ { * } ( x ^ { \prime } ) d x ^ { \prime } } \end{array}
$$

Inourwork，we introduce (for convenience） the adjusted Schrodinger bridge potential $\begin{array} { r } { v ^ { * } ( x _ { 1 } ) \stackrel { \mathrm { d e f } } { = } \exp ( - \frac { \| x _ { 1 } \| ^ { 2 } } { 2 \epsilon } ) \phi ^ { * } ( x _ { 1 } ) } \end{array}$

3. Integration of the Schrodinger Bridge SDE. The Schrodinger bridge SDE:

$$
T ^ { * } : \quad d X _ { t } = g ^ { * } ( X _ { t } , t ) d t + \sqrt { \epsilon } d W _ { t } .
$$

admits a closed-form solution $\pi ^ { * } ( x _ { 1 } | x _ { 0 } )$ expressed through theadjusted Schrodinger potential $v ^ { * }$ ：

$$
\pi ^ { * } ( x _ { 1 } | x _ { 0 } ) \ { \stackrel { \mathrm { d e f } } { = } } \ { \frac { \exp \left( \left. x _ { 0 } , x _ { 1 } \right. / \epsilon \right) v ^ { * } ( x _ { 1 } ) } { c ^ { * } ( x _ { 0 } ) } } ,
$$

where $\begin{array} { r } { c ^ { * } ( x _ { 0 } ) \ { \stackrel { \mathrm { d e f } } { = } } \ \int _ { \mathbb { R } ^ { D } } \exp \left( \langle x _ { 0 } , x _ { 1 } \rangle / \epsilon \right) v ^ { * } ( x _ { 1 } ) d x _ { 1 } } \end{array}$ is the normalizing constant.

Qualitative results of our solver for   
solving the domain   
translation problem   
(in the latent space of the ALAE autoencoder).

Imagesresolution is 1024×1024.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Light Schrödinger Bridge_poster/auto/images/images/fig_9.jpg)