# Accurate And Scalable Estimation Of Epistemic Uncertainty For Graph Neural Networks

Puja Trivedi1, Mark Heimann2, Rushil Anirudh2, Danai Koutra1 Jayaraman J. Thiagarajan2

# Stochastic Centering: Single Model Ensembles

NTKs for (Graph) Neural Networks are not shift invariant

# The variability over shifts captures epistemic uncertainty!

· Stochastic Centering creates a relative representation for an input, $\pmb { \chi } ,$ in terms of a random anchor, c.

C1 X-C1 Training Manifold X Test sample X-R2 ↑ x-C3 C2 Anchors are drawn at C3 random fromP(X)

·During training, the anchor is randomized, thus implicitly sampling different hypotheses.

· During testing, predictions are computed over multiple anchors.

· Discrepancy across anchors choices captures epistemic uncertainty!

# G △-UQ: Stochastic Centering for GNNs

# We propose G △-UQ, a novel training paradigm for improving calibration with GNNs

Scalable and Lightweight Robust to Distribution Shifts Supports Pretrained Models Easy to Implement

class GNN_ReadOutAnc:definit__(GNN)：self.MPNN1 =MPNN(InputDim,HDim1)self.MPNN2=MPNN(HDim1,HDim2）self.MPNN3=MPNN(HDim2，HDim3）Self.READOUT=READOUTLayer()#Corres.toGDUQLayer!self.classifier=Linear(HDim3\*2,NumClass)def forward（X,Adj)：h=self.MPNN1（X,Adj）h=self.MPNN2(h,Adj）h=self.MPNN3(h,Adj)g=self.READOUT(h,Batch） #OUT:（B，HDim3)C=SHUFFLE（g，dim=0） #（B，HDim3)gAnc=CONCAT（[g-C,C],dim=1)#（B，HDim3x2）pred=self.classifier(gAnc) #Out:(B,NumClass)return pred

G △-UQ is easy to implement, with only a few changes to standard GNNs!

#training  
for(G,y)intrainloader：C=create_anchors(n=  
BatcbSAae)=CONCAT([G-C,C]，dim=1)preds=model(G_Anc)loss=criterion(preds,Y)  
#inference  
anc_preds=[]  
testAncs=create_anchors(n=K)  
forA in testAncs:G_anc=CONCAT（[I-A,A]，dim=1）preds=model(G_anc)anc_preds.append(preds)  
P=CONCAT（anc_preds，dim=0)  
mu=MEAN（P，dim=@）  
var=STDDEV(P，dim=0)

# Improved Node Classification Calibration

# Better Graph Classification Calibration

![](/data/huangyc/Document2All/posterDataOutput_vlm/Accurate and Scalable Estimation of Epistemic Uncertainty for Graph Neural Networks_poster/auto/images/images/fig_1.jpg)  
G △-UQ Improves Calibration of Pretrained GNNs

![](/data/huangyc/Document2All/posterDataOutput_vlm/Accurate and Scalable Estimation of Epistemic Uncertainty for Graph Neural Networks_poster/auto/images/images/fig_2.jpg)  
G△-UQ Estimates are Effective in Safety Critical Tasks

·G △-UQ achieves the best OOD detection AUROC on $5 / 6$ datasets.

· G △-UQ also performs well on the generalization gap prediction tasks.

Node Feature Int.MPNN Readout READOUT/MLP READOUT/MLP $\mathbb { M } \mathbb { P }$ Anchored Inference $[ \mathbf { G } _ { i } - \mathbf { G } _ { c } | | \mathbf { G } _ { c } ]$ GNN.. GN..k. GNN... Stochesi $( \mathbf { A } _ { i } , \mathbf { X } _ { i } )$ $( \mathbf { A } _ { i } , \mathbf { X } _ { i } )$ Calbrteg 1- $\big \{ ( \mathbf { A } _ { c } , \mathbf { X } _ { c } ) \sim \mathbb { D } _ { t r a i n } \big \}$ $( \mathbf { A } _ { c } , \mathbf { X } _ { c } ) \sim \mathbb { D } _ { t r a i n } \}$

· Induce varying levels of stochasticity, trading off hypothesis diversity and the semantic diversity of the anchoring distribution.

We evaluate GΔ-UQwith node feature anchoring on:

· 4 Datasets ·2 Distribution shifts · 8 Post Hoc Calibration

G $\pmb { \triangle }$ -UQmatches or surpasses accuracy and calibration of the vanilla GNN on $8 / 8$ datasets.

· Since graphs are variable sized and discrete, we introduce three anchoring strategies tailored for GNNs.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Accurate and Scalable Estimation of Epistemic Uncertainty for Graph Neural Networks_poster/auto/images/images/fig_3.jpg)  
G △-UQ Improves Graph Classification Calibration with Different MPNNs

Shift: Concept Shift: Covariate   
Accuracy (↑） ECE(↓) Accuracy (↑) ECE（↓)   
Dataset Domain Calibration No G-△UQ G-△UQ No G-△ UQ G△UQ No G-△ UQ G△UQ No G-△ UQ G△ UQ   
X 0.253±0.003 0.281±0.009 0.67±0.061 0.593±0.025 0.122±0.029 0.115±0.041 0.599±0.091 0.525±0.033   
CAGCN 0.253±0.005 0.268±0.008 0.452±0.14 0.473±0.12 0.122±0.018 0.092±0.161 0.355±0.227 0.396±0.161   
Dirichlet 0.229±0.018 0.22±0.022 0.472±0.06 0.472±0.03 0.244±0.105 0.295±0.044 0.299±0.092 0.328±0.044   
ETS 0.253±0.005 0.273±0.012 0.64±0.06 0.575±0.019 0.121±0.021 0.084±0.027 0.539±0.112 0.499±0.027   
WebKB University ±0.029   
Ord G △-UQ $^ +$ Post Hoc. Calib ±0.013 E0.065   
0.056   
achieves: 0.04   
±0.025   
±0.01   
±0.003   
Cora Degree ±0.011   
Best accuracy on 8/8 datasets 0.004   
Ord ±0.027   
±0.004   
±0.005   
±0.019   
±0.035   
Best or2nd bestcalibration ±0.007   
±0.013   
Cora Word on 8/8 datasets 0.037 ±0.004   
Ord ±0.076   
±0.004   
VS 0.607±0.001 0.63±0.002 0.283±0.003 ±0.003 0.603±0.004 .636± 0.261±0.005 0.119±0.003   
X 0.83±0.014 0.829±0.011 0.169±0.013 0.151±0.014 0.703±0.015 0.746±0.027 0.266±0.02 0.169±0.018   
CAGCN 0.83±0.013 0.83±0.013 0.137±0.011 0.143±0.022 0.703±0.019 0.749±0.033 0.25±0.021 0.186±0.017   
Dirichlet 0.801±0.02 0.806±0.008 0.161±0.012 0.17±0.01 0.671±0.018 0.771±0.03 0.241±0.029 0.217±0.017   
ETS 0.83±0.013 0.827±0.014 0.146±0.013 0.164±0.007 0.703±0.019 0.76±0.037 0.28±0.023 0.176±0.019   
CBAS Color GATS 0.83±0.013 0.83±0.021 0.16±0.009 0.173±0.021 0.703±0.019 0.751±0.016 0.236±0.039 0.16±0.015   
IRM 0.829±0.013 0.839±0.015 0.142±0.009 0.133±0.006 0.72±0.019 0.803±0.04 0.207±0.035 0.158±0.017   
Orderinvariant 0.83±0.013 0.803±0.008 0.174±0.006 0.173±0.009 0.703±0.019 0.766±0.045 0.261±0.017 0.194±0.031   
Spline 0.82±0.016 0.824±0.011 0.159±0.009 0.16±0.014 0.683±0.019 0.786±0.038 0.225±0.034 0.179±0.035   
vs 0.829±0.012 0.840±0.011 0.166±0.011 0.146±0.012 0.717±0.019 0.809±0.008 0.242±0.019 0.182±0.014

· G △-UQ is flexible to message passing layer. ·Required level of stochasticity may vary fordataset/GNN.

# Check out the G △-UQ Family!

T