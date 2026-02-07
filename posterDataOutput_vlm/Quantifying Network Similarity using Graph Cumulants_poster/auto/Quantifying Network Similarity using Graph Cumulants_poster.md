# Quantifying Network Similarity using Graph Cumulants

Gecia Bravo-Hermsdorf1Lee M.Gunderson1Pierre-André Maugis²Carey E.Priebe3 epartentateritti

# TL;DR:

Using only moments is awkward

“The length of a human averages 1.7 meters, and their average squared length is 2.9 square meters"

Using cumulants is easier to understand

"The length of a human has: a variance of 0.01 meters, a standard deviation of 0.1 meters, arelative fluctuation of $6 \% ^ { \because }$

# Graph Cumulants: the Better Subgraph Statistics

Erdós-Renyi is the new Gaussian...

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_1.jpg)

...degrees are encoded instars..

...c.lustering is encoded in cycles...

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_2.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_3.jpg)

..and bipartite-ness as well!

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_4.jpg)

But are graphcumulants beterfortesting7 (than subgraph densities)

# Apples-to-Apples: A Two-Sample Test

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_5.jpg)

When estimating the covariance..

$$
\begin{array} { r } { \mathsf { C o v } ( \hat { \mu } _ { g } , \hat { \mu } _ { g ^ { \prime } } ) = \underbrace { \left. \hat { \mu } _ { g } \hat { \mu } _ { g ^ { \prime } } \right. } _ { \mathrm { ~ \bar { \boldsymbol { \mu } } h a r d ^ { \prime } ~ } } - \underbrace { \left. \hat { \mu } _ { g } \right. \left. \hat { \mu } _ { g ^ { \prime } } \right. } _ { \mathrm { ~ \bar { \boldsymbol { \mu } } _ { e a s y ^ { \prime } } ~ } } } \end{array}
$$

..the "hard” part uses a combinatorial disjoint union rule

$$
c _ { \Lambda } c _ { \prime } = 4 c _ { \Lambda } + 2 c _ { \Delta } + 2 c _ { \curlyeq } + 4 c _ { \Pi } + c _ { \iota \Lambda }
$$

# Combinatorial Construction of Cumulants

(X)= mean   
μ= K1 (X2)= variance + mean2   
μ2 K2 +K1K1   
$\begin{array} { r l r l r l r l } { \mu _ { 3 } } & { { } = } & { \kappa _ { 3 } } & { } & { { } + \kappa _ { 2 } \kappa _ { 1 } } & { { } + \kappa _ { 2 } \kappa _ { 1 } \cdot } & { { } + \kappa _ { 2 } \kappa _ { 1 } \cdot } & { { } + \kappa _ { 1 } \kappa _ { 1 } \kappa _ { 1 } } \end{array}$ N门门A   
μ=κ+κκ+κκ+κ/κ+κκκ/

# Graph Cumulants Clearly Conquer

Graph cumulants outperform subgraph densities in general..

...and graph cumulants also work for single graph samples!

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_6.jpg)

Why do graph cumulants perform better?

...because their fluctuations look more Vormal!

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_7.jpg)

$" Z ^ { 2 }$ -score" for graphs sampled from the same distribution

# Graph Cumulants in the (semi-)Wild!

# Varying:

Number of subgraphs used byboth tests

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_8.jpg)

# Comparing:

Genetic interaction networks of Arabidopsisand Mouse

# Varying:

Numberof graphspersample used by both tests

# Comparing:

Genetic interaction networks of Humanand Rat

![](/data/huangyc/Document2All/posterDataOutput_vlm/Quantifying Network Similarity using Graph Cumulants_poster/auto/images/images/fig_9.jpg)  
false positive