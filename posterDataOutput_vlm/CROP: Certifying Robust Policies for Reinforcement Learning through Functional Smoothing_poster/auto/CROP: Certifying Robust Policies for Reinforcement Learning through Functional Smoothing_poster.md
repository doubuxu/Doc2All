# CROP: Certifying Robust Policies for Reinforcement Learning through Functional Smoothing

Fan Wu1,LinyiLi1, Zijian Huang1,Yevgeniy Vorobeychik²,Ding Zhao3,Bo Li1 1Universityof llinois at Urbana-Champaign 2Washington University in St.Louis3Carnegie Mellon University

# Background & Motivation

Testing and improving the robustness of safety-critical applications before their massive deployment to real-world is of great importance. Robustness certification for a given learning algorithm is needed to end therepeated game between theattackersand defenders.

# Threat Model

Testing-time evasion attack on agent's observation

Adversary can apply $\ell _ { 2 }$ -bounded perturbations $B ^ { \varepsilon } = \{ \delta \in \mathbb { R } ^ { n } \| \| \delta \| _ { 2 } \leq \varepsilon \}$ to input state observations of the agent

![](/data/huangyc/Document2All/posterDataOutput_vlm/CROP: Certifying Robust Policies for Reinforcement Learning through Functional Smoothing_poster/auto/images/images/fig_1.jpg)

# Certification Goal

Provide test-time certification for the performance of the trained agent in the perturbed environment

1．Providing criteria for robustness certification 2.Proposing certification strategies corresponding to different certification criteria

# Certification Criteria

Criterion 1 (state-level): Per-state action stability

Maximum Perturbation Magnitude $\bar { \varepsilon }$ ： $\pi ( s + \delta ) = \pi ( s ) , \forall \delta \in B ^ { \bar { \varepsilon } }$ ，where $B ^ { \varepsilon } = \{ \delta \in \mathbb { R } ^ { n } \mid \| \delta \| _ { 2 } \leq \varepsilon \}$

.e., the policy produces the same action on state s with or without perturbation.

# Criterion 2 (trajectory-level): Cumulative reward lower bound

perturbed cumulative reward $J _ { \varepsilon } ( \pi )$ $J _ { \varepsilon } ( \pi ) : = \sum _ { t = 0 } ^ { \infty } \gamma ^ { t } R \left( s _ { t } , \pi \left( s _ { t } + \delta _ { t } \right) \right)$ where $s _ { t + 1 } \sim P \left( s _ { t } , \pi \left( s _ { t } + \delta _ { t } \right) \right) , s _ { 0 } \sim d _ { 0 }$

Lowerbound of perturbed cumulative reward $\_$ : with perturbations at every step bounded by $B ^ { \varepsilon }$ ,we have $\underline { { J } } \leq J _ { \varepsilon } ( \pi )$

# CROP Framework

# Per-State Action Certification

CROP-LoAct: Local randomized smoothing on states

Action-value functional smoothing Let $Q ^ { \pi } : S \times A  [ V _ { \operatorname* { m i n } } , V _ { \operatorname* { m a x } } ]$ ,then   
smoothed value function: $\widetilde { Q } ^ { \pi } ( s , a ) : = \mathbb { E } _ { \Delta \sim \mathcal { N } ( 0 , \sigma ^ { 2 } I _ { N } ) } Q ^ { \pi } ( s + \Delta , a ) \quad \forall s \in \mathcal { S } , a \in \mathcal { A }$   
smoothed policy: $\begin{array} { r } { \widetilde { \pi } \left( s _ { t } \right) : = \arg \operatorname* { m a x } _ { a } \widetilde { Q } ^ { \pi } \left( s _ { t } , a \right) \quad \forall s _ { t } \in \mathcal { S } } \end{array}$

Properties of the smoothed function ·Lipschitz continuity of ${ \widetilde { Q } } ^ { \pi }$ w.r.t. the state input: $L = \frac { V _ { \operatorname* { m a x } } - V _ { \operatorname* { m i n } } } { \sigma } \sqrt { 2 / \pi }$ $\bar { \varepsilon }$ $r _ { t } = \frac { \sigma } { 2 } \left( \Phi ^ { - 1 } \left( \frac { \widetilde { Q } ^ { \pi } \left( s _ { t } , a _ { 1 } \right) - V _ { \operatorname* { m i n } } } { V _ { \operatorname* { m a x } } - V _ { \operatorname* { m i n } } } \right) - \Phi ^ { - 1 } \left( \frac { \widetilde { Q } ^ { \pi } \left( s _ { t } , a _ { 2 } \right) - V _ { \operatorname* { m i n } } } { V _ { \operatorname* { m a x } } - V _ { \operatorname* { m i n } } } \right) \right)$

# Cumulative Reward Certification

# CROP-GRe: Global smoothing on trajectories

Expectation bound via mean smoothing

· Mean smoothing: $\widetilde { F } _ { \pi } \left( \oplus _ { t = 0 } ^ { H - 1 } \delta _ { t } \right) : = \mathbb { E } _ { \Delta \sim \mathcal { N } ( 0 , \sigma ^ { 2 } I _ { H \times N } ) } F _ { \pi } \left( \oplus _ { t = 0 } ^ { H - 1 } \left( \delta _ { t } + \Delta _ { t } \right) \right)$ Expectation lower bound: $\mathbb { E } \left[ J _ { \varepsilon } \left( \pi ^ { \prime } \right) \right] \geq \widetilde { F } _ { \pi } \left( \oplus _ { t = 0 } ^ { H - 1 } \mathbf { 0 } \right) - L \varepsilon \sqrt { H }$ ,where $\begin{array} { r } { L = \frac { ( J _ { \mathrm { m a x } } - J _ { \mathrm { m i n } } ) } { \sigma } \sqrt { 2 / \pi } } \end{array}$

Percentile bound via percentile smoothing

Percentile smoothing: $\begin{array} { r } { \widetilde { F } _ { \pi } ^ { p } \left( \oplus _ { t = 0 } ^ { H - 1 } \delta _ { t } \right) = \operatorname* { s u p } _ { y } \left\{ y \in \mathbb { R } \mid \mathbb { P } \left[ F _ { \pi } \left( \oplus _ { t = 0 } ^ { H - 1 } \left( \delta _ { t } + \Delta _ { t } \right) \right) \leq y \right] \leq p \right\} } \end{array}$   
Percentile lower bound:

the $p$ -th percentile of $J _ { \varepsilon } \left( \pi ^ { \prime } \right) \geq \widetilde { F } _ { \pi } ^ { p ^ { \prime } } \left( \oplus _ { t = 0 } ^ { H - 1 } \mathbf { 0 } \right)$ where $p ^ { \prime } : = \Phi ( \Phi ^ { - 1 } ( p ) - \varepsilon \sqrt { H } / \sigma )$

# CROP-LoRe: Local smoothing $^ +$ adaptive search

Sequenceofertfieradii (rl)

![](/data/huangyc/Document2All/posterDataOutput_vlm/CROP: Certifying Robust Policies for Reinforcement Learning through Functional Smoothing_poster/auto/images/images/fig_2.jpg)

$r _ { t } ^ { k }$ when $\varepsilon < r _ { t } ^ { k }$ ,the possible action willbe among the set of top $k$ actions

$$
r _ { t } ^ { k } = \frac { \sigma } { 2 } \left( \Phi ^ { - 1 } \left( \frac { \widetilde { Q } ^ { \pi } \left( s _ { t } , a _ { 1 } \right) - V _ { \operatorname* { m i n } } } { V _ { \operatorname* { m a x } } - V _ { \operatorname* { m i n } } } \right) - \Phi ^ { - 1 } \left( \frac { \widetilde { Q } ^ { \pi } \left( s _ { t } , a _ { k + 1 } \right) - V _ { \operatorname* { m i n } } } { V _ { \operatorname* { m a x } } - V _ { \operatorname* { m i n } } } \right) \right) , \quad 1 \leq k < \vert A \vert
$$

Adaptive search algorithm

Base case: $\varepsilon = 0$ ，   
$\_$ :reward without perturbation Adaptive search:   
alternating the two procedures:

![](/data/huangyc/Document2All/posterDataOutput_vlm/CROP: Certifying Robust Policies for Reinforcement Learning through Functional Smoothing_poster/auto/images/images/fig_3.jpg)

1.Trajectory exploration and expansion: obtain the lower bound $\underline { { J } } _ { \varepsilon }$ forε (DFS)

2. Perturbation magnitude growth: obtain a new $\varepsilon ^ { \prime }$ (priority queue)

· Outcome ofthe algorithm: $\left\{ \left( \varepsilon _ { i } , \underline { { J } } _ { \varepsilon _ { i } } \right) \right\} _ { i = 1 } ^ { | C | }$

# Experiments

# Setup

Four RL environments: Freeway,Pong,CartPole,Highway Nine DQN variants: StdTrain, GaussAug, AdvTrain,SA-MDP (PGD,CVX), RadialRL,CARRL,NoisyNet, GradDQN Two certification criteria: per state-action, cumulative reward Three certification algorithms: CROP-LoAct, CROP-GRe,CROP-LoRe

![](/data/huangyc/Document2All/posterDataOutput_vlm/CROP: Certifying Robust Policies for Reinforcement Learning through Functional Smoothing_poster/auto/images/images/fig_4.jpg)  
Robustness Certification for Per-State Action   
Fig.Robustness certification for per-stateaction in termsof certified radiusrat all time steps.

GradDQN and RadialRLachieve the highest certified radius on Freeway.   
Periodic patterns can be observed in Pong.   
Certified results largely match empirical observations.

# Robustness Certification for Cumulative Reward

![](/data/huangyc/Document2All/posterDataOutput_vlm/CROP: Certifying Robust Policies for Reinforcement Learning through Functional Smoothing_poster/auto/images/images/fig_5.jpg)  
Fig.RobustnesscertificationforcumulativerewardonFreewayincludingexpectationoundJE,percentileboundJp andabsolute lower bound J.

Under global smoothing,percentile bound is tighter than expectation bound. For CROP-LoRe,diferent RLalgorithms demonstrate different behavior in different regions of attackmagnitudeε---GradDQN achieves higher lower bound under smaller ε,while RadialRL is the dominant one under larger $\varepsilon$ The certification is relatively tight, compared with theempirical result. More details,experimental results,and codecan be found inour paper,leaderboard, and repository!