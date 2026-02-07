# Bayesian Inverse Transition Learning for Offline Settings

Leo Benac,Sonali Parbhoo,Finale Doshi-Velez

# Summary

Lcarningamodel ishard under low-covcragc data   
Having a model help be more data efficient   
·Inverse Transition Learning infers the dynamics using near-optimal   
demonstrations   
We create a set of constraints to estimate in a gradient-free way an   
empirical posterior distribution over the transition dynamics $T$ ,where each sample has near-optimal guarantees   
$\circ$ Show that planned policies are highly performant and exhibit lower variance across different batches of datas compared to MLE estimates   
Explain how quantifying the uncertainty of the dynamics help planning morc informativc policics than thc cxpcrt policy and thc onc obtaincd from MLE estimates

# What is Inverse Transition Learning?

Inverse Transition Learning   
Expert Behavior   
?   
Rewards ITL Dynamics

Infer thc dynamics T givcn ncar-optimal demonstrations $\mathcal { D }$ ,thcrcward function $R$ and a near-optimal expert policy $\pi _ { \epsilon }$ where $\pi _ { \epsilon }$ isassumed to only take actions that are $\epsilon$ -close to the best unkown action $a ^ { * }$ .

# Why is it hard?

· Number of parameters grows with the dimensions of state and action   
spaces   
Trade-off between a model that is expressive enough and one that is   
small enough to learn   
Lack of covcrage in offinc invcrsc scttings

# Why do we care?

Data efficiency Simulation of ncw data ·Off-Policy Evaluation $\circledast$ Counterfactual Reasoning

# Baselines

$\nu T ^ { \ M L E }$ Maximum Likelihood Estimateobtained from the expert   
demonstrations $\mathcal { D }$   
$P ( T ( s ^ { \prime } | s , a ) | \mathcal { D } ) = D i r ( N _ { s , a } + \mathbf { 1 } | s , a )$ Probabilistic model over $\mathrm { T }$ without   
making any optimality assumption. Where $\mathbf { 1 }$ isavector of $\rceil$ 'sof   
dimension $| S |$ and $\Lambda _ { s . a }$ is the number of transitions from state s and   
actionainthcbatchdata $\mathcal { D }$

# Constraints

Using the reward $R$ and near-optimal expert policy $\pi _ { \epsilon }$ we create a set of constraints with respect to the dynamics $T$ to impose the values of the actions of the expert to be superior to the ones of unseen actions.

# Method

·Sample from $I ^ { \prime } ( T | \mathcal { D } )$ and only keep samples that satisfies the   
constraints.   
Crcatc cmpirical postcrior $P ( T | \mathcal { D } , \pi _ { \epsilon } )$ with acccptcd samplcs. This will be the estimate of the posterior on $T$ given that the demonstrations from the expert are near-optimal

# Metric

$$
Q _ { m c t r i c } ^ { * } ( \hat { \pi } ) = \sum _ { s \in S } \bigg ( Q ^ { * } ( s , a ^ { * } ) - \sum _ { a \in \Lambda } \hat { \pi } ( a | s ) Q ^ { * } ( s , a ) \bigg )
$$

# Results

·MLE   
$\boldsymbol { \widehat { T } } = \boldsymbol { T } ^ { M L E } \underset { \mathrm { V a l u e ~ I t e r a t i o n } } { \longrightarrow } \left( \pi ^ { M L E } , Q ^ { M L E } \right) = \left( \boldsymbol { \widehat { \pi } } , \boldsymbol { \widehat { Q } } \right) \underset { \mathrm { C o m p u t e ~ R e s u l t s } } { \longrightarrow }$   
· $P ( T | \mathcal { D } , \pi _ { \epsilon } )$ and $P ( T | \mathcal { D } )$   
$\begin{array} { r l } & { \{ \widehat { T } ^ { ( i ) } \} _ { i = 1 } ^ { 1 0 0 0 } \sim \mathrm { P o s t e r i o r } \underset { \mathrm { V a l u e ~ I t e r a t i o n } } { \longrightarrow } \{ ( \widehat { \pi } ^ { ( i ) } , \widehat { Q } ^ { ( i ) } ) \} _ { i = 1 } ^ { 1 0 0 0 } } \\ & { \mathrm { F m p i r i c a l ~ M e a n } \{ ( \widehat { \pi } , \widehat { Q } ) \} _ { \mathrm { C o m p u l t e ~ R e s u l l s } } } \end{array}$ $\varepsilon = 0$ LowData $\varepsilon = 0$ HighData 300 MLE MLE   
\* 200 PTID,) P(TD,n)   
O 100 0 ε=3,LowData $\varepsilon = 3$ HighData 300 MLE MLE   
￥ 200 PTID,) P(TD,)   
Q 100 0 ε=4,LowData $\varepsilon = 4$ HighData 300 MLE MLE   
\* 200 PTID, P(TID,n)   
Q 100 0 0 500 1000 0 500 1000 Dataset# Dataset#

· $P ( T | \mathcal { D } , \pi _ { \epsilon } )$ outcrperforms both basclincs by bcing more accurate and avoiding low value actions $P ( T | \mathcal { D } , \pi _ { \epsilon } )$ exhibits significantly less variance over different datasets · $P ( T | \mathcal { D } , \pi _ { \epsilon } )$ allows quantifying uncertainty on corresponding policies

# Acknowledgements

This material is based upon work supported by the National Science Foundation under Grant No. IIS-20o7o76. Any opinions, findings,and conclusions orrecommendationsexpressed inthismaterial are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.