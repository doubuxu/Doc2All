# G²N² :Weisfeiler and Lehman go grammatical

![](/data/huangyc/Document2All/posterDataOutput_vlm/G$^2$N$^2$ : Weisfeiler and Lehman go grammatical_poster/auto/images/images/fig_1.jpg)

Jason Piquenot,Aldo Moscatell,Maxime Bérar,Pierre Héroux,Jean-Yves Ramel,Romain Raveaux,SebastienAdam LITIS Lab, University of Rouen Normandy，France,LIFAT Lab,University of Tours,France

![](/data/huangyc/Document2All/posterDataOutput_vlm/G$^2$N$^2$ : Weisfeiler and Lehman go grammatical_poster/auto/images/images/fig_2.jpg)

# Contributions

•A generic framework to design a GNN from any fragment of an algebraic language. The instantiation of the framework on $\mathrm { M L } \left( \mathcal { L } _ { 3 } \right)$ resulting in $\mathsf { G } ^ { 2 } \mathsf { N } ^ { 2 }$ , a provably 3-WL GNN. Experiments demonstrating that $\mathsf { G } ^ { 2 } \mathsf { N } ^ { 2 }$ outperforms existing 3-WL GNNs on various downstream tasks.

# MATLANG and WL

Definition 1:MATLANG is a matrix language with operation set $\{ + , \cdot , \odot ;$ T ${ \mathrm { T r } } , { \mathrm { d i a g } } , 1 , \times , f { \big \} }$ Restricting operations toa subset $\mathcal { L }$ definesa fragment of MATLANG ML $( \mathcal { L } )$ $s ( X ) \in \mathbb { R }$ isa sentence in $\operatorname { M L } \left( \mathcal { L } \right)$ if it consists of consistent consecutive operations in $\mathcal { L }$ ，operatingonamatrix $X$ resultingina scalarvalue. In termsof separative power, $\mathrm { M L } \left( \mathcal { L } _ { 3 } \right) \sim 3 \ – \mathsf { W L }$ with $\mathcal { L } _ { 3 } = \{ \cdot , \mathrm { ~ \bf ~ ^ { T } ~ } , 1 , \mathrm { d i a g } , \odot \}$ Ex: $s ( X ) = 1 ^ { \mathbf { T } } \left( X ^ { 2 } \odot \mathrm { d i a g } \left( 1 \right) \right) 1 = \mathrm { T r } ( X ^ { 2 } ) \in \mathrm { M L } \left( \mathcal { L } _ { 3 } \right)$

# Context-Free Grammar

Definition 2: A Context-Free Grammar (CFG) $G = ( V , \Sigma , R , S )$ with $V$ a finite set of variables, $\Sigma$ a finite set of terminal symbols, $R$ a finite set of rules $V \to ( V \cup \Sigma ) ^ { * }$ ， $S$ astartvariable.

# Framework

Language Step1 8 ExharGtive 8 Redued GNN Definition Reduction Translation

From ML(C3) to the 3-WL G²N²

# Step 1: 3-WL exhaustive CFG

# Step 2: 3-WL reduced CFG

Theorem1:For $G _ { \mathcal { L } _ { 3 } }$ definedas follow we have $L ( G _ { \mathcal { L } _ { 3 } } ) = \mathrm { M L } \left( \mathcal { L } _ { 3 } \right)$

·Theorem 2:The following CFG denoted $\mathsf { r } { - } G _ { \mathcal { L } _ { 3 } }$ isas expressive as 3-WL.

$S \to ( V _ { r } ) ( V _ { c } ) \mid \mathrm { d i a g } \left( S \right) \mid S S \mid ( S \odot S )$ $V _ { c } \to ( V _ { c } \odot V _ { c } ) \mid M V _ { c } \mid ( V _ { r } ) ^ { \mathbf { T } } \mid V _ { c } S \mid 1$ $V _ { r } \to ( V _ { r } \odot V _ { r } ) \mid V _ { r } M \mid ( V _ { c } ) ^ { \mathbf { T } } \mid S V _ { r }$ $M  ( M \odot M ) \mid M M \mid ( M ) ^ { \mathbf { T } } \mid \mathrm { d i a g } ( V _ { c } ) \mid ( V _ { c } ) ( V _ { r } ) \mid A$

$$
\begin{array} { l } { { V _ { c } \to M V _ { c } \mid 1 } } \\ { { M \to ( M \odot M ) \mid M M \mid \mathrm { d i a g } ( V _ { c } ) \mid A } } \end{array} \qquad 
$$

$V _ { c }$ variable maintains expressivenessat a set depth.

Edge features Matrix E readout Decision L Vector layer JILPG readout H G²N2 layers function Node features

# Overview of G²N2

# Step 3: Parallelised rules generation in r- $G _ { \mathcal { L } _ { 3 } }$

# Regression task: QM9 dataset (MAE ↓)

<table><tr><td>Target PPGN</td><td>G²N</td><td>PPGN</td><td>G²N²</td></tr><tr><td>μ</td><td>0.0934</td><td>0.0703</td><td>0.231 0.102</td></tr><tr><td>α</td><td>0.318</td><td>0.127</td><td>0.382 0.196</td></tr><tr><td>Chomo</td><td>0.00174</td><td>0.00172</td><td>0.00276 0.0021</td></tr><tr><td>Elumo</td><td>0.0021</td><td>0.00153</td><td>0.00287 0.00211</td></tr><tr><td>△</td><td>0.0029</td><td>0.00253</td><td>0.0029 0.00287</td></tr><tr><td>R²</td><td>3.78</td><td>0.342</td><td>16.07 1.19</td></tr><tr><td>ZPVE</td><td>0.0003990.0000951</td><td></td><td>0.00064 0.0000151</td></tr><tr><td>U0</td><td>0.022</td><td>0.0169</td><td>0.234 0.0502</td></tr><tr><td>U</td><td>0.0504</td><td>0.0162</td><td>0.234 0.0503</td></tr><tr><td>H</td><td>0.0294</td><td>0.0176</td><td>0.229 0.0503</td></tr><tr><td>G</td><td>0.024</td><td>0.0214</td><td>0.238 0.0504</td></tr><tr><td>C</td><td>0.144</td><td>0.0429</td><td>0.184 0.0707</td></tr><tr><td>ep</td><td>129 s 98s</td><td>131s</td><td>57s</td></tr></table>

# Classification task: TUD dataset (ACC ↑)

![](/data/huangyc/Document2All/posterDataOutput_vlm/G$^2$N$^2$ : Weisfeiler and Lehman go grammatical_poster/auto/images/images/fig_3.jpg)

Variables: $S$ scalar, $V _ { c } / V _ { r }$ column/row vector,M matrix.

·GCN:

·2-IGN:

Vc →CVc|1

M1→M2O|M2OJ| (M2)To JM2→JM1|M1J|JM1J|A

# PPGN:

M → MM | diag(1) | A

Itcration k-1 Iteration k Iteration k +1 (4) Output storage (1) Rule selection (2) Inputs selection (3)Rulc computation (4) Output storage (1) Rule selection MOM AoA MM MM MM or A2 or diag(Ve) AOA² diag(Ve) Mtri emoryVecto mry Aatri memoryVecto merary Matrix memory Vector memory MVe   
s L1 b. s L2 b. s(+1) s() L MLPM C(l+1) s() b。 L4 s bMve L5   
H() f L6 L bdiag bMVe diag MLPV H(l+1)

<table><tr><td rowspan=1 colspan=2>DatasetG²N²   rank Best GNNcompetitor</td></tr><tr><td rowspan=1 colspan=2>MUTAG92.5±5.51（1）92.2±7.5</td></tr><tr><td rowspan=1 colspan=2>PTC   72.3±6.31（1）68.2±7.2</td></tr><tr><td rowspan=1 colspan=2>Proteins80.1±3.71（1)77.4±4.9</td></tr><tr><td rowspan=1 colspan=1>NCI1   82.8±0.95（3）</td><td rowspan=1 colspan=1>83.5±2.0</td></tr><tr><td rowspan=1 colspan=1>IMDB-B76.8±2.83（3</td><td rowspan=1 colspan=1>77.8±3.3</td></tr><tr><td rowspan=1 colspan=1>IMDB-M54.0±2.92（2)</td><td rowspan=1 colspan=1>54.3±3.3</td></tr></table>

# Acknowledgments

Theauthorsacknowledge the support of the French Agence Nationalede la Recherche (ANR) undergrant ANR-21-CE23-0025(CoDeGNN project).Theauthorsacknowledge the support oftheANRandtheRégion Normandieunder grant ANR-20-THIA-0021 (HAISCoDe project).