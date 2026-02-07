# GeoReasoner: Geo-localization with Reasoning in Street Views using a Large Vision-Language Model

Ling Li, Yu Ye, Bingchuan Jiang,Wei Zeng

# Introduction

# Data Curation

# Geo-localization with Reasoning

This work tackles the problem of geo-localization with anew paradigm using a large vision-language model (LVLM) augmented with human inference knowledge.

Challenge: The scarcity of data for training the LVLM- existing street-view datasets often contain numerous low-quality images lacking visual clues, and lack any reasoning inference.

Dataset: We devise a CLIP-based network to quantify the locatability of street-view images, resulting in the creation of a new dataset comprising highly locatable street views. Additionally,we integrate external knowledge obtained from real geo-localization games, tapping into valuable human inference capabilities.

Model: GeoReasoner,which undergoes finetuning through dedicated reasoning and locationtuning stages,outperforms counterpart LVLMs by more than $25 \%$ at country-level and $38 \%$ at citylevel geo-localization tasks,and surpasses StreetCLIP in performance while requiring fewer training resources.

Retrieval-based approaches LVLM-based approaches [lat,lon] External Knowledge   
Imput [lat.Ion atput Training 0.83 [at,lon] Phase LVLM → [laton] C. 8 .》 0 →   
Classification-based approaches Images Answer   
Training Phase → Model Image Input Geo Cells Inference LVLM → LoGetion   
Inference 1 Input Reasons   
Phase Impue → Model → Clsifiation Question

Street-View Images: A total of over $\boldsymbol { \mathsf { 1 3 0 k } }$ street-view images with geo-tags collected from Google Street View Textual Clues: A total of over 3K textual clues that encapsulate rich geo-localization information from GeoGuessr and Tuxun communities

$$
\mathit { l o c a t a b i l i t y } ( \mathbf { I } _ { s e g } , \mathbf { w } _ { l o c } ) = \sum _ { k = 1 } ^ { n } \mathbf { I } _ { s e g } ( k ) \cdot \mathbf { w } _ { l o c } ^ { k }
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/GeoReasoner: Geo-localization with Reasoning in Street Views using a Large Vision-Language Model_poster/auto/images/images/fig_1.jpg)

The locatability quantization networkdevisesa CLIP-based visual-text pairingapproach to predict the locatability metric.

![](/data/huangyc/Document2All/posterDataOutput_vlm/GeoReasoner: Geo-localization with Reasoning in Street Views using a Large Vision-Language Model_poster/auto/images/images/fig_2.jpg)  
Locatability Quantization Method

![](/data/huangyc/Document2All/posterDataOutput_vlm/GeoReasoner: Geo-localization with Reasoning in Street Views using a Large Vision-Language Model_poster/auto/images/images/fig_3.jpg)

The architecture of GeoReasoner consists of three modules: Vision Encoder,VL Adapter and Pre-trained LLM. The model undergoes a two-fold supervised fine-tuning process: reasoning tuning and location tuning,to enable geo-localization with reasoning.

# GeoReasoner

Comparisonof Precision,RecallandF1scores incountry-leveland city-level geo-localization.   
\*represents the model trained on high-locatability GSV images.

STAGE1 Reasoning Tuning STAGE2 Location Tuning Vision Encoder Vision Encoder + VLAdapter imae Explainthereason. VLAdapter GSV image located? images ↓ LoRA 1 Pre-trained LLM coty:ndianignbd' LoRA 1 LoRA 2 Pre-trained LLM ('county: suitzeand StreetImage Answer Vision Encoder VL Adapter Question LoRA 1 LoRA2 Seoul',Thepictureisastreet Pre-trainedLLM → viewTheitigonh imtatettotgtio

# Experiments

![](/data/huangyc/Document2All/posterDataOutput_vlm/GeoReasoner: Geo-localization with Reasoning in Street Views using a Large Vision-Language Model_poster/auto/images/images/fig_4.jpg)  
InputQuestion

Results of theablation experiments   

<table><tr><td rowspan="2">Model</td><td colspan="3">Country</td><td colspan="3">City</td></tr><tr><td>Accuracy↑</td><td>Recall↑</td><td>F1↑</td><td>Accuracy↑</td><td>Recall↑</td><td>F1↑</td></tr><tr><td>StreetCLIP(Haas et al.,2023)</td><td>0.7943</td><td>1.00</td><td>0.8854</td><td>0.7457</td><td>1.00</td><td>0.8543</td></tr><tr><td>LLaVA(Liuet al.,2024)</td><td>0.4029</td><td>1.00</td><td>0.5744</td><td>0.2400</td><td>1.00</td><td>0.3871</td></tr><tr><td>Qwen-VL(Qwen-7B)(Bai etal.,2023a)</td><td>0.5829</td><td>0.95</td><td>0.7225</td><td>0.3743</td><td>0.89</td><td>0.5270</td></tr><tr><td>GPT-4V(Achiam et al.,2023)</td><td>0.8917</td><td>0.34</td><td>0.4923</td><td>0.5083</td><td>0.31</td><td>0.3851</td></tr><tr><td>ViT*(Dosovitskiy etal.,2021)</td><td>0.7100</td><td>1.00</td><td>0.8304</td><td>0.6762</td><td>1.00</td><td>0.8068</td></tr><tr><td>GeoReasoner*</td><td>0.8237</td><td>1.00</td><td>0.9033</td><td>0.7521</td><td>1.00</td><td>0.8585</td></tr></table>

GroundTruth·'country':China'·'city':'Lhasa'   

<table><tr><td rowspan="3">Model</td><td colspan="2">Training</td><td colspan="6">Performance</td></tr><tr><td rowspan="2">Reasoning</td><td rowspan="2">Location</td><td colspan="2">Country</td><td rowspan="2">F1↑</td><td colspan="2">City</td><td rowspan="2">F1↑</td></tr><tr><td>Accuracy↑</td><td>Recall↑</td><td>Accuracy↑</td><td>Recall↑</td></tr><tr><td>Qwen-VL(Qwen-7B)</td><td>-</td><td>-</td><td>0.5829</td><td>0.95</td><td>0.7225</td><td>0.3743</td><td>0.89</td><td>0.5270</td></tr><tr><td>GeoReasoner w/o location tuning</td><td>/</td><td>×</td><td>0.6971</td><td>1.00</td><td>0.8215</td><td>0.4114</td><td>0.99</td><td>0.5813</td></tr><tr><td>GeoReasoner w/o reasoning tuning</td><td>×</td><td>广</td><td>0.7803</td><td>1.00</td><td>0.8766</td><td>0.7029</td><td>1.00</td><td>0.8255</td></tr><tr><td>GeoReasoner</td><td>√</td><td></td><td>0.8237</td><td>1.00</td><td>0.9033</td><td>0.7521</td><td>1.00</td><td>0.8584</td></tr></table>

# Contributions

country':'China'city':'Beijing' 'reason':'ThepresenceofChinesecharactersonthebuildings and signs,as wellas the traditional Chinese clothing worn by the peopleintheimage,suggestthatthelocationisinChinaspecifirallv in Reiing'

# GPT-4V

country':'China''ciy':'hasa' 'reason':Thearchitecturalstyleandthetraditionalatireofthe personin theforeground areindicative ofTibetanculture.The signsonthebuildingsareinboth Tibetanscriptand Chinese, which is common in Tibet,China.The urban setting with the specificstyle of buildings and signage suggests thatis taken in Lhasa,the capital city of the Tibet Autonomous Region in China.

·We present a new paradigm that leveragesan LVLM and external knowledge of humaninference for geolocalization with reasoning from street-view images.

·'country':'China'·'city':'Lhasa'   
reason':Themainsquareof Lhasais themostfamoussquare in   
Lhasa,andit isalso the symbolof Lhasa.'

·We introduce the concept of locatability and devise a CLIP-based network to quantify the degree of locatability in street-view images.

·country':'China'·'city':'Lhasa' 'reason':['The pictureshowsa Tibetanwoman in traditional clothing,whichisadistinctivefeatureofTibet.TheflagofChina canbeseen inthepicture,indicating that thepicturewas taken in China.ThepictureshowsabusystreetinLasawhichisthe capital city of Tibet.']

·We propose GeoReasoner, an LVLM that outperforms existing geo-localization modelsand providesdetailed reasoning for the inferred results.