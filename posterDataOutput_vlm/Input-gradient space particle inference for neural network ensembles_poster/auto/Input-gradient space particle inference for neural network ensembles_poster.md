# Input-gradient space particle inference for neural network ensembles

TrungTrinh1,Markus Heinonen1,LuigiAcerbi2,Samuel Kaski1.3 1Aalto University，2Helsinki University，3Universityof Manchester {trung.trinh,markus.o.heinonen,samuel.kaski@aalto.fi,luigi.acerbi@helsinki.fi

# Overview

Illustrative experiments

# Tuning the lengthscales $\Sigma$

TL;DR: We learn an ensemble of neural networks that is diverse with respect to their input gradients.

# Repulsive deep ensembles (RDEs) [1]

Description: Train an ensemble $\{ \pmb { \theta } _ { i } \} _ { i = 1 } ^ { M }$ using Wasserstein gradient descent [2], which employsa kernelized repulsion term to diversify theparticles to cover the Bayes posterior $p ( \boldsymbol { \theta } | \mathcal { D } )$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Input-gradient space particle inference for neural network ensembles_poster/auto/images/images/fig_2.jpg)  
First-order Repulsive deep ensembles (FoRDEs)

$$
\small \theta _ { i } ^ { ( t + 1 ) } = \theta _ { i } ^ { ( t ) } + \eta _ { t } \Biggl ( \underbrace { \nabla _ { \theta _ { i } ^ { ( t ) } } \log p ( \theta _ { i } ^ { ( t ) } \mid \mathcal { D } ) } _ { \mathrm { D r i v i n g ~ f o r c e } } - \underbrace { \frac { \sum _ { j = 1 } ^ { N } \nabla _ { \theta _ { i } ^ { ( t ) } } k ( \theta _ { i } ^ { ( t ) } , \theta _ { j } ^ { ( t ) } ) } { \sum _ { j = 1 } ^ { N } k ( \theta _ { i } ^ { ( t ) } , \theta _ { j } ^ { ( t ) } ) } } _ { \mathrm { R e p u l s i o n ~ f o r c e } } \Biggr )
$$

·The driving force directs the particles towards high density regions of the posterior.   
·Therepulsion force pushes the particles away from each other to enforce diversity.

Problem: It is unclear how to define the repulsion term for neural networks: ·weight-spacerepulsionisineffectivedue tooverparameterization. ·function-space repulsion often results in underfitting.

# Possible advantages:

·Each member is guaranteed to represent a different function; ·The issues of weight-and function-space repulsion are avoided; ·Each member is encouraged to learn different features,which can improve robustness.

# Main takeaways

$$
\underbrace { \frac { \partial } { \partial s _ { d } } \kappa ( \mathbf { s } , \mathbf { s } ^ { \prime } ; \Sigma ) } _ { \mathrm { ~ \bf ~ o ~ \ n ~ \ i ~ \Gamma ~ } } = - \frac { s _ { d } - s _ { d } ^ { \prime } } { h \Sigma _ { d d } } \kappa ( \mathbf { s } , \mathbf { s } ^ { \prime } ; \Sigma ) \propto \frac { 1 } { \underbrace { 1 } }
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Input-gradient space particle inference for neural network ensembles_poster/auto/images/images/fig_3.jpg)  
Fora1Dregression task(above) anda 2Dclassification task(below),FoRDEs capture higher uncertainty than baselines in allregions outside of the training data. For the 2D classification task,we visualize the entropy of the predictive posteriors.

Repulsion force in thed-th dimension

Input-gradient-space repulsion can perform beter than weight- and function-space repulsion.

2.Betercorruptionrobustnesscanbeachievedbyconfiguringtherepulsionkernelusing theegen-decompositionoftetainngdata.

Each lengthscale is inversely proportional to the strength of the repulsion force in the corresponding input dimension.

lengthscalein thed-th dimension

Proposition:One should apply strong forces in high-variance dimensions (more in-between uncertainty) and weak forces in low-variance dimensions (less in-betweenuncertainty).

In high-variance data dimensions,distances between In low-variance data dimension,data points lie close to datapointsare large,which lead tomore in-between each other,leading to less in-between uncertainty→we uncertainty→we canapplystrongrepulsion forceto need to use weak repulsion force. push the input gradientsfar awayfromeach other. L

# Benchmark comparison

# Defining the input-gradient kernel k

Givena base kernel $\kappa ,$ wedefine the kernel in the input-gradient space for a minibatchoftrainingsamples $B = \{ ( \mathbf { x } _ { b } , y _ { b } ) \} _ { b = 1 } ^ { B }$ asfollows:

Table1:FoRDE-PCAachieves the bestperformanceundercorruptionswhileFoRDE-Identity outperformsbaselines on cleandata.FoRDE-Tuned outperformsbaselines onboth cleanand corrupted data.Results of REsNET18/CIFAR-1OOaveraged over5 seeds.Each ensemble has10 members.cA,cNLL and cECEare accuracy,NLL,and ECE on CIFAR-100-C.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Input-gradient space particle inference for neural network ensembles_poster/auto/images/images/fig_4.jpg)

·UsePCAtogettheeigenvalesandeigenvectorsof tetrainingdata $\{ \mathfrak { a } _ { d } , \lambda _ { d } \} _ { d = 1 } ^ { D }$ ·Define the base kernel:

$$
\kappa _ { \mathrm { P C A } } ( \mathbf { s } , \mathbf { s } ^ { \prime } ; \Sigma _ { \alpha } ) = \exp \left( - \frac { 1 } { 2 h } ( \mathbf { U } ^ { \top } \mathbf { s } - \mathbf { U } ^ { \top } \mathbf { s } ^ { \prime } ) ^ { \top } \Sigma _ { \alpha } ^ { - 1 } ( \mathbf { U } ^ { \top } \mathbf { s } - \mathbf { U } ^ { \top } \mathbf { s } ^ { \prime } ) \right)
$$

· $\mathbf { U } = \left\lceil \mathbf { u } _ { 1 } \quad \mathbf { u } _ { 2 } \quad \cdots \quad \mathbf { u } _ { D } \right\rceil$ is a matrix containing the eigenvectors as columns. ： ${ \boldsymbol { \Sigma } } _ { \alpha } ^ { - 1 } = ( 1 - \alpha ) \mathbf { I } + \alpha { \boldsymbol { \Lambda } }$ Whereisadagoalmatrixontainngtheeigenvaues

Table 2:FoRDE-PCA achieves the best performance under corruptions whileFoRDE-Identity hasthebestNLLoncleandata.FoRDE-Tuned outperformsmostbaselinesonbothcleanand corrupted data.Resultsof REsNET18/CIFAR-1Oaveraged over5seeds.Each ensemble has10 members.cA,cNLL and cECE areaccuracy,NLL,and ECE onCIFAR-10-C.   

<table><tr><td>METHOD</td><td>NLL↓</td><td>ACCURACY(%)↑</td><td>ECE↓</td><td>CA/CNLL/CECE</td></tr><tr><td>DEEP ENSEMBLES</td><td>0.117±0.001</td><td>96.3±0.1</td><td>0.005±0.001</td><td>78.1/0.78/0.08</td></tr><tr><td>WEIGHT-RDE</td><td>0.117±0.002</td><td>96.2±0.1</td><td>0.005±0.001</td><td>78.0/0.78/0.08</td></tr><tr><td>FUNCTION-RDE</td><td>0.128±0.001</td><td>95.8±0.2</td><td>0.006±0.001</td><td>77.1/0.81/0.08</td></tr><tr><td>FEATURE-RDE</td><td>0.116±0.001</td><td>96.4±0.1</td><td>0.004±0.001</td><td>78.1/0.77/0.08</td></tr><tr><td>FORDE-PCA(OURS)</td><td>0.125±0.001</td><td>96.1±0.1</td><td>0.006±0.001</td><td>80.5/0.71/0.07</td></tr><tr><td>FORDE-IDENTITY(OURS)</td><td>0.113±0.002</td><td>96.3±0.1</td><td>0.005±0.001</td><td>78.0/0.80/0.08</td></tr><tr><td>FORDE-TUNED(OURS)</td><td>0.114±0.002</td><td>96.4±0.1</td><td>0.005±0.001</td><td>79.1/0.74/0.07</td></tr></table>

# Lengthscale tuning experiments

We choose the RBF kernel ona unit sphere as the base kernel $\kappa$

K(si,sj;∑） exp （s-s 1(si-s;) S= Ascalaradaptivelyadjusted Diagonalmatrixcontaining Normalizeinput gradients tounit topreventkernelvanishing. the lengthscales. vectors.

<table><tr><td>METHOD</td><td>NLL↓</td><td>ACCURACY(%)↑</td><td>ECE↓</td><td>CA/CNLL/CECE</td></tr><tr><td>DEEPENSEMBLES</td><td>0.70±0.00</td><td>81.8±0.2</td><td>0.041±0.003</td><td>54.3/1.99/0.05</td></tr><tr><td>WEIGHT-RDE</td><td>0.70±0.01</td><td>81.7±0.3</td><td>0.043±0.004</td><td>54.2/2.01/0.06</td></tr><tr><td>FUNCTION-RDE</td><td>0.76±0.02</td><td>80.1±0.4</td><td>0.042±0.005</td><td>51.9/2.08/0.07</td></tr><tr><td>FORDE-PCA(OURS)</td><td>0.71±0.00</td><td>81.4±0.2</td><td>0.039±0.002</td><td>56.1/1.90/0.05</td></tr><tr><td>FORDE-IDENTITY(OURS)</td><td>0.70±0.00</td><td>82.1±0.2</td><td>0.043±0.001</td><td>54.1/2.02/0.05</td></tr><tr><td>FORDE-TUNED(OURS)</td><td>0.70±0.00</td><td>82.1±0.2</td><td>0.044±0.002</td><td>55.3/1.94/0.05</td></tr></table>

# References

[1FDAge L

ResNet18/CIFAR-100 Cleandata Severity level1,2,3 Severity level 4,5 63.5 44.5 63.0 44.0 62.5 43.5 43.0 0.0 0.5 1.0 0.0 0.5 1.0 0.0 0.5 1.0 ∑-1=I- a I a I- a Λ ·Bluelinesshowaccuraciesof FoRDEs,while dotted orange lines showaccuracies of Deep ensembles. ·When moving from the identity lengthscale I to the PCA lengthscalesA: ·FoRDEs exhibit small performancedegradations onclean images of CIFAR-100; ·while becomes more robust against the natural corruptions of ClFAR-100-C.