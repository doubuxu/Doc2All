# FLAb: Benchmarking deep learning methods for antibody fitness prediction

# 1 Background

# Antibody therapeutics must have a particular set of fitness properties

a)Expressionb)Thermostabilityc)Immunogenicityd)Bindingafinitye)Aggregationf)Polyreactivity

好   
W

Sixclasses of biophysical data relevanttoantibodydevelopmentare (a) expression,(b) thermostability,(c) immunogenicity,(d) binding affinity,(e) aggregation,and (f)polyreactivity

# Do deep learning methods capture properties of therapeuticantibodies?

We seek toanswer this question by: 1.Creatingacollection of datasets of antibody therapeuticdata 2.BenchmarkrepresentativeAImodellikelihoodsforfitnessprediction

# 2 Dataset curation

# We curated publicly available antibody fitness datasets

Number ofdatapoints   

<table><tr><td></td><td>Antibody</td><td>Exp. （ug/mL）</td><td>Tm (℃)</td><td>Imm. (%ADA)</td><td>Binding (nM)</td><td>Agg. (Wv shift)</td><td>Poly. (min)</td></tr><tr><td></td><td>GSKCA1</td><td>34</td><td>34</td><td>-</td><td>29</td><td>-</td><td>-</td></tr><tr><td>GSKCA2</td><td></td><td>25</td><td>22</td><td></td><td>22</td><td></td><td></td></tr><tr><td></td><td>GSKCA3</td><td>11</td><td>8</td><td></td><td>11</td><td></td><td></td></tr><tr><td></td><td>GSKCA4</td><td>24</td><td>24</td><td></td><td>19</td><td></td><td></td></tr><tr><td></td><td>HieC143</td><td>-</td><td>2</td><td></td><td>16</td><td>二</td><td></td></tr><tr><td></td><td>HiemAb114</td><td>=</td><td>7</td><td></td><td>20</td><td></td><td></td></tr><tr><td></td><td>HiemAb114UCA</td><td></td><td></td><td></td><td>-</td><td></td><td></td></tr><tr><td></td><td>HieMEDI8852</td><td></td><td></td><td></td><td>15</td><td></td><td></td></tr><tr><td>set</td><td>HieMEDI8852UCA</td><td></td><td>6</td><td></td><td>20</td><td></td><td></td></tr><tr><td></td><td>HieREGN10987</td><td></td><td>8</td><td></td><td>13</td><td></td><td></td></tr><tr><td></td><td>HieS309</td><td></td><td>10</td><td></td><td>19</td><td></td><td></td></tr><tr><td></td><td>Koenig G6</td><td>4275</td><td>-</td><td></td><td>4275</td><td></td><td></td></tr><tr><td></td><td>Prihodaimm</td><td>=</td><td>-</td><td>217</td><td>-</td><td></td><td></td></tr><tr><td></td><td>RosaceAdalimumab</td><td></td><td>14</td><td>-</td><td>14</td><td>=</td><td>14</td></tr><tr><td></td><td>Rosace CD3022</td><td></td><td>6</td><td></td><td>6</td><td></td><td>6</td></tr><tr><td></td><td>Rosace Golimumab</td><td></td><td>5</td><td></td><td>5</td><td></td><td>5</td></tr><tr><td></td><td>Shane.Trast.multi</td><td></td><td></td><td></td><td>24</td><td></td><td></td></tr><tr><td></td><td>Shane.Trast.zero</td><td></td><td></td><td></td><td>422</td><td></td><td></td></tr><tr><td></td><td>WarszawskiD44</td><td></td><td></td><td></td><td>2049</td><td></td><td></td></tr><tr><td></td><td>WittrupCST</td><td>274</td><td>137</td><td></td><td>=</td><td>822</td><td>411</td></tr></table>

# Dataset

Thisdatabase includes mutational landscapes of17distinct antibody families andatotal of13,384associated fitnessmetrics.Each sequence ismapped toat leastone fitness labelpertainingtothe6fitnessproperties

# 3 Methods

Pipeline for benchmarking protein language models

Language model AVQLVEsGce.... ppl ppl →p,T Fitness metric exp. 79.40μg/mL

Foreach protein languagemodel,weseparately input theantibody heavyand light sequences to return two perplexity scores,and we tabulate theaverage perplexity between the two sequences.Wecalculate Spearman's(p),Pearson's(r) andKendalltau's (t)correlation coefficients between perplexityand fitness.

Michael Chungyoun, Jeffrey Ruffolo, Jeffrey Gray

# 4 Results

# A heat map of model-dataset correlations

Tm. Poly.Imm.Exp. Bind. Agg. Antiberty IgLM ProtGPT2 ProGen2-S ProGen2-M ProGen2-OAS ProGen2-Base ProGen2-L   
ProGen2-BFD90 ProGen2-XL ProteinMPNN ESM-IF Rosetta E   
Incorrect No corr. Correct corr.-1.00 −0.75 -0.50 -0.25 0.00 0.25 0.50 0.75 1.00 corr.

Summary of Pearson'scorrelations.Models generallyperformbestwith thermostabilityand bindingaffinitydatasets,butmoststrugglewithaggregation propensityand polyreactivity.

# Intrinsic biophysical properties are more accurately predicted than extrinsic

Aggregation Thermostability (Extrinsic) (Intrinsic) 1.00 1.0 0.75 0.50 0.5 0.25 T ！ 0.00 0.0 Antiberty IgLM ProtGPT2 ProGen2-5 ProGen2-M ProGen2-Base ProGen2-8n2x ProteineNF RosettaE AntbertLM ProGen2-5 ProGen2-Base ProGen2.8nxL Rosetta E

Intrinsic propertiesare impacted by inherent properties of theantibody.   
Extrinsicpropertiesresult fromtarget biologyandmechanismsofaction.

# Models are more accurateat distinguishing intra-family versus inter-family antibody sets

![](/data/huangyc/Document2All/posterDataOutput_vlm/FLAb: Benchmarking deep learning methods for antibody fitness prediction_poster/auto/images/images/fig_1.jpg)

Intra-familyantibodiesare mutants originating fromsamewild type.   
Inter-familyantibodies have different wildtype origins.

# Parameter size influences performance over architecture and dataset composition

![](/data/huangyc/Document2All/posterDataOutput_vlm/FLAb: Benchmarking deep learning methods for antibody fitness prediction_poster/auto/images/images/fig_2.jpg)

Polyreactivity   
1.0   
0.8   
0.6   
0.4   
0.2   
0.0   
ProGen2-S ProGen2-M ProGen2-L ProGen2-XL

Polyreactivityand thermostabilityperformancecorrelations improvewith parametersizeforProGen2(151M,764M,2.7B,6.4Bparameters)

# Some models favor evolutionary signal rather than physical fitness

ProGen2-XL-Golimumab1.851.801.7563 64 65Temperature（C）

![](/data/huangyc/Document2All/posterDataOutput_vlm/FLAb: Benchmarking deep learning methods for antibody fitness prediction_poster/auto/images/images/fig_3.jpg)

Thelanguagemodel (left) incorrectlyassigns higherconfidence towild type antibody.Physics-basedmodel(right)correctlyassigns higherstability to the mutants

# 5 Conclusion

FLAbisa living benchmark where we will continuously add models evaluated and availableantibodydata

Nomodel wastop performingacrossallsixfitness classes