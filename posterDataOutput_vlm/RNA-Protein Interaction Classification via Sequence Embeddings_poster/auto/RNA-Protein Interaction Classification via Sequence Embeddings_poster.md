# RNA-Protein Interaction Classification via Sequence Embeddings

universitatfreiburg

DominikaMatus1,2,FredericRunge',JrgK.H.Franke',LarsGerne',MichaelUhl',FrankHutter3,1,RolfBackofen' Universtfdsoelagdteltit

# Inanutshell

# RNAInterAct

RNA and proteins form complexes through binding interactions,crucial foradvances inbiologyor medicine,suchas drug development. Predicting RNA-protein interactions (RPls) computationally ischallengingdue todatascarcity and itsbias. Wepresent RNAlnterAct,the largest publiclyavailable datasetwith biologicallyplausiblenegative interactions. Thedataset includes sequence information and precomputed embeddings thatcapturemeaningful informationabout interactors'structureand function. Ameticulous train/test splitbased on the RNA family enablesevaluationon trulyunseeninteractions. Weintroduce RPlembeddor,a transformer-based modelforbinary interactionclassificationand demonstrate its strong performance.

Compilation of the RNAlnterAct dataset in five steps:

1.Gathering positiveRPls from the RNAlnter1database:   
2. Cross-linking large scale databases to obtain sequence information.   
3. Filtering.   
4. Annotating proteins with clanand RNA with RNA family information.   
5. Generating biologically relevant negative interactions.

The final dataset contains 122,217RPls with a1:2positive to negative ratio.

![](/data/huangyc/Document2All/posterDataOutput_vlm/RNA-Protein Interaction Classification via Sequence Embeddings_poster/auto/images/images/fig_1.jpg)

# RPlembeddor

# RNA family-based train/test split

![](/data/huangyc/Document2All/posterDataOutput_vlm/RNA-Protein Interaction Classification via Sequence Embeddings_poster/auto/images/images/fig_2.jpg)

Dataset split into TRinter (training)and TSfam (test) setsbased on RNA families.

![](/data/huangyc/Document2All/posterDataOutput_vlm/RNA-Protein Interaction Classification via Sequence Embeddings_poster/auto/images/images/fig_3.jpg)

Non-homologous data guarantees evaluations on truly unseen interactions.

·Proteinembeddings:ESM- $\cdot 2 ^ { 3 }$ RNA embeddings:RNA-FM4.

<table><tr><td>Feature</td><td>TRinter</td><td>TSfam</td><td>RPI28252</td></tr><tr><td>Unique RNAFamilies</td><td>976</td><td>172</td><td>N/A</td></tr><tr><td>Unique Protein Clans</td><td>152</td><td>152</td><td>N/A</td></tr><tr><td>Positive Interactions</td><td>35,852</td><td>4,887</td><td>871</td></tr><tr><td>Negative Interactions</td><td>73,362</td><td>8,116</td><td>0</td></tr><tr><td>Total Interactions</td><td>109,214</td><td>13,003</td><td>871</td></tr></table>

# Ablation studies

<table><tr><td>Model</td><td>Prec.</td><td>Rec.</td><td>F1</td><td>Acc.</td></tr><tr><td>RPlembeddor</td><td>0.563±0.019</td><td>0.659±0.071</td><td>0.605±0.019</td><td>0.678±0.009</td></tr><tr><td>One-Hot</td><td>0.0±0.0</td><td>0.0±0.0</td><td>0.0±0.0</td><td>0.0±0.0</td></tr><tr><td>Random-Protein</td><td>0.0±0.0</td><td>0.0±0.0</td><td>0.0±0.0</td><td>0.0±0.0</td></tr><tr><td>RNA-Random</td><td>0.0±0.0</td><td>0.0±0.0</td><td>0.0±0.0</td><td>0.0±0.0</td></tr></table>

# Bothembeddings contribute to RPlembeddor's performance.

# Evaluation on TSfam and RPl2825

<table><tr><td rowspan="2">ModellTest set</td><td colspan="4">TSfam</td><td colspan="4">RPI2825</td></tr><tr><td>Prec.</td><td>Rec.</td><td>F1</td><td>Acc.</td><td>Prec.</td><td>Rec.</td><td>F1</td><td>Acc.</td></tr><tr><td>RPlembeddor</td><td>0.550 ±0.010</td><td>0.627 ±0.017</td><td>0.586 ±0.013</td><td>0.667 ±0.009</td><td>1.0 ±0.0</td><td>0.667 ±0.085</td><td>0.8 ±0.049</td><td>0.667 ±0.085</td></tr><tr><td>IPMiner</td><td>0.357</td><td>0.375</td><td>0.366</td><td>0.512</td><td>1.0</td><td>0.107</td><td>0.193</td><td>0.107</td></tr><tr><td>XRPI</td><td>0.375</td><td>0.909</td><td>0.531</td><td>0.398</td><td>1.0*</td><td>0.982*</td><td>0.991*</td><td>0.982*</td></tr></table>

\*XRPIhasbeentrainedontheRPl2825dataset.

![](/data/huangyc/Document2All/posterDataOutput_vlm/RNA-Protein Interaction Classification via Sequence Embeddings_poster/auto/images/images/fig_4.jpg)

. RPlembeddor generalizesacross data distributions.   
Competitorsbehave likerandom classifiers.