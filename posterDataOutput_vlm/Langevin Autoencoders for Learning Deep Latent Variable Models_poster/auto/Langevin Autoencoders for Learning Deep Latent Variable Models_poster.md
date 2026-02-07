# Langevin Autoencoders for Learning Deep Latent Variable Models

# Motivation

# Learning deep latent variablemodels

Latentvariablemodels

$$
p ( \mathbf { x } ; \pmb { \theta } ) = \int p ( \mathbf { x } \mid z ; \pmb { \theta } ) p ( z ) d z
$$

# Gradientovermodel parameters

$$
\nabla _ { \pmb { \theta } } \mathbb { E } _ { \hat { p } _ { \mathrm { d a t a } } ( \mathbf { x } ) } [ \mathrm { l o g } p ( { \pmb x } ; { \pmb \theta } ) ] \approx \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \mathbb { E } _ { p \left( \mathbf { z } ^ { ( i ) } \mid \mathbf { x } ^ { ( i ) } ; { \pmb \theta } \right) } \left[ \nabla _ { \pmb { \theta } } \mathrm { l o g } p \left( \mathbf { x } ^ { ( i ) } , { \pmb z } ^ { ( i ) } ; { \pmb \theta } \right) \right]
$$

·To learna latent variablemodel via gradient ascent,we need to approximate theexpectationover the latentposterior $p ( \mathbf { z } \mid \mathbf { x } ; \pmb \theta )$ which is intractable ingeneral. Variational inferenceisadominantapproachof approximation (e.g.,VAE [1]),buttheapproximationpower is limited. MarkovchainMonteCarlo (MCMC)iscapableofapproximatecomplex posteriors,but is too slowdue to datapoint-wise iterations.

# Preliminary

# Langevindynamics

·Langevindynamics[2]isa gradient-basedMCMC.

$$
\begin{array} { l } { { z ^ { \prime } \sim q ( z ^ { \prime } \mid z ) = \mathcal { N } ( z ^ { \prime } ; z + \eta \nabla _ { z } { \log p ( x , z ; \theta ) } , 2 \eta I ) } } \\ { { z  z ^ { \prime } \mathrm { w i t h ~ p r o b a b i l i t y ~ m i n ~ } \{ 1 , \displaystyle \frac { p ( x , z ^ { \prime } ; \theta ) q ( z \mid z ^ { \prime } ) } { p ( x , z ; \theta ) q ( z ^ { \prime } \mid z ) } \} } } \end{array}
$$

·Byrepeating this iterative update,thesamplesasymptoticallyapproach to the true posterior $p ( \mathbf { z } \mid \mathbf { x } ; \pmb \theta )$ .

·MCMC iterationsare independentlyperformed for each posteriorper datapoint $p ( z ^ { ( i ) } \mid \boldsymbol { x } ^ { ( i ) } ; \boldsymbol { \theta } )$ for $i = 1 , . . . , n$

# →How can we amortize the cost of datapoint-wise iterations?

![](/data/huangyc/Document2All/posterDataOutput_vlm/Langevin Autoencoders for Learning Deep Latent Variable Models_poster/auto/images/images/fig_1.jpg)  
(a) Variational inference

# Method

# Amortized Langevin dynamics

![](/data/huangyc/Document2All/posterDataOutput_vlm/Langevin Autoencoders for Learning Deep Latent Variable Models_poster/auto/images/images/fig_2.jpg)

$\cdot$ In ouramortized Langevindynamics (ALD),weprepareanencoder that mapstheobserveddata into the latentvariable,andrunMCMCon its parameterspace.

$\cdot$ Markovchainonthe latent space is implicitlyperformedbycollecting the outputof the encoder.

·Our main theorem shows that theALDisvalidas MCMC if the encoder takes the form of:

$$
f _ { { \mathbf { Z } } | { \mathbf { x } } } ( { \mathbf { x } } ; { \Phi } ) = \Phi g ( { \mathbf { x } } ) .
$$

·Itcanbeeasilyimplementedusinganeural netwhoseparametersare fixed except forthe lastlinear layer.

# LangevinAutoencoder

$\cdot$ ALDcan beapplied to the training of deep latent variable models (DLVMs) byslightlymodifying the learningalgorithm of traditional autoencoders. ·Wecalltis learning algorithmof DLVMs the Langevinautoencoder (LAE).

$$
\begin{array} { r l } & { V _ { T } = - \sum _ { i = 1 } ^ { n } \log p ( \boldsymbol { x } ^ { ( i ) } , \boldsymbol { z } ^ { ( i ) } = \Phi g ( \boldsymbol { x } ^ { ( i ) } ; \boldsymbol { \psi } ) ; \boldsymbol { \theta } ) } \\ & { \boldsymbol { \theta }  \boldsymbol { \theta } - \eta \nabla _ { \boldsymbol { \theta } } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } V _ { t } } \\ & { \boldsymbol { \psi }  \boldsymbol { \psi } - \eta \nabla _ { \boldsymbol { \psi } } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } V _ { t } } \end{array}
$$

# Results

Toy example

![](/data/huangyc/Document2All/posterDataOutput_vlm/Langevin Autoencoders for Learning Deep Latent Variable Models_poster/auto/images/images/fig_3.jpg)

$\cdot$ Weperformposterior inference forarandomlyinitialized DLVMusing variational inference (Vl) and our ALD. $\cdot$ VIfailstocapture themultimodalityof thetrueposterior. ·Our ALDcanapproximatecomplexmultimodalposteriorsintoy examples.

# Imagedensityestimation

<table><tr><td></td><td>MNIST</td><td>SVHN</td><td>CIFAR-10</td><td>CelebA</td></tr><tr><td>VAE</td><td>1.189±0.002</td><td>4.442±0.003</td><td>4.820±0.005</td><td>4.671±0.001</td></tr><tr><td>VAE-flow</td><td>1.183±0.001</td><td>4.454±0.016</td><td>4.828±0.005</td><td>4.667±0.005</td></tr><tr><td>Hoffman（2017）[3]</td><td>1.189±0.002</td><td>4.440±0.007</td><td>4.831±0.005</td><td>4.662±0.011</td></tr><tr><td>LAE (ours)</td><td>1.177±0.001</td><td>4.412±0.002</td><td>4.773±0.003</td><td>4.636±0.003</td></tr></table>

Likelihood evaluation for testdata

·OurLAEconsistently outperforms Vl-based methods suchas the VAEand otherexistingMCMC-based methods.

# Future works

·Howcan we remove the bias of finite-step MCMC samples? ·Recentlyproposed unbiased MCMC methods [4]may beuseful.

·Isitpossible toapplytheALD (andLAE)tothestate-of-the-art DLVMs, such as NVAE[5]?

# References

[1]DiederikPKingmaand Max Welling(2013).“Auto-encodingvariational bayes.In:arXivpreprintarXiv:1312.6114.

[2]Radford M Neal (2011)."Mcmc using hamiltonian dynamics." In: Handbook of Markov Chain MonteCarlo,page113.

[3]MatthewD Hoffman (2017).“Learning deep latent gaussianmodelswith markovchainmontecarlo."In:International conferenceonmachine learning,pages1510-1519.PMLR.

[4]PierreEJacob,JohnO'Leary，andYvesFAtchadé(202O).“Unbiased markovchainmontecarlomethodswith couplings."In:Journal of the Royal Statistical Society:SeriesB(Statistical Methodology),82(3):543-600.

[5]Arash Vahdatand JanKautz(2o2O).“Nvae:Adeep hierarchical variationalautoencoder.In:AdvancesinNeural InformationProcessing Systems,33:19667-19679.