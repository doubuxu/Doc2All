# TL;DR:

Graph cumulants perform better and are more intuitive than the typical subgraph statistics

Using only moments is awkward

"The length of a human averages 1.7 meters,

and their average squared length is 2.9 square meters"

Using cumulants is easier to understand

“The length of a human has: a variance of 0.01 meters,

a standard deviation of 0.1 meters,

a relative fluctuation of $6 \% ^ { \prime }$

# Graph Cumulants: the Better Subgraph Statistics

Erd6s-Rényi is the new Gaussian...

![](visuals/images/fig_1.jpg)

![](visuals/images/fig_2.jpg)

![](visuals/images/fig_3.jpg)

...degreesare encoded in stars...

![](visuals/images/fig_4.jpg)

...clustering is encoded in cycles..

![](visuals/images/fig_5.jpg)

![](visuals/images/fig_6.jpg)

![](visuals/images/fig_7.jpg)

...and bipartite-ness as well!

![](visuals/images/fig_8.jpg)

But

are graph cumulants better for testing?

(than subgraph densities)

# Apples-to-Apples: A Two-Sample Test

![](visuals/images/fig_9.jpg)

![](visuals/images/fig_10.jpg)

$$
\hat {d} _ {\kappa} ^ {2} (\mathbf {A}, \mathbf {B}) = \left(\hat {\kappa} (\mathbf {A}) - \hat {\kappa} (\mathbf {B})\right) ^ {\top} \left(\hat {\Sigma} _ {\kappa} (\mathbf {A}) + \hat {\Sigma} _ {\kappa} (\mathbf {B})\right) ^ {- 1} \left(\hat {\kappa} (\mathbf {A}) - \hat {\kappa} (\mathbf {B})\right)
$$

$$
\underbrace {\hat {d} _ {\mu} ^ {2} (\mathbf {A} , \mathbf {B})} _ {\text {" Z ^ {2} - s c o r e "}} = \underbrace {\left(\hat {\mu} (\mathbf {A}) - \hat {\mu} (\mathbf {B})\right) ^ {\top}} _ {\text {d i f f e r e n c e}} \underbrace {\left(\hat {\Sigma} _ {\mu} (\mathbf {A}) + \hat {\Sigma} _ {\mu} (\mathbf {B})\right) ^ {- 1}} _ {\text {m e t r i c}} \underbrace {\left(\hat {\mu} (\mathbf {A}) - \hat {\mu} (\mathbf {B})\right)} _ {\text {d i f f e r e n c e}}
$$

When estimating the covariance...

$$
\operatorname {C o v} \left(\hat {\mu} _ {g}, \hat {\mu} _ {g ^ {\prime}}\right) = \underbrace {\left\langle \hat {\mu} _ {g} \hat {\mu} _ {g ^ {\prime}} \right\rangle} _ {\text {" h a r d "}} - \underbrace {\left\langle \hat {\mu} _ {g} \right\rangle \left\langle \hat {\mu} _ {g ^ {\prime}} \right\rangle} _ {\text {" e a s y "}}
$$

...the“hard” part uses a combinatorial disjoint union rule

$$
c _ {\Lambda} c _ {/} = 4 c _ {\Lambda} + 2 c _ {\Delta} + 2 c _ {\perp} + 4 c _ {\cap} + c _ {\Lambda}
$$

# Combinatorial Construction of Cumulants

$$
\begin{array}{c c c} \bullet & & \odot \\ \mu_ {1} & = & \kappa_ {1} \end{array}
$$

$\left. X \right. = { \mathsf { m e a n } }$

![](visuals/images/fig_11.jpg)

![](visuals/images/fig_12.jpg)

<X²)= variance + mean²

![](visuals/images/fig_13.jpg)

![](visuals/images/fig_14.jpg)

![](visuals/images/fig_15.jpg)

![](visuals/images/fig_16.jpg)

![](visuals/images/fig_17.jpg)

![](visuals/images/fig_18.jpg)

![](visuals/images/fig_19.jpg)

![](visuals/images/fig_20.jpg)

![](visuals/images/fig_21.jpg)

![](visuals/images/fig_22.jpg)

# Graph Cumulants Clearly Conquer

Graph cumulants outperform subgraph densities in general...

...and graph cumulants also work for single graph samples!

![](visuals/images/fig_23.jpg)

![](visuals/images/fig_24.jpg)

Why do graph cumulants perform better?

...because their fluctuations lookmoreNormal!

![](visuals/images/fig_25.jpg)

![](visuals/images/fig_26.jpg)

"Z2-score" for graphs sampled from the same distribution

# Graph Cumulants in the (semi-)Wild!

![](visuals/images/fig_27.jpg)

Varying:

Number of subgraphs

used by both tests

Comparing:

Genetic interaction networks of Arabidopsisand Mouse

Varying:

Number of graphs per sample used by both tests

Comparing:

Genetic interaction networks of Humanand Rat

![](visuals/images/fig_28.jpg)