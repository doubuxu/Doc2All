# Conditional Matrix Flows for Gaussian Graphical Models

# Gaussian Graphical Models: Graphical Lasso

d d d 1 2 2   
n →d →d 3 3 5 4 5 1 4   
Xi\~N(0,Ω-1 obs.X∈Rnxd s\~Wa(n,Ω-1) S=XTX 12345 precision Ω graphical model

GGMs provides structural information: $\Omega _ { i j } = 0$ implies conditional independence of features $i$ and $j$ given all remaining features

Maximum likelihood estimate of $\Omega$ is not sparse and for $d > n$ is not unique penalized likelihood to encourage sparse $\Omega$ $\begin{array} { r } { \operatorname * { a r g m a x } _ { \Omega \sim 0 } \{ \log \operatorname* { d e t } \Omega - \operatorname { T r } ( \frac { 1 } { n } S \Omega ) - \lambda \| \Omega \| _ { 0 } \} } \end{array}$

Intractable because the objective is highly non-convex · Graphical Lasso: use convex relaxation $\| \Omega \| _ { 0 } \longrightarrow \| \Omega \| _ { 1 }$

# Benefits

$\clubsuit$ Solution path: frequentist approach provides solutions as a function of $\lambda$

# Limitations

$\clubsuit$ Over-shrinking: $l _ { 1 }$ norm causes well-known over-shrinking of features $\clubsuit$ No credibility interval

# Bayesian Graphical Lasso

Bayesian approach: $p ( \Omega | S , \lambda ) \propto p ( S | \Omega ) \ p ( \Omega | \lambda )$ Encourage sparsity with double exponential prior (DE) $\begin{array} { l } { { p ( S | \Omega ) \propto \mathcal { W } _ { d } ( n , \Omega ^ { - 1 } ) } } \\ { { p ( \Omega | \lambda ) \propto \mathcal { W } _ { d } ( d + 1 , \lambda 1 _ { d } ) \displaystyle \prod _ { i < j } \mathrm { D E } ( \omega _ { i j } | \lambda ) I [ \Omega \sim 0 ] } } \end{array}$ ·Recovers the $l _ { 1 }$ normpenalized likelihood solution in the MAPlimit

# Benefits

Credibility interval: can be computed within Bayesian framework

# Limitations

$\clubsuit$ Expensive posterior sampling: needs Gibbs sampler (also limits prior choice) $\clubsuit$ Over-shrinking:priorcannot be generalized to sub- $\boldsymbol { l } _ { 1 }$ pseudo-norms $\clubsuit$ Expensive solution path: independent Markov chains for each $\lambda$ value

# Conditional Matrix Flow for Gaussian Graphical Models

[Goal:unify benefits of frequentist and Bayesian frameworks while overcoming limitations

Weproposeilrov flowa continuum of sparse regression models jointly forallregularization parameters $\lambda$ and all $l _ { q }$ norms, including non-convex sub- $\mathbf { \cdot } l _ { 1 }$ pseudo-norms.

<table><tr><td colspan="3">PROPOSEDAPPROACH</td></tr><tr><td>VARIATIONAL INFERENCE</td><td></td><td>Posterior approximation and effcient sampling via Normalizing Flow:DkL(p(Ω|S,λ)||p(Ω|S,λ)) ·Freechoice of prior p(Ω|λ) andlikelihood p(S|Ω) →model any BayesianGGMs beyond Lasso</td></tr><tr><td>SUB-1 PSEUDO-NORMS</td><td></td><td>Generalized Gaussian Distributions (GGD) as sparsity-inducing g1/g GGD(x｜λ,q) = -exp{-&gt;|æ/9} priors corresponding to lq (pseudo-) norms 2T(1/@)</td></tr><tr><td>CONDITIONAL FLOW</td><td></td><td>·Condition the Normalizing Flow on入andq toobtainsolution paths · Can select Xby maximizing marginal likelihood</td></tr></table>

# ARCHITECTURE

Hypernetwork λ,q √ Bijections +1) 1 i 2 →. → → d → d → d MM \~ MM p(2) p(/s,X,) p(Ω/s,),q) L（2) [+(2() (2a

· Condition bijections on $\lambda$ and $q$ and define flow on space of symmetric positive definite matrices by construction ·EfficientlogdeterminantofJacobianforCholesky-Product $\cdot \ \mathrm { d e t } \ { \mathcal { I } } _ { \mathrm { C h o l } } ( L ) = 2 ^ { d } \prod _ { i = 1 } ^ { d } ( L _ { i i } ) ^ { d - i + 1 }$

# Combine benefits

# References

# Overcome limitations

N.Meinshausen and P. Buhlmann (2006). "High-dimensional graphs andvariable selection with the Lasso"In: Institute of Mathematical Statistics

H.Wang (2012) "Bayesian Graphical LassoModelsand EfficientPosterior Computation." In: Bayesian Anal.7(4)

$\clubsuit$ Credibility intervals:sample-based credibilityintervals forany $\lambda$ and $q$ $\clubsuit$ Solution paths:we recover Bayesian Graphical Lasso( $T = 1$ and Graphical Lasso solution paths $( T \to 0 )$ bytraining withsimulatedannealing

G.Papamakarios et al （2021)"Normalizing Flowsfor Probabilistic Modelingand Inference" In: Journal of Machine Learning Research 22

$\clubsuit$ Cheap posterior sampling: no need for sequential Gibbs sampler $\clubsuit$ No over-shrinking:GGD prior enables exploration of sub- $l _ { 1 }$ pseudo-norms $\clubsuit$ Model selection: direct access to the marginal likelihood for selecting >

![](/data/huangyc/Document2All/posterDataOutput_vlm/Conditional Matrix Flows for Gaussian Graphical Models_poster/auto/images/images/fig_1.jpg)  
Bayesian solution pathat $T = 1$ &model selection

![](/data/huangyc/Document2All/posterDataOutput_vlm/Conditional Matrix Flows for Gaussian Graphical Models_poster/auto/images/images/fig_2.jpg)  
Frequentist solution path at $T \to 0$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Conditional Matrix Flows for Gaussian Graphical Models_poster/auto/images/images/fig_3.jpg)  
Solution path in sub- $l _ { 1 }$ regime

![](/data/huangyc/Document2All/posterDataOutput_vlm/Conditional Matrix Flows for Gaussian Graphical Models_poster/auto/images/images/fig_4.jpg)  
Credibility intervalsin sub $l _ { 1 }$ regir no over-shrinking