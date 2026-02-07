# Subtractive Mixture Models via Squaring:

# Representation and Learning

Lorenzo Loconte AleksanteriM.Sladek University of Edinburgh, UK Aalto University,Fl

A！ Aalto University

StefanMengel University of Artois,CNRS,CRIL,FR

Martin Trapp Aalto University, Fl

Arno Solin Aalto University,FI

Nicolas Gillis Université de Mons, BE

Antonio Vergari University of Edinburgh,UK

# Mixture models

$$
p ( \mathbf { X } ) = \sum _ { i = 1 } ^ { K } w _ { i } p _ { i } ( \mathbf { X } ) \quad \mathrm { s u b j e c t t o ~ } \ \lvert w _ { i } \geq 0 \quad \sum _ { i = 1 } ^ { K } w _ { i } = 1
$$

$x$ components can onlybeadded together!

![](/data/huangyc/Document2All/posterDataOutput_vlm/Subtractive Mixture Models via Squaring: Representation and Learning_poster/auto/images/images/fig_1.jpg)

。 8   
Ground Truth w1N1+w2N2 wiNi+..WKNK N1-w2N2

# Fewer components with subtractions

Questions? ...Contributions!

023

# How to learn subtractive mixture models?

$p ( \mathbf { X } ) = \sum _ { i = 1 } ^ { K } w _ { i } p _ { i } ( \mathbf { X } ) \qquad w _ { i } \in \mathbb { R }$ How to ensure $p ( \mathbf { X } )$ is non-negative? $\Longrightarrow$ Imposead-hocconstraintsover the parameters $\times$ challenging to derive in closed-form[1][2][3]

How much more expressive are they? with respect to traditional additive-only mixtures

What is their relationship with other models? understanding why they are expressive .. ... and why they support tractable inference

"We learn exponentially more expressive mixture models with subtractions,by squaring deep tensorized mixtures"

Learning deep subtractive mixtures by squaring layers of a deep circuit

![](/data/huangyc/Document2All/posterDataOutput_vlm/Subtractive Mixture Models via Squaring: Representation and Learning_poster/auto/images/images/fig_2.jpg)

# Squaring mixtures...

$$
p ( \mathbf { X } ) \propto \left( \sum _ { i = 1 } ^ { K } w _ { i } p _ { i } ( \mathbf { X } ) \right) ^ { 2 } = \sum _ { i = 1 } ^ { K } \sum _ { j = 1 } ^ { K } w _ { i } w _ { j } p _ { i } ( \mathbf { X } ) p _ { j } ( \mathbf { X } )
$$

Renormalization:

$$
\begin{array} { r l } {  { \times \mathrm { e n o r m a n } \imath \imath z \mathrm { a t } 1 0 \mathrm { n } ; } } \\ & { \boldsymbol { Z } = \sum _ { i = 1 } ^ { K } \sum _ { j = 1 } ^ { K } w _ { i } w _ { j } \int p _ { i } ( \mathbb { X } ) p _ { j } ( \mathbb { X } ) \mathrm { d } \mathbb { X } \quad \cdot [ \mathscr { W } \mathscr { W }  } \end{array}
$$

Tractable marginalization is supported by exponential families [2] and splines components

![](/data/huangyc/Document2All/posterDataOutput_vlm/Subtractive Mixture Models via Squaring: Representation and Learning_poster/auto/images/images/fig_3.jpg)

十 p²(X）2  
000000  
𝑝² p²P²P1P2 P1P3 P2P3

# ... by squaring circuits

+++ W∈R3×3 W 区区区 xxx +++ 000   
Build deep mixtures with   
layers as "Lego blocks"

# Theorem.exponential separation [4][5]

There is a class of distributions $\mathcal { F }$ overvariables X that can be compactly representedasa shallow squared mixture with negative weights，but the smallest structured decomposable additive-only mixture of any depth computing any $F \in { \mathcal { F } }$ hassize $2 ^ { \Omega ( | \mathbf { X } | ) } .$

Deep additive-only mixtures

Squared subtractive mixture model

）²

![](/data/huangyc/Document2All/posterDataOutput_vlm/Subtractive Mixture Models via Squaring: Representation and Learning_poster/auto/images/images/fig_4.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Subtractive Mixture Models via Squaring: Representation and Learning_poster/auto/images/images/fig_5.jpg)

$$
p ( \mathbf { x } ) \propto \kappa ( \mathbf { x } ) ^ { \top } \mathbf { A } \kappa ( \mathbf { x } ) \ \Rightarrow \sum \Bigl ( \bigl \| \mathbf { w } \bigr \| \Bigr ) ^ { 2 }
$$

Understanding the expressiveness of other models in a unifying framework

Power Gas Hepmass +2 +2 2 100 00 + + MiniBooNE BSDS300 1 ±² + LL Training data + LL Test data -70 ±² -75 -75 -80 -80 -85 K= 10² 103 102 103

# References

[1]B. Zhang and C. Zhang.“Finite mixturemodels with negative components\*.In: MLDM.Springer.20o5, pp.31-41. [2]G.RabuseauandFDenis.Learngnegativemiuremodelsbytensordecompositios.nivpreprintiv:43.4224(2014). j [4]J.MartenadVMedabalii.Otheexpessiveefiiencyofsumproductetwrks.In:aivpeprintiv:14.7(24). [5]A.de Colnet andS.Mengel.“A Compilation ofSucinctness Resultsfor Arithmetic Circuits”,In: KR.2021,pp.205-215. 6]lse [7]ARuiandCrto.RepesetatioEtivePobbiodels.Ne.rrses,,p.22. HZ