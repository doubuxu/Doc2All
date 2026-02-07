# Spatial Graph Attention and Curiosity-driven Policy for Antiviral Drug Discovery

Yulun Wu (yulun_wu@berkeley.edu)tS, Mikaela Cashmanls,Nicholas Choma#,Erica T.Prateslls, Verónica Melesse Vergaral,Andrew Chent\$,Manesh Shah',Austin Clydett,Thomas S.Brettin+, WibeA.de Jong#\$,Neeraj Kumarsss,Martha S.Head \$,Rick L.Stevenstt#,Peter Nugent‡, Daniel A.Jacobsonlls,JamesB.Brownt#s

# Overview

# Reward from Protein-Ligand Structural Information

# Experiments

Disilled Graph Attention Policy Network (DGAPN) is a reinforcement learning model for generating novel graph-structured chemical representations that optimize user-defined objectives by efficiently navigating a constrained domain

The framework is examined on the task of generating molecules that are designed to bind,noncovalently,to functional sites of a SARS-CoV-2 protein.

# Our proposed method:

uses state-of-the-art policy gradient reinforcement learning framework   
defines fragment-interchanging-based action space that is chemically reasonable   
embeds both atom and bond atributes as well as spatial structures by leveraging self-attention   
incorporates an efficient surrogate approach that proposes curiosity bonus to enhance exploration   
is parallelized in various fashions to fit specific needs

# Distilled Graph Attention Policy Network

![](/data/huangyc/Document2All/posterDataOutput_vlm/Spatial Graph Attention and Curiosity-driven Policy for Antiviral Drug Discovery_poster/auto/images/images/fig_1.jpg)  
Overview of DGAPN during a single step of the generating process

The generating process is framed as a Markov decision problem. In a single step, the CReM environment proposes candidates that are reasonable evolutions for the current molecular state; the current state and candidates are encoded into hidden graph representations by a shared Spatial Graph Attention (sGAT) network, then encoded into vector representations by two separate networks; a retrieval system attention mechanism is applied to predict the selection probability of each candidate;a candidate is sampled as the next state and its curiosity score is evaluated by random network distillation [1] as part of the reward; if stopping criteria are met,the main objective is evaluated and added to the reward.After a certain number of steps and rewards are recorded, the network is updated by the proximal policy gradient [2] technique.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Spatial Graph Attention and Curiosity-driven Policy for Antiviral Drug Discovery_poster/auto/images/images/fig_2.jpg)

The main reward of a generated ligand is its binding afinity estimate against the catalytic site of SARS-CoV-2 protein NSP15,predicted by molecular docking.

# Experiments

# Single-objective optimization

The negative docking score is used as the main reward $r _ { m }$ and assign it to the final state $s _ { T }$ as the single objective.

Table1:Primary objective and other summary metrics in evaluations   

<table><tr><td></td><td colspan="4">Dock Score</td><td colspan="5"></td></tr><tr><td></td><td>mean</td><td>1st</td><td>2nd</td><td>3rd</td><td>Validity</td><td>Diversity</td><td>QED</td><td>SA</td><td>FCD</td></tr><tr><td>REINVENT</td><td>-5.6</td><td>-10.22</td><td>-9.76</td><td>-9.50</td><td>95%</td><td>0.88</td><td>0.57</td><td>7.80</td><td>7e-3</td></tr><tr><td>JTVAE</td><td>-5.6</td><td>-8.56</td><td>-8.39</td><td>-8.39</td><td>100%</td><td>0.86</td><td>0.70</td><td>3.34</td><td>2e-1</td></tr><tr><td>GCPN</td><td>-5.0</td><td>-9.19</td><td>-7.93</td><td>-7.54</td><td>100%</td><td>0.91</td><td>0.44</td><td>5.48</td><td>8e-4</td></tr><tr><td>MolDQN</td><td>-7.5</td><td>-10.59</td><td>-10.42</td><td>-10.17</td><td>100%</td><td>0.87</td><td>0.17</td><td>5.01</td><td>3e-3</td></tr><tr><td>MARS</td><td>-6.2</td><td>-10.29</td><td>-9.98</td><td>-9.88</td><td>100%</td><td>0.88</td><td>0.27</td><td>3.65</td><td>4e-2</td></tr><tr><td>DGAPN</td><td>-8.3</td><td>-12.22</td><td>-12.11</td><td>-11.62</td><td>100%</td><td>0.86</td><td>0.14 </td><td>3.19</td><td>6e-3</td></tr></table>

DGAPN managed to generate molecules with improved docking scores compared to state-of-the-art models

![](/data/huangyc/Document2All/posterDataOutput_vlm/Spatial Graph Attention and Curiosity-driven Policy for Antiviral Drug Discovery_poster/auto/images/images/fig_3.jpg)  
Ablation studies   
Figure 3:Loss in supervised learning with and without spatial convolution

<table><tr><td></td><td colspan="3">Dock Score</td><td></td><td></td><td></td></tr><tr><td></td><td>mean</td><td>1st</td><td>2nd</td><td>Diversity</td><td>QED</td><td>SA</td></tr><tr><td>GAPN</td><td>-8.1</td><td>-11.37</td><td>-11.33</td><td>0.83</td><td>0.20</td><td>3.12</td></tr><tr><td>DGAPN</td><td>-8.3</td><td>-12.22</td><td>-12.11</td><td>0.86</td><td>0.14</td><td>3.19</td></tr><tr><td>CReM Greedy</td><td>-8.8</td><td>-10.60</td><td>-10.50</td><td>0.85</td><td>0.28</td><td>2.99</td></tr><tr><td>DGAPN eval</td><td>-9.3</td><td>-13.89</td><td>-13.33</td><td>0.84</td><td>0.26</td><td>3.44</td></tr></table>

lable2:Dock scores and other metrics under different raining and evaluation settings

# Constrained optimization

In lead optimization problems in drug discovery and material science,itcan be useful to require the generated molecule to maintain a certain level of similarity to its starting molecule.

$$
r _ { m ^ { \prime } } ( s _ { T } ) = r _ { m } ( s _ { T } ) - \lambda \cdot \operatorname* { m a x } \{ 0 , \delta - S I M \{ s _ { 0 } , s _ { T } \} \}
$$

The three best performing models in single-objective optimization are compared.

Table 3: Objective improvements and molecule similarities under different constraining coeficients   

<table><tr><td></td><td colspan="2">MolDQN</td><td colspan="2">MARS</td><td colspan="2">DGAPN</td></tr><tr><td>8</td><td>Improvement</td><td>Similarity</td><td>Improvement</td><td>Similarity</td><td>Improvement</td><td>Similarity</td></tr><tr><td>0</td><td>2.24±0.94</td><td>0.22 ±0.06</td><td>0.98±1.50</td><td>0.15±0.05</td><td>2.79±1.60</td><td>0.27±0.18</td></tr><tr><td>0.2</td><td>1.95±0.92</td><td>0.25±0.06</td><td>0.25±1.55</td><td>0.16±0.07</td><td>2.06±1.23</td><td>0.32±0.16</td></tr><tr><td>0.4</td><td>1.04±0.90</td><td>0.40±0.09</td><td>0.08±1.42</td><td>0.17±0.09</td><td>1.17± 0.82</td><td>0.43±0.25</td></tr><tr><td>0.6</td><td>0.55±0.78</td><td>0.61 ± 0.11</td><td>0.06±1.53</td><td>0.19±0.09</td><td>0.58±0.60</td><td>0.67±0.24</td></tr></table>

# Multi-objective optimization

The docking reward is weighted with a formula including QED[3] and SA[4].

$$
r _ { m ^ { \prime } } ( s _ { T } ) = \omega \cdot r _ { m } ( s _ { T } ) + ( 1 - \omega ) \cdot \mu _ { 1 } \cdot \left. Q E D ( s _ { T } ) + \left( 1 - \frac { S A \{ s _ { T } ) - 1 }  { \mu _ { 2 } } \right) \right.
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Spatial Graph Attention and Curiosity-driven Policy for Antiviral Drug Discovery_poster/auto/images/images/fig_4.jpg)  
Figure4: Summary of the molecules obtained under different settings of weight $\omega$ Left and middle plots are QED and SA vs. dock rewards of each 1,00O molecules generated by DGAPN.Right plot shows the top 3 molecules with the highest objective scores generated under each seting of w.

The balancing between the main objective and realism metrics is investigated to generate promising chemicals in practice with room for hit optimization

# Conclusions

Our framework advances the state-of-the-art algorithms in the optimization of molecules with antiviral potential while maintaining reasonable synthetic accessibility. Avaluable extension of ourwork would be to focus on lead-optimization— the refinement of molecular fragmentsalready known to bind the protein of interest through position-constrained modification.

# References

Burda,Yuri，etal."Explorationbyrandomnetworkdistilation."arXivpreprintarXiv:1810.12894(2018).   
Schulman,John,etal."Proximalpolicyoptimizationalgorithms."arXivpreprintarXiv:1707.06347(2017).   
Bickerton,G.Richard,etal."Quantifying thechemicalbeautyofdrugs."Naturechemistry4.2(2012):90-98.   
ErtPetendAarfe"stimationfsteticcesslioeofugieoeulessdolular complexityand fragment contributions."Journal of cheminformatics1.1(20o9):1-11.