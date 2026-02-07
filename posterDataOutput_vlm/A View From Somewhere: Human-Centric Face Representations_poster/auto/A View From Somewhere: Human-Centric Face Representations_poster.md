# A View From Somewhere: Human-Centric Face Representations

Jerone T.A.Andrews1,Przemys law Joniak²,Alice Xiang3 1Sony Al, Tokyo2University of Tokyo,Tokyo3SonyAl,New York

jerone.andrews@sony.com

# Sony Al

# Motivation

# Contributions

# Results

# Dataset Bias

Dataset bias can result in models thatare discriminatory or depend on spurious correlations. Forinstance,aface image restorationmodel may“hallucinate"features correlated with oversampled subgroups,resulting intheerasureof minoritygroups.

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_1.jpg)  
Originalimagesare taken fromtheChicago Face Database (https://www.chicagofaces.org)

Priortolearning,human-centricimagedataset users should evaluate thediversityof thedata

# Parity and Diversity

Thecanonicalapproach isto categorizepeopleusingdemographic labels. However,evaluating diversity by examining counts across subgroupsfails to reflect thecontinuous natureof human phenotypicdiversity (e.g.,skin tone isoftenreduced tolightvs.dark).Moreover,such approaches often deny multi-groupmembership (e.g.,erasingmulti-ethnic individuals).

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_2.jpg)

# Unknown Label Distributions

Mosthuman-centricimage datasetsareweb-scraped,lacking ground-truth informationabout theimage subjects.Therefore,researchers typicallychoose certain attributes they consider to berelevantfor humandiversityandusehumanannotatorstoinfer them.This isdifficult for ill-definedand highlychangeablesocial constructssuchas raceand gender.Observational labelsrisk not only encoding stereotypes,butreifyingand propagating thembeyond“their culturalcontext”.Furthermore,discrepanciesbetweenobservedandself-identifiedattributes can invalidatean image subject'sself-image and identity.

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_3.jpg)

Motivated by issues inherentto categorical labels,weaim todevelopa toolthat canevaluate thevisual diversity offaces in unlabeled datasets.Wedoso without everaskinganannotator to explicitly categorizea person.

# Face Similarity (FAX) Dataset

Weintroduceanoveldataset,FAX,containing 638,18oodd-one-outface similarityjudgments over4,921faces (stimulusset).Judgments correspond to the odd-one-out (i.e.,least similar) faceina triplet,andareassociatedwiththeidentifieranddemographicattributesof the annotatorwho made the judgment.

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_4.jpg)

{annotator_id’：‘hXs6iz'，‘age’：37,‘gender-id’：‘female’，‘nationality'： brazilian',‘regional_ancestry':‘europe',‘subregional_ancestry':‘west_europe'}

# Model of Conditional Decision-Making

Weintroduceamodel that learns to predict human judgments of face similarity conditioned on theannotatorwho generated the judgment.The conditionsare realized using annotator masks.

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_5.jpg)

Afacecan exhibit certain characteristics toa greater or lesser extent than others,even within thesamesubpopulation.Therefore,weconstrainourmodelto learn faceembeddingsthatare continuous,non-negative (human-interpretable),and sparse byminimizing:

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_6.jpg)

where ${ \hat { p } } ( k \mid a )$ isthepredictedprobabilitythatface ${ \bf x } _ { k }$ is the odd-one-out according to annotator $^ { a }$ .

# Interpretability

From learning on FAX,we note thematerialization of distinct dimensions coinciding with commonlydefineddemographic subgroups,i.e.,Male,Female,Black,White,East Asian, SouthAsian,and Elderly.Inaddition,separate dimensionssurfacefor faceand hair morphology,i.e.,Wide Face,Long Face,Smiling Expression,Neutral Expression, Balding,Facial Hair,and Dyed Hair.

![](/data/huangyc/Document2All/posterDataOutput_vlm/A View From Somewhere: Human-Centric Face Representations_poster/auto/images/images/fig_7.jpg)  
Originalimagesare taken fromFFHQ(https://github.com/NVlabs/ffhq-dataset）

Moreover,we validate thatFAX dimensions can be used to directly collect continuousattribute valuesfornovel faces,sidestepping the limitsofcategorical definitions.

Predicting Novel Similarity Judgments   

<table><tr><td>Model</td><td>Loss/Method</td><td>Acc.</td><td>r</td></tr><tr><td>FairFace</td><td>Cross-entropy</td><td>51.9</td><td>0.67</td></tr><tr><td>CelebA</td><td>Cross-entropy</td><td>48.9</td><td>0.56</td></tr><tr><td>FFHQ</td><td>Cross-entropy</td><td>51.8</td><td>0.68</td></tr><tr><td>CASIA-WebFace</td><td>ArcFace</td><td>46.1</td><td>0.40</td></tr><tr><td>FAX-C</td><td>Conditional</td><td>61.7</td><td>0.82</td></tr><tr><td>FAX-U</td><td>Unconditional</td><td>57.5</td><td>0.86</td></tr><tr><td>FAX-Triplet</td><td>Tripletmarginwith distance swap</td><td>52.8</td><td>0.64</td></tr></table>

From56images，wegenerate $\binom { 5 6 } { 3 }$ possible tripletswith 2-3 unique judgmentsper triplet(8o,3oojudgments).

Wereportodd-one-outpredictiveaccuracy;and,Spearman's between the strictlyupper triangularmodel-and humangeneratedsimilaritymatrices.Entry(i,j）inthehumangeneratedsimilaritymatrixcorrespondstothefractionoftriplets containing（i,j)，whereneitherwasjudgedastheodd-one-out. Entry(i,j)inamodel-generated similaritymatrixcorrespondsto themeanρ(k)over alltriplets containing $( i , j )$

Annotator Bias   

<table><tr><td>Annotatorattribute</td><td>Groups</td><td>#Masks</td><td>AUROC</td></tr><tr><td>Agegroup</td><td>30-39/40-49</td><td>393/121</td><td>0.59±0.05</td></tr><tr><td>Gender identity</td><td>Male/Female</td><td>523/473</td><td>0.65±0.05</td></tr><tr><td>Nationality</td><td>America/India</td><td>530/204</td><td>0.86±0.03</td></tr><tr><td>Regional ancestry</td><td>Europe/Asia</td><td>407/243</td><td>0.86±0.03</td></tr><tr><td></td><td>Subregional ancestry West Europe/South Asia 173/107</td><td></td><td>0.88±0.05</td></tr></table>

Using1o-foldcrossvalidation,wetrainlinearSVMs todiscriminatebetweenannotatormasksfrom two different annotator subgroups.

# Comparative Diversity Auditingand Binary Attribute Classification

Comparativediversityauditing   

<table><tr><td colspan="6">Model (Disparity△/Spearman&#x27;s𝑟r)</td></tr><tr><td></td><td>Data Attribute</td><td>FAX</td><td>CelebA</td><td>FairFace</td><td>FFHQ</td></tr><tr><td>CC</td><td>&gt;70y.0.*</td><td>0.22/0.96</td><td>0.06/0.99</td><td>0.06/0.95</td><td>0.08/0.99</td></tr><tr><td>CC</td><td>Male*</td><td>0.06/0.97</td><td>0.02/0.99</td><td>0.02/1.00</td><td>0.04/0.99</td></tr><tr><td>CC</td><td>Light skin</td><td>0.06/0.94</td><td>0.3/0.65</td><td>0.18/0.85</td><td>0.06/0.99</td></tr><tr><td>CFD</td><td>Smiling</td><td>0.12/0.99</td><td>0.06/0.95</td><td></td><td></td></tr><tr><td>CFD</td><td>Male*</td><td>0.00/1.00</td><td>0.08/0.99</td><td>0.02/1.00</td><td>0.02/1.00</td></tr><tr><td>CFD</td><td>EastAsian*</td><td>0.06/1.00</td><td>二</td><td>0.02/0.98</td><td>0.02/1.00</td></tr><tr><td>CFD</td><td>Black*</td><td>0.10/0.98</td><td>一</td><td>0.14/0.97</td><td>0.00/1.00</td></tr><tr><td>CFD</td><td>White*</td><td>0.04/1.00</td><td>0.02/0.99</td><td>0.04/0.97</td><td>0.04/0.99</td></tr><tr><td>CFD</td><td>Indian*</td><td>0.08/1.00</td><td></td><td>0.30/0.73</td><td>0.08/0.87</td></tr></table>

Givenaset of candidate subsets,weaimto findthemostdiverse subset (i.e.,minimal attribute disparity). FAXdimensionsresult intheidentificationofdata subsetswith competitiveattributedisparityscores.Inparticular,Spearman'srevidencesthat FAXdisparityscoresarehighlycorrelatedwiththeground-truthlabel disparity.

Discriminatingbetween binary-valuedattributes   

<table><tr><td></td><td></td><td colspan="4">AUROC</td></tr><tr><td>Data</td><td>Attribute</td><td>FAX</td><td></td><td>CelebAFairFace</td><td>FFHQ</td></tr><tr><td>cc</td><td>&gt; 70y.0.*</td><td>0.800</td><td>0.936</td><td>0.959</td><td>0.962</td></tr><tr><td>FFHQ</td><td>&gt;70y.0.</td><td>0.905</td><td>0.959</td><td>0.971</td><td>0.980</td></tr><tr><td>CFD</td><td>Male*</td><td>0.991</td><td>0.997</td><td>0.996</td><td>0.998</td></tr><tr><td>Cc</td><td>Male*</td><td>0.971</td><td>0.986</td><td>0.990</td><td>0.981</td></tr><tr><td>CA</td><td>Male</td><td>0.990</td><td>0.999</td><td>0.994</td><td>0.995</td></tr><tr><td>COCo</td><td>Male</td><td>0.893</td><td>0.926</td><td>0.963</td><td>0.958</td></tr><tr><td>MIAP</td><td>Male</td><td>0.924</td><td>0.942</td><td>0.945</td><td>0.938</td></tr><tr><td>FFHQ</td><td>Male</td><td>0.933</td><td>0.959</td><td>0.988</td><td>0.996</td></tr><tr><td>CA</td><td>Smiling</td><td>0.895</td><td>0.982</td><td>一</td><td>二</td></tr><tr><td>CFD</td><td>Smiling</td><td>0.969</td><td>0.992</td><td></td><td></td></tr><tr><td>CFD</td><td>Neutral</td><td>0.731</td><td>一</td><td>一</td><td>一</td></tr><tr><td>CFD</td><td>EastAsian*</td><td>0.969</td><td></td><td>0.955</td><td>0.938</td></tr><tr><td>CFD</td><td>Black*</td><td>0.992</td><td></td><td>0.992</td><td>0.988</td></tr><tr><td>CFD</td><td>White*</td><td>0.972</td><td>0.889</td><td>0.990</td><td>0.988</td></tr><tr><td>CFD</td><td>Indian*</td><td>0.960</td><td>二</td><td>0.848</td><td>0.883</td></tr><tr><td>cc</td><td>Light skin</td><td>0.930</td><td>0.830</td><td>0.965</td><td>0.960</td></tr><tr><td>Coco</td><td>Light skin</td><td>0.889</td><td>0.771</td><td>0.927</td><td>0.931</td></tr><tr><td>CA</td><td>Balding</td><td>0.963</td><td>0.995</td><td>二</td><td>二</td></tr></table>

FAXdimensionsarecompetitivewith the baselines,even inchallenging unconstrained settingsas represented by COCOand MIAP.