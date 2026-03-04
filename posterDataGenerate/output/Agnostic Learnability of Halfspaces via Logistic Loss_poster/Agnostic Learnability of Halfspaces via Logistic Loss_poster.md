# Agnostic Learnability of Halfspaces via Logistic Loss

ZiweiJi(UIUC)KwangnAn(M)PranjalAwasthi(GoogleResearch)SatyenKale(GoogleResearch)StefaniKarp(GoogleResearch&CU)

# Setting.

Binary classification: given by distribution $P$ on $\mathbb { R } ^ { d } \times \{ - 1 , + 1 \} ;$ we have i.i.d. samples from $P$

Linear classifier: $x \mapsto \langle x , w \rangle$

Goal: compete with the optimal solution $\bar { u }$ ,where

$$
\mathcal {R} _ {0 - 1} (\bar {u}) := \Pr_ {(x, y) \sim P} \left(\operatorname {s i g n} \left(\langle \bar {u}, x \rangle\right) \neq y\right) = \mathrm {O P T} > 0.
$$

Logistic regression (LR): let $\ell _ { \log } ( z ) : = \ln ( 1 + e ^ { - z } ) ,$ andlet

$$
\mathcal {R} _ {\log} (w) := \mathbb {E} _ {(x, y) \sim P} \left[ \ell_ {\log} (y \langle w, x \rangle) \right]
$$

denote the population logistic risk of $w$ over $P$

# Contributions.

Prior lower and upper bounds for LR do not match:

·General P: 1- OPT lower bound (Ben-David et al., 2012).   
·Isotropic log-concave distributions: $\widetilde \Omega ( \mathrm { O P T } )$ lowerbound (Diakonikolas et al.,2020).   
"Well-behaved" sub-exponential distributions: $\widetilde { O } ( { \sqrt { \mathrm { O P T } } } )$ upper bound with SGD(Freietal,).

# On "well-behaved" conditions:

· Standard concentration and anti-concentration conditions.   
·Example: a mixture of log-concave dist. (e.g., Gaussian).

Our lower and upper bounds for LR:

· $\Omega ( \sqrt { \mathrm { O P T } } )$ lower bound for well-behaved sub-exp dist.; matching $\widetilde { O } ( { \sqrt { \mathrm { O P T } } } )$ upper bound from (Frei et al.,2021).   
· ${ \widetilde { O } } ( { \mathrm { O P T } } )$ upperbound with"radialLipschitzness"

Upper bounds beyond LR:

·Diakonikolas et al. (2020) designed a nonconvex SGD that achieves $O ( \mathrm { O P T } ) + \epsilon$ risk using $\widetilde { O } ( d / \epsilon ^ { 4 } )$ samples. They can also handle heavy-tailed distributions.   
· Other prior algorithms achieving $O ( \mathrm { O P T } ) + \epsilon$ risk involve solving multiple rounds of convex program (Awasthi et al.,2014; Daniely,2015).   
· We design a simple two-phase convex program that achieves ${ \cal O } ( \mathrm { O P T } \ln ( 1 / \mathrm { O P T } ) ) + \epsilon$ risk using $\widetilde { O } ( d / \epsilon ^ { 2 } )$ samples, without radial Lipschitzness.

# Lower bound.

We construct a distribution Q with three parts $Q _ { 1 } , Q _ { 2 } , Q _ { 4 }$ (One part $Q _ { 3 }$ is omitted for simplicity.)

1. $Q _ { 1 }$ consists of two squares with edge length $\sqrt { \mathrm { O P T } / 2 }$ and density 1;one has center $( { \sqrt { 2 } } / 2 , - { \sqrt { 2 } } / 2 )$ and label $^ { - 1 }$ ,the other has center $( - { \sqrt { 2 } } / 2 , { \sqrt { 2 } } / 2 )$ and label $+ 1$   
2. $Q _ { 2 }$ is supported on $[ 0 , \sqrt { \mathrm { O P T } } ] \times [ 0 , 1 ]$ and $[ - \sqrt { \mathrm { O P T } } , 0 ] \times$ $[ - 1 , 0 ]$ with density1,andthe label is given by $\mathrm { s i g n } ( x _ { 1 } )$   
3. $Q _ { 4 }$ is the uniform distribution over the unitball with density 94 := 1-OPT-2VOPT $\begin{array} { r } { q _ { 4 } : = \frac { 1 - \mathrm { O P T } - 2 \sqrt { \mathrm { O P T } } } { \pi } } \end{array}$ and label sign $\left( x _ { 1 } \right)$

![](visuals/images/fig_1.jpg)

Theorem. Q is well-behaved and sub-exponential,and the global minimizer $\boldsymbol { w } ^ { * }$ of $\mathcal { R } _ { \mathrm { l o g } }$ has $\mathcal { R } _ { 0 - 1 } ( w ^ { * } ) = \Omega ( \sqrt { \mathrm { O P T } } )$

# Proof ideas:

·To minimize $\mathcal { R } _ { \mathrm { l o g } }$ on $Q _ { 4 } ,$ we should go to infinity along $( 1 , 0 )$   
· $Q _ { 1 }$ keeps $\boldsymbol { w } ^ { * }$ bounded with $\lVert \boldsymbol { w } ^ { * } \rVert = O ( 1 / \sqrt { \mathrm { O P T } } )$   
· $Q _ { 2 }$ drags $\boldsymbol { w } ^ { * }$ above by an angle of $\Omega ( \sqrt { \mathrm { O P T } } )$

# Upper bound: radial Lipschitzness.

To exclude Q and overcome the lower bound,we make the following assumption for LR.

Radial Lipschitzness: There exists a measurable function $\kappa : \mathbb { R } _ { + }  \mathbb { R } _ { + }$ such that for any two-dimensional subspace V,letting $p _ { V }$ denote the density of the projection of feature distribution onto $V$ ,then

$$
| p _ {V} (r, \theta) - p _ {V} (r, \theta^ {\prime}) | \leq \kappa (r) | \theta - \theta^ {\prime} |.
$$

·Holds if $p _ { V }$ is Lipschitz, even non-log-concave ones (e.g., Gaussian mixtures).   
·Does not hold for general log-concave distributions.   
· Does not hold for $Q _ { \ l }$ ,non-Lipschitz near the vertical axis.

# Upper bound: logistic regression.

Projected gradient descent (PGD): let $w _ { 0 } : = 0 ,$ and

$$
w _ {t + 1} := \Pi_ {\mathcal {B} (1 / \sqrt {\epsilon})} \left[ w _ {t} - \eta \nabla \widehat {\mathcal {R}} _ {\log} (w _ {t}) \right].
$$

Theorem. If the dist. is well-behaved, sub-exponential and radially-Lipschitz, with learning rate $\widetilde { \Theta } ( 1 / \dot { d } )$ ，using $\mathrm { p o l y } ( d , 1 / \epsilon , \ln ( 1 / \delta ) )$ samples and iterations, with prob. $1 - \delta$ PGD outputs $w _ { t }$ with

$$
\mathcal {R} _ {0 - 1} (w _ {t}) = \widetilde {O} (\mathrm {O P T}) + \epsilon .
$$

Proof ideas: under the given conditions, suppose $\hat { w }$ satisfies $\mathcal { R } _ { \log } ( \hat { w } ) \leq \mathcal { R } _ { \log } ( \Vert \hat { w } \Vert \bar { u } ) + \epsilon ^ { \prime } ,$ then

$$
\mathcal {R} _ {0 - 1} (\hat {w}) = \widetilde {O} \left(\max  \left\{\mathrm {O P T}, \sqrt {\frac {\epsilon^ {\prime}}{\| \hat {w} \|}}, \frac {C _ {\kappa}}{\| \hat {w} \| ^ {2}} \right\}\right). \tag {1}
$$

· $C _ { \kappa } = O ( \mathrm { l n } ( 1 / \mathrm { O P T } ) ^ { 2 } )$ for Lipschitz density.   
·The globaloptimizer $\boldsymbol { w } ^ { * }$ of $\mathcal { R } _ { \mathrm { l o g } }$ satisfies $\lVert \boldsymbol { \dot { w } } ^ { * } \rVert = \widetilde { \Omega } ( 1 / \sqrt { \mathrm { O P T } } ) ;$ ： PGD also ensures $w _ { t }$ has small $\epsilon ^ { \prime }$ and $\lVert \boldsymbol { w } _ { t } \rVert = \widetilde { \Omega } ( 1 / \sqrt { \mathrm { O P T } } )$

# Upper bound: two-phase convex program.

Motivation: (1) holds for the hinge loss $\ell _ { h } ( z ) : = \operatorname* { m a x } \{ - z , 0 \}$ without radial Lipschitzness!

$$
\mathcal {R} _ {0 - 1} (\hat {w}) = \widetilde {O} \left(\max  \left\{\mathrm {O P T}, \sqrt {\frac {\epsilon^ {\prime}}{\| \hat {w} \|}} \right\}\right).
$$

However, the global minimizer of $\mathcal { R } _ { h }$ is O;if we find $\hat { w }$ by global minimization,as $\epsilon ^ { \prime }$ gets small, $\| \hat { w } \|$ also gets small.

Ideas: LR followed by restricted Perceptron:

·LR finds unit $v$ that is $\widetilde { O } ( \sqrt { \mathrm { O P T } } )$ away from $\bar { u }$   
· Then minimize $\mathcal { R } _ { h }$ over $\mathcal { D } : = \{ w | \langle w , v \rangle \geq 1 \}$

$$
- \forall w \in \mathcal {D}, \| w \| \geq 1.
$$

$$
- \| \hat {w} \| \bar {u} \text {m a y n o t i n} \mathcal {D}, \text {b u t} (1 + \widetilde {\mathcal {O}} (\mathrm {O P T})) \| \hat {w} \| \bar {u} \in \mathcal {D}!
$$

· Use SGD for better sample complexity.

Theorem. If the dist. is well-behaved and sub-exponential, using $\widetilde { O } ( d / \epsilon ^ { 2 } )$ samples, SGD can achieve zero-one risk $O ( \mathrm { O P T } \ln ( 1 / \mathrm { O P T } ) ) + \epsilon$