# Unveiling Privacy, Memorization,and Input Curvature Links

DeepakRavikumar,Efstathia Soufleri,Abolfazl Hashemi,Kaushikoy

OVERVIEW

DeepNeural Nets(DNNs)oftenoverfitandmemorizetrainingdataimpactinggeneralization,noisylearningand privacy. Feldman(2o19)proposedaformalmemorizationscore,butitiscomputationallyintensive.Recentworklinksinputloss curvaturewithmemorization,showingittobemuchmoreeficient.Wetheoreticallyconnectmemorization,diferential privacy,and input loss curvature, validating our findings on ClFAR and ImageNet datasets.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_1.jpg)

Semiconductor Research Corporation

U.S. National NSF Science Foundation

# Motivation and Background

# Low Input Curvature Typical Easy

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_2.jpg)

Images from ImageNet ranked using input losscurvature. Input loss curvature wasobtained usinga single ResNet18 trained on ImageNet. Ten lowest curvature samples (top) and ten highest curvature samples (bottom) from the training set are visualized for5classes (each rowisa class) from lmageNet.Low curvature samplesare‘prototypical'of theirclass,while high curvature samplesare rare,difficult,and more likely memorized instances

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_3.jpg)

High Input Curvature Atypical Hard

# Theory

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_4.jpg)

Ourtheoretical framework provides upper bounds in Theorems5.1, 5.3,and5.4.Theseare visualizedas linksbetweenDifferential Privacy,Memorization,and Input Loss Curvature.

# Differential Privacy vs.Input Curvature

# Theoretical Results

Input Curvature is given by $\mathrm { C u r v } _ { \phi } ( z _ { i } , S ) = \operatorname { t r } ( H ) = \operatorname { t r } \left( \nabla _ { z _ { i } } ^ { 2 } l ( h _ { s } ^ { \phi } , z _ { i } ) \right)$   
Theorem 5.1Input Curvature Upper Bounds   
Memorization   
Lemma 5.2 Privacy $\Rightarrow$ Stability   
Theorem5.3Privacy $\Rightarrow$ Low Input Loss Curvature   
Theorem5.4Privacy $\Rightarrow$ LessMemorization

# Empirical Results

Memorization vs.Input Curvature

Memorization Input Curvature Theorem 5.1

Herewe aimto understand howmemorizationchanges withcurvature.The experiment aims to plot the memorization score vs.curvature score to validate our theoretical results.Wecalculate curvature scoresby averagingovermanyseedsat theendof training.This measurement is proportional to the expected curvature score in Theorem 5.1

CIFAR100 0.012   
0.010 0.008   
0.004 0.006 Theory Best Fit Theory Best Fit,Subpop.bound 0.002 × Empirical 0.0 0.2 0.4 0.6 0.8 1.0 Avg.Mem Score

Plotof memorization score vs.input loss curvatureat the end of training for CIFAR100 (average over1000Small Inception models)

Plot of   
memorizationscore vs.input loss curvatureatthe end of training for   
ImageNet (average   
over100ResNet50 models)

Pia Theorem5.3 Input Curvature

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_5.jpg)

We study the relation between privacyand curvature,we train privateResNet18modelson CIFAR1O and CIFAR1OO usingDP-SGD (Abadi et al.,2016).We aim to plot privacy budget vs curvature scoreandvalidateTheorem5.3

Result of studying the   
link between input loss curvature and privacy   
budget. All these results stronglycorrelatewith theory and validate Theorem 5.3.   
0.00070 0.00065 x\*xxXxX X X + +++ +++++ +   
0.00055   
0.00050 Thcory Best FitCIFAR10 × Empirical CIFAR10   
0.00045 Theory BestFit CIFAR100   
0.00040 + EmpiricalCIFAR100 0 20 40 60 80 100 Privacy Budget

# Summary

# Differential Privacyvs.Memorization

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_6.jpg)

We how privacy affects memorization for the top 5oo most memorized examples.This is done by varying the privacy budget. The results align with Theorem 5.4,showing an increase in memorizationas the privacy budget increases.

Plotofdifferential privacy vs memorization for CIFAR100 and the upperboundfrom theTheorem5.4

![](/data/huangyc/Document2All/posterDataOutput_vlm/Unveiling Privacy, Memorization, and Input Curvature Links_poster/auto/images/images/fig_7.jpg)  
Privacy Budget

The memorization scores are significantly lower than the bound from Theorem5.4 supportingNasr etal.(2021)'sobservation thatDP-SGD may be overly conservative.

We explore the theoretical link between memorization, curvature,and privacy. Theoretical analysis is based on assumptions of stability,generalization,andLipschitzness,applicable to non-convex settings like DNNs. Main result: Memorization is upper-bounded by the curvature of the loss with respect to input and privacy.   
. Privacy bounds input curvature and memorization   
Theory validated using DNNs on CIFAR100 and ImageNet,showinga strongmatch between theoretical predictions and empirical results.

# MIA Perspective

Acommonapproach to measure privacy is viamembership inferenceattack (MIA),We used the LiRA (Carlini etal.,2022). Morememorized samplesare easier to detect usingMlA attacks. ForlmageNet MlA performancedependson theaccuracyof the samplesin the trainset.If theaccuracy on the trainset is highand memorization is low,MlA is unsuccessful (mem.score $\mathbf { \Omega } < 0 . 1 $ ).If the memorizationis high but themodel is inaccurate (scorerange0.4 $- 0 . 7 )$ thendue to lack ofmodel learningMlA isunsuccessful but toalesser extent.However,if memorization is highand accuracy onthesamplesis high MlA is successful (mem.score $> 0 . 7$ ).

100 ImageNet   
X MIA Balancod Accuracy   
90 X Trainset Accuracy X AUROC X   
80 \*   
70 xxxxx X xxxx X X xx X   
60 xX x   
50   
Radom Classifer Acc.(Lower bounid）   
40   
0.0 0.2 0.4 0.6 0.8 1.0 Avg. Mem Scorc   
100 × X X X CIFAR100 X X X X X X X X   
80 xxxxxXxxxxxxxxxxxx   
X   
60   
RandomClassifer Aco(Lowerbound)   
40 X MIA Balanced Aueuracy × Treinset Accurey   
20 × AUROC   
0.0 0.2 0.4 0.6 0.8 1.0 Avg.Mem Score

# References

Abadi,M.,Chu,A.,Goodfellow,I.,McMahan,H.B.,Mironov,1.,Talwar,K.,andZhang,L.Deeplearning withdifferentialprivacy.In Proceedingsof the2016ACMSIGSACconferenceoncomputerand communicationssecurity,pp.308-318,2016

Feldman,V.Does learning require memorization?ashorttaleaboutalongtail.arXivpreprint arXiv:1906.05271,2019

Nasr,M.,SongiS.akurta,A.,Papernot,N.,andCarlini,N.Adversaryinstantiation:Lowerboundsfor differentiallyprivatemachinelearning.In2O21IEEESymposiumonsecurityandprivacy(SP),pp.866- 882.IEEE,2021.