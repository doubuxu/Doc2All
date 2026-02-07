# Improving Equilibrium Propagation Without Weight Symmetry Through Jacobian Homeostasis

Axel Laborieux1,Friedemann Zenke1.2 1Friedrich Miescher Institute for Biomedical Research,2Facultyof Natural Sciences,Universityof Basel

# Generalized Equilibrium Propagation [1]

Goal: Local gradients for Neurobiologyand Neuromorphics

$$
{ \frac { \mathrm { d } { \pmb u } } { \mathrm { d } t } } = F ( \pmb \theta , \pmb u , \pmb x ) \widehat { \mathrm {  ~ \xi ~ } + \beta } { \frac { \mathrm { d } { \pmb \mathcal { L } } ^ { \top } } { \mathrm { d } u } }
$$

4 COOO Wijt Wji Oo0oO OO0OO

Fixed-point (prediction): $0 = F ( \pmb \theta , \pmb u _ { 0 } ^ { * } , \pmb x )$

EP error vector:

$$
\begin{array} { r } { \left. \frac { \mathrm { d } \boldsymbol { u } ^ { * } } { \mathrm { d } \beta } \right| _ { \beta = 0 } = - J _ { F } ( \boldsymbol { u } _ { 0 } ^ { * } ) ^ { - 1 } \cdot \frac { \partial F } { \partial \beta } ( \boldsymbol { u } _ { 0 } ^ { * } ) } \\ { = - \underbrace { J _ { F } ( \boldsymbol { u } _ { 0 } ^ { * } ) ^ { - \top } } _ { \mathrm { f o r ~ E B M s } } \cdot \underbrace { \frac { \mathrm { d } \mathcal { L } } { \mathrm { d } \boldsymbol { u } _ { 0 } ^ { * } } } _ { \mathrm { b y ~ D e f . ~ 1 ~ } } = \delta } \end{array}
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_1.jpg)  
Non-symmetric

# Entangled sources of bias:

- Finite differences X - Jacobian asymmetry \~

# Our contributions:

·Disentangle the two sources of bias in non-symmetric EP ·Extend holomorphic EP[2] to non symmetric networks · New homeostatic loss promotes Jacobian symmetry

# Accurate computation of the EP error vector

Forcomplex-differentiable $F$ ：

$$
\left. \frac { \mathrm { d } \pmb { u } ^ { * } } { \mathrm { d } \beta } \right| _ { \beta = 0 } = \ \frac { 1 } { T | \beta | } \int _ { 0 } ^ { T } \pmb { u } _ { \beta ( t ) } ^ { * } e ^ { - 2 \mathrm { i } \pi t / T } \mathrm { d } t .
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_2.jpg)

Derivative as integral √ Non vanishing perturbations

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_3.jpg)  
Teaching amplitude |β|

# Continuous-in-time estimation of the gradient

Presynaptic term (Mean value theorem):

Post synaptic error:

0.4 Raw oscillation Timeaverage   
0.3 Free fixed point   
0.2   
0.1   
0.0   
0 100 200 300 400 Time

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_4.jpg)

The gradient estimate can be computed in continuous time without discrete forward/backward phases $\circledcirc$

# Isolated effect of Jacobian asymmetry

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_5.jpg)

New homeostatic loss:

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_6.jpg)

# Benefits of the homeostatic loss on learning

![](/data/huangyc/Document2All/posterDataOutput_vlm/Improving equilibrium propagation without weight symmetry through Jacobian homeostasis_poster/auto/images/images/fig_7.jpg)  
Epoch

<table><tr><td rowspan="2"></td><td>CIFAR-10</td><td colspan="2">ImageNet 32× 32</td></tr><tr><td>Top-1(%)</td><td>Top-1(%)</td><td>Top-5 (%)</td></tr><tr><td>hEP w/o Lhomeo</td><td>60.4± 0.4</td><td>1</td><td>1</td></tr><tr><td>hEPN=2,β|=1</td><td>81.4±0.1</td><td>1</td><td>一</td></tr><tr><td>hEP(True dβu*)</td><td>84.3± 0.1</td><td>31.4± 0.1</td><td>55.2 ± 0.1</td></tr><tr><td>RBP</td><td>87.8± 0.3</td><td>1</td><td>1</td></tr><tr><td>RBP w/oLhomeo</td><td>87.7 ± 0.2</td><td>1</td><td>1</td></tr><tr><td>Sym. hEPN=2,|β|=1</td><td>88.6±0.2</td><td>36.5± 0.3</td><td>60.8±0.4</td></tr></table>

Homeostatic loss is: - More general than symmetrising weights $\circledast$ - Reduces the gap with the energy-based case L

# References

[1] Scellier,etal Generalizationof equilibrium propagation to vectorfield dynamics.arXiv:1808.04873,2018.

[2]Laborieuxand Zenke.Holomorphic equilibrium propagation computes exact gradients through finite size oscillations.NeurlPS 2022.