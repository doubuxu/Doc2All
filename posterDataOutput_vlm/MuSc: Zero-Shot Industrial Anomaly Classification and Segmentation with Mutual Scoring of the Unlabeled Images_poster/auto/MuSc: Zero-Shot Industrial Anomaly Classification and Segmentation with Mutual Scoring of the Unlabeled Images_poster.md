# MuSc: Zero-Shot Industrial Anomaly Classification and Segmentation with Mutual Scoring of the Unlabeled Images

Xurui Li1\*, Ziming Huang1,\*, Feng Xue³， Yu Zhou1,2

H {xrli_plus,zmhuang，yuzhou}@hust.edu.cn},feng.xue@unitn.it

# Motivation

# Framework

# LNAMD

A rich amount of normal information implicit in unlabeled test images can be exploited for anomaly detection.

MVTecADdataset   
2.74%   
97.26%   
VisAdataset   
0.55%   
99.45%   
normal pixelsabnormal pixels

A discriminative characteristic: the normal image patches could find a relatively large number of similar patches in other unlabeled images, while the abnormal ones only have a few similar patches.

![](/data/huangyc/Document2All/posterDataOutput_vlm/MuSc: Zero-Shot Industrial Anomaly Classification and Segmentation with Mutual Scoring of the Unlabeled Images_poster/auto/images/images/fig_1.jpg)

# Contributions

The first method that only uses the unlabeled test images for industrial anomaly detection. We reveal the potential capability of normal and abnormal patches contained in unlabeled images. $2 1 . 1 \%$ PRO gains and $2 1 . 9 \%$ seg-AP gains on MVTec AD and $1 9 . 4 \%$ seg-AP gains on VisA.

![](/data/huangyc/Document2All/posterDataOutput_vlm/MuSc: Zero-Shot Industrial Anomaly Classification and Segmentation with Mutual Scoring of the Unlabeled Images_poster/auto/images/images/fig_2.jpg)

# Mutual Scoring Mechanism

Image $I _ { j }$ assigns a score to each aggregated patch token of image $I _ { i }$

$$
\begin{array} { r } { a _ { i , l } ^ { m , r } ( I _ { j } ) = \operatorname* { m i n } _ { n } \| \hat { p } _ { i , l } ^ { m , r } - \hat { p } _ { j , l } ^ { n , r } \| _ { 2 } } \end{array}
$$

Interval Average (minimum $30 \%$ ）$\overline { { a } } _ { i , l } ^ { m , r } = \frac { 1 } { K } \sum _ { k \in \left[ 1 , K \right] } a _ { i , l } ^ { m , r } ( \overline { { I } } _ { k } )$

Neighborhood range $1 \times 1 \ 3 \times 3 \ 5 \times 5$

Aggregate function: Adaptive average pooling

35 normal 7 normal 30 abnormal 6 abnormal   
25 overlap 5 overlap 20 4 15 3 10 2 5 1 0 0 0.0 anomaly scoresofallnormalpatches 1.000 anomalyscoresofallabnormalpatches 1.0 201e2 20.1e2   
15 15 10 10 5 0 0 0.0 wholevalueinterlavege 1.00.0 theminimum30%valuenteralaverage 1.0

Multi-degree aggregation To segment abnormal regions of varying sizes.

![](/data/huangyc/Document2All/posterDataOutput_vlm/MuSc: Zero-Shot Industrial Anomaly Classification and Segmentation with Mutual Scoring of the Unlabeled Images_poster/auto/images/images/fig_3.jpg)

Mean:

$r$ and $l$

$$
\pmb { a } _ { i } ^ { m } = \frac { 1 } { L } \sum _ { l \in \{ 1 , . . . , L \} } \frac { 1 } { 3 } \sum _ { r \in \{ 1 , 3 , 5 \} } \overline { { { a } } } _ { i , l } ^ { m , r }
$$

# Experiments

# RsCIN

# Comparison with O-shot methods

<table><tr><td rowspan=1 colspan=1>Methods</td><td rowspan=1 colspan=1>WinCLIPli</td><td rowspan=1 colspan=1>APRIL-GANI2I</td><td rowspan=1 colspan=1>ACRI31</td><td rowspan=1 colspan=1>MuSc(ours)</td></tr><tr><td rowspan=1 colspan=2></td><td rowspan=1 colspan=3>MVTec ADDataset</td></tr><tr><td rowspan=1 colspan=1>cls-AUROC</td><td rowspan=1 colspan=1>91.8</td><td rowspan=1 colspan=1>86.1</td><td rowspan=1 colspan=1>85.8</td><td rowspan=1 colspan=1>97.8(+6.0)</td></tr><tr><td rowspan=1 colspan=1>PRO</td><td rowspan=1 colspan=1>64.6</td><td rowspan=1 colspan=1>44.0</td><td rowspan=1 colspan=1>72.7</td><td rowspan=1 colspan=1>93.8(+12.4)</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VisA Dataset</td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>cls-AUROC</td><td rowspan=1 colspan=1>78.1</td><td rowspan=1 colspan=1>78.0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>92.8(+10.7)</td></tr><tr><td rowspan=1 colspan=1>PRO</td><td rowspan=1 colspan=1>56.8</td><td rowspan=1 colspan=1>86.8</td><td rowspan=1 colspan=1>=</td><td rowspan=1 colspan=1>92.7(+5.7)</td></tr></table>

No training No prompt

# Comparison with 4-shot methods

Image GT GAN(0) APRIL- · 言 (redundancy)

Image-level feature $\mathcal { F } _ { i }$ Extracted by ViT

Similarity matrix $W _ { i , j } = \mathcal { F } _ { i } \cdot \mathcal { F } _ { j }$

Multi-window Mask

$$
M _ { k } ( i , j ) = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f } I _ { j } \in \mathcal { N } _ { k } ( I _ { i } ) } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. \ k \in \{ k _ { 1 } , k _ { 2 } \}
$$

$$
\begin{array} { r l } & { D ( i , i ) \ = \ \sum _ { j = 1 } ^ { N } M _ { k } \odot W ( i , j ) } \\ & { \hat { \mathbf { C } } = ( \ \sum _ { M _ { k } \in \overline { { M } } } ( D ^ { - 1 } ( M _ { k } \odot W ) \mathbf { C } ) + \mathbf { C } ) / ( K + 1 ) } \\ & { \qquad M _ { k } \in \overline { { M } } } \end{array}
$$

# References

<table><tr><td rowspan=1 colspan=1>Methods</td><td rowspan=1 colspan=1>PatchCorel4l</td><td rowspan=1 colspan=1>WinCLIPI</td><td rowspan=1 colspan=1>APRIL-GANI2I</td><td rowspan=1 colspan=1>MuSc(ours)</td></tr><tr><td rowspan=1 colspan=5>MVTec ADDataset</td></tr><tr><td rowspan=1 colspan=1>cls-AUROC</td><td rowspan=1 colspan=1>88.8</td><td rowspan=1 colspan=1>95.2</td><td rowspan=1 colspan=1>92.8</td><td rowspan=1 colspan=1> 97.8(+2.6)</td></tr><tr><td rowspan=1 colspan=1>PRO</td><td rowspan=1 colspan=1>84.3</td><td rowspan=1 colspan=1>89.0</td><td rowspan=1 colspan=1>91.8</td><td rowspan=1 colspan=1>93.8(+2.0)</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VisA Dataset</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>cls-AUROC</td><td rowspan=1 colspan=1>85.3</td><td rowspan=1 colspan=1>87.3</td><td rowspan=1 colspan=1>92.6</td><td rowspan=1 colspan=1>92.8(+0.2)</td></tr><tr><td rowspan=1 colspan=1>PRO</td><td rowspan=1 colspan=1>84.9</td><td rowspan=1 colspan=1>87.6</td><td rowspan=1 colspan=1>90.2</td><td rowspan=1 colspan=1> 92.7(+2.5)</td></tr></table>

Optimize score Ci of Ii Optimized score i k2 G 1 Ci Wi,jCj 3 j=1 Weighted average of scores within   
$\begin{array} { l } { | } \\ { | } \end{array}$ the window mask   
$\begin{array} { r } { \mathbf { \ i } _ { \overline { { w } } _ { i , j } } ^ { \mathsf { I } } = \left\{ \begin{array} { r } { \hat { w } _ { i , j } ^ { k _ { 1 } } + \hat { w } _ { i , j } ^ { k _ { 2 } } , \quad \mathrm { ~ i f ~ } 0 < j \leq k _ { 1 } } \\ { \hat { w } _ { i , j } ^ { k _ { 2 } } , \quad \mathrm { i f ~ } k _ { 1 } < j \leq k _ { 2 } } \end{array} \right. \mathbf { \mathsf { I } } } \\ { \mathbf { \ell } _ { 1 } ^ { \mathsf { I } } . } \end{array}$

[1]JeongJ,ZouYKiTtal.ncip:Zero-/fe-shotaomlyssificaiondgmtationC//roing of the IEEE/CVF Conferenceon ComputerVisionand Pattern Recognition.2023:19606-19616.

Jniversal module for other AD methods [2]ChenX，HanYZhangJ.Azero-/few-shotanomalyclasificationandsegmentationmethodforcpr2023 vandworkshopchallenge tracks1&2:1stplaceonzero-shotadand4thplaceonfew-shotad[J].arXivpreprint arXiv:2305.17382，2023.

3]LiA，QiuC，KloftM,etal.Zero-shot anomalydetectionviabatchnormalization[J].AdvancesinNeura nformation Processing Systems,2024,36.

[4]RothK，PemulaL,ZepedaJetal.Towardstotalrecallinindustrialnomalyetection[C]/Proceedingsofthe IEEE/CVFConferenceonComputerVisionandPatternRecognition.2022:14318-14328.

# Detect various types of defects