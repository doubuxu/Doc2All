# DOCSAM: UNIFIED DOCUMENT IMAGE SEGMENTATION VIA QUERY DECOMPOSITION AND HETEROGENEOUS MIXED LEARNING

Xiao-Hui $\mathbf { L i } ^ { 1 }$ , Fei $\mathbf { Y i n } ^ { 1 }$ , Cheng-Lin Liu1,2

1MAIS, Institute of Automation of Chinese Academy of Sciences, Beijing, 100190, China 2School of Artificial Intelligence, University of Chinese Academy of Sciences, Beijing, 100049, China {xiaohui.li, fyin, liucl}@nlpr.ia.ac.cn

# ABSTRACT

Document image segmentation is crucial for document analysis and recognition but remains challenging due to the diversity of document formats and segmentation tasks. Existing methods often address these tasks separately, resulting in limited generalization and resource wastage. This paper introduces DocSAM, a transformer-based unified framework designed for various document image segmentation tasks, such as document layout analysis, multi-granularity text segmentation, and table structure recognition, by modelling these tasks as a combination of instance and semantic segmentation. Specifically, DocSAM employs Sentence-BERT to map category names from each dataset into semantic queries that match the dimensionality of instance queries. These two sets of queries interact through an attention mechanism and are cross-attended with image features to predict instance and semantic segmentation masks. Instance categories are predicted by computing the dot product between instance and semantic queries, followed by softmax normalization of scores. Consequently, DocSAM can be jointly trained on heterogeneous datasets, enhancing robustness and generalization while reducing computational and storage resources. Comprehensive evaluations show that DocSAM surpasses existing methods in accuracy, efficiency, and adaptability, highlighting its potential for advancing document image understanding and segmentation across various applications. Codes are available at https://github.com/xhli-git/DocSAM.

Keywords Document Image Segmentation $\cdot$ Unified Model $\cdot$ Heterogeneous Mixed Learning

# 1 Introduction

Document image segmentation (DIS) is a fundamental task in the field of document analysis and recognition (DAR) [1], serving as a cornerstone for downstream applications such as text recognition, information extraction (IE), and document visual question answering (DocVQA). Despite its importance, DIS faces significant challenges due to the wide diversity of document types, page layouts, content annotations, and structural complexities, see fig. 1. Existing approaches often address specific aspects of DIS separately, such as layout analysis, text detection, and table structure recognition, leading to specialized and fragmented solutions tailored to particular applications. This fragmentation not only impedes the performance of individual tasks but also results in redundant computational and storage overheads, making them inefficient for large-scale deployment.

To address the aforementioned challenges, this paper introduces DocSAM (Document Segment Anything Model), a transformer-based unified framework designed to simultaneously handle various document image segmentation tasks, thereby eliminating the need for separate models and enhancing overall efficiency. As illustrated in fig. 2, DocSAM comprises four primary modules: the Vision Backbone, the Deformable Encoder, Sentence-BERT [2], and the Hybrid Query Decoder (HQD). Given a document image and desired instance or semantic class names in natural text format, DocSAM first extracts multi-scale image features using the Vision Backbone. These features are then refined by the Deformable Encoder, which includes several deformable attention layers [3]. Class names are fed into Sentence-BERT and mapped to semantic queries. Subsequently, both semantic queries and learnable instance queries pass together through the HQD, where they interact to jointly perform semantic and instance segmentation.

![]({
  "fig_id": "fig_1",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_1.jpg",
  "caption": [
    "Figure 1: Examples of various segmentation tasks on heterogeneous document datasets. "
  ],
  "content_list_index": 10,
  "llm_description": "A collage showcasing eight distinct datasets used in document and scene text analysis: PubLayNet (layout analysis), MTHv2 and SCUT-CAB-Logical (historical documents), CTW1500 and Total-Text (scene text detection), cTDaR-Moderne and cTDaR-Archive (table detection/recognition), and SCUT-HCCDoc (handwritten documents), each with visual examples of their content types.",
  "weight": 1292,
  "height": 564
})  
Figure 1: Examples of various segmentation tasks on heterogeneous document datasets.

Inside each HQD layer (see fig. 2), semantic and instance queries are concatenated and passed through a multi-head self-attention layer followed by a feed-forward layer for information exchange. These queries are then separately cross-attended with multi-scale image features in a coarse-to-fine manner using two multi-scale decoders, each with $L = 4$ layers. They further interact via another multi-head self-attention and feed-forward layer. The resulting semantic and instance queries, along with fused multi-scale image features, are forwarded to the Mask Predictor, Class Predictor, and BBox Predictor for semantic mask segmentation, instance mask segmentation, category classification, and bounding box regression, respectively. We stack $K$ HQD layers for more refined predictions.

This design ensures that DocSAM can effectively manage the heterogeneity of document types, annotation formats, and segmentation tasks while maintaining high efficiency and accuracy. Extensive experiments and evaluations on various datasets demonstrate that DocSAM surpasses existing methods in accuracy, efficiency, and adaptability. Our results highlight DocSAM’s potential as a powerful tool for advancing document image segmentation and understanding, with applications spanning from modern and historical document layout analysis to table structure decomposition, handwritten and scene text detection, and beyond. Our contributions are summarized as follows:

• We introduce DocSAM, a unified solution for diverse document image segmentation tasks such as layout analysis, multi-grained text segmentation, and table structure decomposition, reducing the need for specialized models and enhancing overall efficiency;   
• By training on various tasks and datasets, DocSAM improves robustness and generalization, making it highly effective in handling varied document types and structures; Compared to specialized models, DocSAM significantly reduces computational and storage requirements, making it more practical for large-scale deployment;   
• Extensive experiments on various datasets show that DocSAM outperforms current methods in terms of accuracy, efficiency, and adaptability.

# 2 Related Works

# 2.1 DIS Tasks and Datasets

Depending on specific application scenarios, DIS involves various sub-tasks including Document Layout Analysis (DLA), Multi-Granularity Text Detection (MGTD), and Table Structure Recognition (TSR). DLA aims at identifying and categorizing page regions including text blocks, figures and tables [4, 5, 6, 7, 8]. This foundational step provides a structured overview of the document’s layout, enabling more precise processing in subsequent tasks. MGTD focuses on detecting and segmenting text at various granularities, from paragraphs down to individual lines and words [9, 10, 11, 12, 13]. MGTD is a prerequisite for accurate Optical Character Recognition (OCR) tasks. TSR specifically aims to extract the structural of tables, including rows, columns and cells [14, 15, 16, 17, 18]. By decomposing tables into substructures, TSR facilitates the extraction and analysis of tabular information from documents.

Table 1: Datasets involved in DocSAM.   

{
  "table_id": "table_1",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_1.jpg",
  "caption": [
    "Table 1: Datasets involved in DocSAM. "
  ],
  "content_list_index": 19,
  "table_body": "<table><tr><td rowspan=1 colspan=2>Task                                                    Dataset</td></tr><tr><td rowspan=1 colspan=1>DocumentLayout</td><td rowspan=2 colspan=1>BaDLAD[20],CDLA[21],D4LA[22],DocBank [5],DocLayNet[7],ICDAR2017-POD[4],IT-AR-13K[23],Doc[8],PubLayNet [6],RanLayNet [24]</td></tr><tr><td rowspan=1 colspan=1>Analysis</td></tr><tr><td rowspan=1 colspan=1>Ancient and Hand-writtenDocumentSegmentation</td><td rowspan=1 colspan=1>CASIA-AHCDB [25], CHDAC-2022 [26],ICDAR2019-HDRC [27],SCUT-CAB [19], MTHv2[10],HJDataset [28],CASIA-HWDB [29], SCUT-HCCDoc [11]</td></tr><tr><td rowspan=1 colspan=1>Table  StructureRecognition</td><td rowspan=1 colspan=1>FinTabNet [30],ICDAR2013[31],ICDAR2017-POD[4,17],ICDAR2019-cTDaR[14,17],NTable [32],PubTables-1M[18],PubTabNet [16], STDW [33],TableBank[15],TNCR[34],WTW[35]</td></tr><tr><td rowspan=1 colspan=1>Scene Text Detec-tion</td><td rowspan=1 colspan=1>CASIA-10k[36],COCO-Text [37],CTW1500[12],CTW-Public [38],HUST-TR400 [39],ICDAR2015[40],ICDAR2017-RCTW[41],ICDAR2017-MLT[42],CDAR2019-ArT[43],ICDAR2019-LSVT[44],ICDAR2019-MLT[45],ICDAR2019-ReCTS[46],ICDAR2023-HerText [47],ICDAR2023-ReST[48],ICPR2018-TWI[49],SRA-D500[50],opig[51],Total-Text [13], USTB-SV1K [52]</td></tr></table>",
  "llm_description": "This table categorizes benchmark datasets by task type: Document Layout Analysis, Ancient/Handwritten Document Segmentation, Table Structure Recognition, and Scene Text Detection, listing specific datasets with their citation numbers for each category.",
  "weight": 1178,
  "height": 347
}

Along with these tasks, plenty of datasets have been accumulated after decades of research, see table 1. These datasets exhibit great diversity and heterogeneity in data sources, document types, annotation formats, writing languages, category sets and many other aspects. For example, PubLayNet [6] contains born-digital English PDF documents with region-level annotations; SCUT-CAB [19] and MTHv2 [10] contains scanned historical Chinese documents with region, line and char-level annotations; SCUT-HCCDoc [11] contains handwritten documents with line-level annotations; CTW1500 [12] and Total-Text [13] contain natural scene images with texts of arbitrary shapes.

# 2.2 Deep Learning for DIS

Existing deep learning based DIS methods basically focus on specific sub-tasks and datasets. Generally speaking, they usually transform various DIS tasks into general object detection or image segmentation problems and make some modifications to general object detection [53, 54, 55, 56] and image segmentation methods [57, 58, 59] to make them more suitable for the tasks and datasets at hand. Some other works treat documents as hierarchical graph structures and adopt graph models like GNN [60] and CRF [61] for the task of layout analysis [62, 63], table structure recognition [64, 17], and text detection [65, 66]. Though more flexible, these methods usually suffer from complicated pre/post-processing steps and are more susceptible to intermediate errors. There are also some multi-modal based methods that combine visual and textual features like LayoutLMv3 [67], DiT [68], and VGT [22]. These methods improve the performance and generalization by pre-training on large-scale unsupervised documents to align text and visual features, but are often slower due to the complexity of architectures.

With the prosperity of large language models (LLMs) [69], many large document models are proposed such as UDOP [70], UniDoc [71], DocPedia [72], DocLLM [73], TextMonkey [74], mPLUG-DocOwl [75, 76], etc. Though promising results can be achieved for the DocVQA task, lacking fine-grained intermediate outputs like text locations and page layouts still greatly limits the interpretability and generalization of these models. As compensation, recently some LLM-free unified models are proposed for low-level document processing tasks such as UPOCR [77], DocRes [78], OmniParser [79] and DAT [80]. These works unify several similar or related tasks into unified models through multi-task learning, but at the cost of significant increment of model complexity and calculating overhead, prohibiting them from generalizing to to more tasks and datasets.

# 2.3 Transformer-based Detection&Segmentation

Following the pioneer work of DETR [81], many Transformer-based objection methods have been proposed in recent years, including Deformable DETR [3], DN-DETR [82], DINO [83], Sparse R-CNN [84], etc. These methods share the same idea with DETR that rely on learnable queries and bipartite matching for object decoding, but make different modifications to improve the accuracy and convergence speed, such as bringing in deformable attention and denoising training, or assigning specific spatial meanings to the queries.

Besides object detection, Transformer also shows great potential in image segmentation [85, 86, 87, 88, 89, 90, 91, 92]. Among them the most related works to this paper are SAM [92] and Mask2former [90]. Inspired by SAM [92] which uses natural language prompts to guide image segmentation, in this paper we propose to embed the class names of each dataset into semantic queries and transform various document segmentation tasks into a combination of instance segmentation and semantic segmentation. The semantic queries not only serve as prompts guiding the model in identifying specific types of regions, but also function as class prototypes that instance queries depend on for classification. Since DIS relies on high resolution image features, we build our DocSAM from Mask2former [90] which adopt Swin-Transformer [93] and deformable attention [3] as the vision encoder. Though the vision encoder of DocSAM is inherited from Mask2former, the decoder is drastically redesigned to be up to the task of general document image segmentation effectively.

![]({
  "fig_id": "fig_2",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_2.jpg",
  "caption": [
    "Figure 2: Network structure of the proposed DocSAM. DocSAM unify various document image segmentation tasks into one single model through instance and semantic query decomposition and interaction. Skip connections and norm layers are omitted for simplicity. "
  ],
  "content_list_index": 29,
  "llm_description": "This diagram illustrates a vision-language model architecture for document understanding, featuring pre-processing of text and images, a vision encoder (Vision Backbone + Deformable Attention + FPN), and a multi-scale decoder with self-attention and cross-attention blocks. It integrates learnable embeddings and semantic queries to predict masked regions, object classes, and bounding boxes from the input.",
  "weight": 1239,
  "height": 550
})  
Figure 2: Network structure of the proposed DocSAM. DocSAM unify various document image segmentation tasks into one single model through instance and semantic query decomposition and interaction. Skip connections and norm layers are omitted for simplicity.

# 3 DocSAM

# 3.1 Preliminaries

Before introducing the proposed DocSAM, we first explore the key attributes of an ideal all-in-one DIS model and why current methods fall short of this goal. We assert that an exemplary all-in-one DIS model should possess the following attributes: it should have the versatility to convert diverse DIS tasks into a unified framework; it should be adaptable to training on heterogeneous datasets, accommodating diverse annotations without restrictions; and it should maintain the capacity for continual and incremental learning. Current methods are typically designed for specific DIS tasks and datasets, and most models become static after training, unable to efficiently incorporate new data, limiting their versatility and adaptability. Specifically, existing DIS methods rely on fully connected (FC) and Softmax layers to predict region classes, with FC’s parameters predefined for specific tasks and datasets, making generalization difficult.

To overcome the above limitations and achieve the aforementioned criteria, the proposed DocSAM makes two significant improvements compared to existing methods. First, it transforms various DIS tasks into a unified paradigm of maskbased instance segmentation and semantic segmentation. Second, it embeds class names into semantic queries, which not only serve as prompts to guide the model in identifying specific types of regions to segment but also function as class prototypes that instance queries depend on for classification. The rest of this chapter presents the details of our proposed DocSAM.

# 3.2 Vision Encoder

Different DIS tasks may focus on contents of different scales, from large objects like paragraphs and figures spanning entire pages to tiny objects like chars and words covering only a few hundreds of pixels. Therefore, high-resolution multi-scale image features are an essential requirement for a unified DIS model. The vision encoder of DocSAM is adapted from Mask2Former [90], which includes a Swin-Transformer [93] as the vision backbone and deformable attention [3] for feature refinement. Additionally, we use another FPN [94] to fuse multi-scale image features $X _ { I } = [ X _ { I } ^ { \tilde { l } } \ \in \mathbb { R } ^ { H _ { l } W _ { l } \times C } , l \in \{ 1 , 2 , 3 , 4 \} ]$ into a single mask feature $X _ { M } \in \mathsf { \bar { R } } ^ { \bar { H } W \times C }$ , which is used for subsequent semantic segmentation and instance segmentation. Here, $X _ { I } ^ { l }$ is image feature of level $l$ , $H _ { l }$ and $W _ { l }$ are the spatial resolution of level $l$ , $C$ is number of feature channels.

# 3.3 Query Embedding

The instance queries $Q _ { I } \in \mathbb { R } ^ { N \times C }$ of DocSAM is standard learnable queries, while the semantic queries $Q _ { S } \in \mathbb { R } ^ { M \times C }$ are embedded from class names using the Sentence-BERT [2]. Here $N$ is a predefined instance query number that remains the same across all tasks and datasets, while $M$ is the semantic query number that may change depending on the class number of each dataset, and $C$ is feature dimension. $Q _ { I }$ and $Q _ { S }$ go together through the following Hybrid Query Decoder for feature decoding and cooperate with each other for semantic segmentation and instance segmentation.

# 3.4 Hybrid Query Decoder

Inside each HQD layer, see fig. 2, we first concatenate $Q _ { S }$ and $Q _ { I }$ along the length dimension and send them into a multi-head self-attention layer (MHSA) followed by a feed forward layer (FFN). This step facilitates information exchange between $Q _ { S }$ and $Q _ { I }$ , allowing them to attend to each other for query fusion. Next, they are separately cross-attended with the multi-scale image features $X _ { I }$ in a coarse-to-fine manner by two Multi-Scale Decoders (MSD) each containing $L$ layers. Here, $L = 4$ stands for the number of feature scales. Each MSD layer consists of two MHSA layers, one multi-head cross-attention layer (MHCA) and one FFN layer. Following Mask2Former [90], we also use masked attention in MHCA, where the attention masks are derived from the predicted instance and semantic masks in the previous HQD layer. After that, $Q _ { S }$ and $Q _ { I }$ further interact with each other through another MHSA and FFN layer. We stack $K$ HQD layers for more refined predictions.

# 3.5 Prediction Head

The output $Q _ { S }$ and $Q _ { I }$ from each HQD layer along with the mask feature $X _ { M }$ are sent to the Mask Predictor, Class Predictor and BBox Predictor for semantic mask segmentation, instance mask segmentation, instance category classification and instance bounding box regression, respectively. For predicting semantic and instance masks, $Q _ { S }$ and $Q _ { I }$ are multiplied with $X _ { M }$ as:

$$
M _ { S } = \sigma ( Q _ { S } \times X _ { M } ^ { T } ) ,
$$

and

$$
M _ { I } = \sigma ( Q _ { I } \times X _ { M } ^ { T } ) ,
$$

where $M _ { S } \in \mathbb { R } ^ { M \times H W }$ and $M _ { I } \in \mathbb { R } ^ { N \times H W }$ are predicted semantic and instance masks, $\sigma$ is Sigmoid function, $T$ means matrix transposition, and $\times$ stands for matrix multiplication. Similarly, for predicting instance classes, $Q _ { I }$ is multiplied with $Q _ { S }$ as:

$$
Y _ { I } = \mathrm { S o f t m a x } ( Q _ { I } \times Q _ { S } ^ { T } ) ,
$$

where $Y _ { I } \in \mathbb { R } ^ { N \times M }$ is predicted class probabilities of instances, softmax is Softmax function along the second dimension of $Y _ { I }$ , $T$ means matrix transposition, and $\times$ stands for matrix multiplication.

Since eq. (1), eq. (2), eq. (3) are all based on matrix multiplication, they are actually calculating the similarities between $Q _ { S }$ , $Q _ { I }$ and $X _ { M }$ . So we can also regard the $Q _ { S }$ , $Q _ { I }$ as instance and semantic prototypes. Through the above semantic query embedding and prototype-based instance classification, we transform the original close-set classifier into an open-set classifier, thus benefiting the construction of unified all-in-one DIS model.

Besides mask segmentation, DocSAM also keep the ability of bbox prediction. This is realized through bounding box regression with the BBox Predictor. Following ISTR [87] and TransDLANet [8], for each HQD layer we predict the residual values of bbox coordinates relative to predictions of the previous HQD layer.

# 3.6 Model Learning

# 3.6.1 Loss Function

There are four losses in DocSAM, namely semantic mask segmentation loss $L _ { S }$ , instance mask segmentation loss $L _ { I }$ instance bbox regression loss $L _ { B }$ , and instance classification loss $L _ { C }$ . Among them, $L _ { S }$ is calculated as:

$$
{ \cal L } _ { S } = \lambda _ { f } { \cal L } _ { f o c a l } ( M _ { S } , \hat { M } _ { S } ) + \lambda _ { d } { \cal L } _ { d i c e } ( M _ { S } , \hat { M } _ { S } ) ,
$$

where $M _ { S }$ and $\hat { M } _ { S }$ are predicted and ground-truth semantic masks, $L _ { f o c a l }$ and $L _ { d i c e }$ are focal loss [95] and dice loss [96], respectively, and $\lambda _ { f } = 1 0$ and $\lambda _ { d } = 1$ are hyper-parameters. Similarly, $L _ { I }$ is calculated as:

$$
{ \cal L } _ { I } = \lambda _ { f } { \cal L } _ { f o c a l } ( M _ { I } , \hat { M } _ { I } ) + \lambda _ { d } { \cal L } _ { d i c e } ( M _ { I } , \hat { M } _ { I } ) ,
$$

where $M _ { S }$ and $\hat { M } _ { S }$ are predicted and ground-truth instance masks, respectively. $L _ { B }$ is calculated as:

$$
{ \cal L } _ { B } = \lambda _ { s l 1 } L _ { s l 1 } ( B _ { I } , \hat { B } _ { I } ) + \lambda _ { d i o u } L _ { d i o u } ( B _ { I } , \hat { B } _ { I } ) ,
$$

![]({
  "fig_id": "fig_3",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_3.jpg",
  "caption": [
    "Figure 3: Loss curves and on-the-fly validation during training. "
  ],
  "content_list_index": 61,
  "llm_description": "Training loss curves (left) show rapid convergence across DocSAM variants, while on-the-fly validation mAP (right) reveals that methods like Curriculum Learning and Sentence-BERT Training achieve superior performance, with Query Selection consistently lagging behind.",
  "weight": 1183,
  "height": 372
})  
Figure 3: Loss curves and on-the-fly validation during training.

where $B _ { I }$ and ${ \hat { B } } _ { I }$ are predicted and ground-truth bounding boxes, $L _ { s l 1 }$ and $L _ { d i o u }$ are smooth L1 loss and distance IoU loss [97], respectively, and $\lambda _ { s l 1 } = 1$ and $\lambda _ { d i o u } = 1$ are hyper-parameters. At last, $L _ { C }$ is calculated as:

$$
L _ { C } = L _ { c e } ( Y _ { I } , \hat { Y } _ { I } ) ,
$$

where $Y _ { I }$ and $\hat { Y } _ { I }$ are predicted and ground-truth instance labels, and $L _ { c e }$ is cross entropy loss. The total loss of DocSAM is the sum of the above four losses:

$$
{ \cal L } = \lambda _ { s } L _ { S } + \lambda _ { i } L _ { I } + \lambda _ { b } L _ { B } + \lambda _ { c } L _ { C } ,
$$

where ${ \lambda _ { s } } = 5$ , $\lambda _ { i } = 5$ , $\lambda _ { b } = 1$ , and ${ \lambda } _ { c } = 1$ are hyper-parameters. We add auxiliary losses to every HQD layer and to query features before HQD. Following DETR [81] and Mask2Former [90], we also use bipartite matching to find the best matched instance predictions before calculating the loss. While for semantic predictions, there is no need to perform the bipartite matching, because the predictions and ground-truths are already one-to-one matched.

# 3.6.2 Heterogeneous Mixed Learning

Unlike existing methods, the novel design of DocSAM enables us to train a single model on heterogeneous mixed datasets. In this work, we collected nearly fifty DIS datasets of various document types and annotation formats, covering diverse DIS tasks from layout analysis and text detection to table structure recognition (see table 1). We combined these datasets to construct a heterogeneous mixed dataset for training DocSAM. After training, the DocSAM model can be directly used as a versatile document segmenter or as a pre-trained model that can be seamlessly fine-tuned using task-specific datasets without any specialized modifications, such as adding or replacing a linear classification layer. This merit of DocSAM endows it with the potential for continual and incremental learning.

# 3.6.3 Improving Training Efficiency

Directly training DocSAM on such heterogeneous datasets may suffer from slow convergence and long training time, so we propose several strategies to improve training efficiency. Firstly, we pre-train the vision encoder of DocSAM on all 48 datasets using SimMIM [98], hoping it can provide more robust visual features for document images. Secondly, we separate the training datasets into groups with each group containing datasets of similar tasks and styles, see table 1, then we adopt curriculum learning (CL) [99] strategy to warm up the training process by gradually adding new group of datasets. Thirdly, we add an instance query selection (IQS) process at the front of each HQD layer. Motivation behind this is that bipartite matching only calculates losses between matched predictions and ground-truths, and the matched query indexes are mostly the same across HQD layers. For a certain document, large ratio of instance queries are not activated from beginning to end, and their class scores are very low. Therefore, we only select instance queries whose class scores are higher than a threshold $T _ { k }$ before the $k$ -th HQD layer. We set $T _ { k }$ as: $\dot { T _ { k } } = T _ { m a x } / 2 ^ { K - k }$ , where $T _ { m a x } = 0 . 0 1$ is the maximum threshold, $K$ is the number of HQD layers, $k$ is the current HQD layer. Experiments show that IQS can discard low-score queries without degrading model performance, thereby improving training speed and reducing memory usage.

# 4 Experiments

# 4.1 Datasets and Metrics

The datasets involved in our experiments are listed in table 1. Underlined datasets (15 in total) are used for ablation studies, mixed pre-training, and dataset-specific fine-tuning. All 48 datasets are used for training the final DocSAM model. These datasets cover a wide range of domains and tasks, showing significant heterogeneity in document types, annotation formats, and other aspects. Typical examples are shown in fig. 1, with more details provided in the supplementary material. For evaluation metrics, we use mIoU [57] for semantic segmentation and mAP (for masks) [100] and ${ \mathrm { m A P } } _ { b }$ (for bounding boxes) [100] for instance segmentation. Additionally, we introduce a new metric for instance segmentation called mAF, which is calculated as the mean F-score of all classes across all IoUs ranging from 0.5 to 0.95 in increments of 0.05 (i.e., [0.5:0.05:0.95]).

Table 2: Ablation studies on model structure and training strategy.   

{
  "table_id": "table_2",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_2.jpg",
  "caption": [
    "Table 2: Ablation studies on model structure and training strategy. "
  ],
  "content_list_index": 75,
  "table_body": "<table><tr><td rowspan=\"2\">Ablation Setting</td><td colspan=\"3\">Instance</td><td>Semantic</td></tr><tr><td>mAP</td><td>mAPb</td><td>mAF</td><td>mIoU</td></tr><tr><td>DocSAMbase</td><td>0.3804</td><td>0.3517</td><td>0.4256</td><td>0.6615</td></tr><tr><td>DocSAMbase +Curriculum</td><td>0.3869</td><td>0.3704</td><td>0.4338</td><td>0.6622</td></tr><tr><td>DocSAMbase +SimMIM</td><td>0.1002 0.3843</td><td>0.0658</td><td>0.1294 0.4295</td><td>0.3882</td></tr><tr><td>DocSAMbase+FreezingBERT</td><td>0.2322</td><td>0.3510</td><td>0.2846</td><td>0.6677</td></tr><tr><td>DocSAMbase - Masked Attention DocSAMbase - Query Interaction</td><td>0.2990</td><td>0.0938 0.1779</td><td>0.3509</td><td>0.6327</td></tr><tr><td>DocSAMbase - Query Selection</td><td>0.3341</td><td>0.3134</td><td></td><td>0.6511</td></tr><tr><td>DocSAMlarge</td><td>0.3900</td><td>0.3658</td><td>0.3763 0.4320</td><td>0.6592 0.6726</td></tr></table>",
  "llm_description": "This table evaluates the impact of various ablation settings on DocSAM’s performance across four metrics—instance mAP, instance mAP_b, instance mAF, and semantic mIoU—showing that adding SimMIM and Curriculum learning improves results, while removing Masked Attention or Query Interaction degrades performance, and scaling to DocSAM_large yields the best overall scores.",
  "weight": 620,
  "height": 252
}

# 4.2 Implementation Details

The vision backbone and deformable attention module are initialized from Mask2Former [90], which is pre-trained on the COCO-panoptic dataset [100]. The Sentence-BERT is initialized using the all-MiniLM-L6-v2 model from the Sentence Transformers library [2]. Other parts of DocSAM are randomly initialized. We trained two sizes of models: DocSAM-base (207M parameters) and DocSAM-large (317M parameters). Their vision backbones use Swin-base and Swin-large, respectively, and the instance query numbers $N$ are set to 500 and 900, respectively. The HQD layer number $K$ is set to 4 by default.

DocSAM is implemented based on PyTorch [101] and trained on $8 ~ \times$ NVIDIA A800 GPUs. We use the AdamW optimizer [102] to train the model, setting the base learning rate to $4 \times 1 0 ^ { - 5 }$ , and decay it using cosine annealing strategy [103]. For joint training on mixed datasets, the default settings are 80,000 iterations and a batch size of 32; for ablation studies and dataset-specific fine-tuning, the defaults are 20,000 iterations and a batch size of 8; for comparison with state-of-the-art, the defaults are 40,000 iterations and a batch size of 16.

# 4.3 Main Results

# 4.3.1 Ablation Studies

To verify the effect of each module in DocSAM and select the best training strategy before large-scale training, we conducted a series of ablation studies, as shown in table 2 and fig. 3. The results in table 2 are averaged over all 15 datasets. On-the-fly validation involves fast testing on a small number of samples (e.g. 10 for each dataset) during training. The results show that using curriculum learning and instance query selection can accelerate convergence and improve model performance, while SimMIM pre-training significantly degrades model performance, possibly due to the large gap between SimMIM and document segmentation. Since freezing the weights of Sentence-BERT has almost no impact on performance, we freeze them during training. Similar to Mask2Former, masked attention plays a crucial role in DocSAM, and removing it leads to a significant performance drop. Additionally, without query interaction, DocSAM’s performance also decreases substantially, highlighting the importance of information exchange between instance and semantic queries. Finally, training a unified model on heterogeneous datasets heavily relies on the model’s capacity, and using a more powerful vision backbone can greatly enhance model performance.

# 4.3.2 Pre-training and Fine-tuning

We train DocSAM on mixed heterogeneous datasets (15 datasets) to validate its performance as a unified document segmenter and a pre-trained model for dataset-specific fine-tuning. The results are shown in table 3 and table 4. DocSAM achieves good semantic and instance segmentation performance on various datasets and tasks, though performance may vary across datasets due to differing levels of difficulty. As a single-modal model, DocSAM may underperform on datasets like $\mathrm { D ^ { 4 } L A }$ [22], DocLayNet [7], ${ \bf M } ^ { 6 } { \bf D o c }$ [8] and SCUT-CAB-logical [19], which require multi-modal information for fine-grained logical layout analysis.

After joint training, we fine-tune DocSAM-large on each specific dataset to further improve performance. As shown in table 4, fine-tuning results are significantly higher than direct testing and training from scratch. We also test DocSAM on unseen datasets IIIT-AR-13K [23] and CHDAC-2022 [26], where fine-tuning from the pre-trained model also yields substantial performance gains. This demonstrates that DocSAM’s performance is not yet saturated and can benefit greatly from transfer learning on unseen datasets and tasks.

Table 3: Performance of DocSAM after joint pre-training.   

{
  "table_id": "table_3",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_3.jpg",
  "caption": [
    "Table 3: Performance of DocSAM after joint pre-training. "
  ],
  "content_list_index": 87,
  "table_body": "<table><tr><td rowspan=\"3\">Task</td><td rowspan=\"3\">Dataset</td><td colspan=\"6\">DocSAM-base</td><td colspan=\"6\">DocSAM-large</td></tr><tr><td colspan=\"4\">Instance</td><td>Semantic</td><td></td><td colspan=\"4\">Instance</td><td>Semantic</td></tr><tr><td>AP50</td><td>AP75</td><td>mAP</td><td>mAPb</td><td>mAF</td><td>mIoU</td><td>AP50</td><td>AP75</td><td>mAP</td><td>mAPb</td><td>mAF</td><td>mIoU</td></tr><tr><td rowspan=\"4\">Document Layout Analysis</td><td>D4LA[22] DocLayNet [7]</td><td>0.595 0.716</td><td>0.514 0.528</td><td>0.448 0.484</td><td>0.438 0.480</td><td>0.486 0.543</td><td>0.389 0.607</td><td>0.637 0.744</td><td>0.562 0.570</td><td>0.490 0.517</td><td>0.473 0.501</td><td>0.539 0.584</td><td>0.434 0.669</td></tr><tr><td>MDoc[8]</td><td>0.519</td><td>0.402</td><td>0.363</td><td>0.352</td><td>0.381</td><td>0.267</td><td>0.551</td><td>0.444</td><td>0.397</td><td>0.387</td><td>0.425</td><td>0.296</td></tr><tr><td>PubLayNet [6]</td><td>0.936</td><td>0.862</td><td>0.806</td><td>0.789</td><td>0.847</td><td>0.898</td><td>0.946</td><td>0.884</td><td>0.830</td><td>0.805</td><td>0.868</td><td>0.911</td></tr><tr><td>SCUT-CAB-logical [19]</td><td>0.681</td><td>0.555</td><td>0.481</td><td>0.478</td><td>0.502</td><td>0.410</td><td>0.717</td><td>0.574</td><td>0.511</td><td>0.495</td><td>0.534</td><td>0.454</td></tr><tr><td rowspan=\"4\">Ancient and Handwritten Document Segmentation</td><td>SCUT-CAB-physical [19]</td><td>0.937</td><td>0.837</td><td>0.777</td><td>0.747</td><td>0.821</td><td>0.937</td><td>0.948</td><td>0.856</td><td>0.786</td><td>0.754</td><td>0.829</td><td>0.942</td></tr><tr><td>HJDataset [28]</td><td>0.956</td><td>0.921</td><td>0.881</td><td>0.865</td><td>0.895</td><td>0.819</td><td>0.956</td><td>0.925</td><td>0.885</td><td>0.869</td><td>0.898</td><td>0.821</td></tr><tr><td>CASIA-HWDB [29]</td><td>0.929</td><td>0.785</td><td>0.721</td><td>0.664</td><td>0.788</td><td>0.935</td><td>0.912</td><td>0.770</td><td>0.714</td><td>0.643</td><td>0.790</td><td>0.939</td></tr><tr><td>SCUT-HCCDoc [11]</td><td>0.865</td><td>0.635</td><td>0.544</td><td>0.559</td><td>0.625</td><td>0.844</td><td>0.869</td><td>0.642</td><td>0.549</td><td>0.560</td><td>0.625</td><td>0.847</td></tr><tr><td rowspan=\"4\">Table Structure Recognition</td><td>FinTabNet [30] PubTabNet [16]</td><td>0.867</td><td>0.770</td><td>0.664</td><td>0.627</td><td>0.757</td><td>0.851</td><td>0.869</td><td>0.786</td><td>0.684</td><td>0.644</td><td>0.778</td><td>0.860</td></tr><tr><td></td><td>0.970</td><td>0.788</td><td>0.643</td><td>0.635</td><td>0.714</td><td>0.840</td><td>0.970</td><td>0.789</td><td>0.648</td><td>0.634</td><td>0.723</td><td>0.845</td></tr><tr><td>TableBank-latex [15]</td><td>0.963</td><td>0.947</td><td>0.897</td><td>0.868</td><td>0.924</td><td>0.940</td><td>0.965</td><td>0.950</td><td>0.915</td><td>0.893</td><td>0.936</td><td>0.951</td></tr><tr><td>TableBank-word [15]</td><td>0.873</td><td>0.837</td><td>0.822</td><td>0.793</td><td>0.851</td><td>0.844</td><td>0.878</td><td>0.844</td><td>0.835</td><td>0.814</td><td>0.857</td><td>0.853</td></tr><tr><td rowspan=\"4\">Scene Text Detection</td><td>CTW1500 [12]</td><td>0.712</td><td>0.430</td><td>0.400</td><td>0.368</td><td>0.500</td><td>0.794</td><td>0.753</td><td>0.482</td><td>0.441</td><td>0.402</td><td>0.531</td><td>0.817</td></tr><tr><td>Total-Text [13]</td><td>0.747</td><td>0.421</td><td>0.405</td><td>0.407</td><td>0.743</td><td>0.453</td><td>0.769</td><td>0.454</td><td>0.428</td><td>0.421</td><td>0.472</td><td>0.764</td></tr><tr><td>MSRA-TD500 [50]</td><td>0.747</td><td>0.525</td><td>0.458</td><td>0.477</td><td>0.502</td><td>0.713</td><td>0.798</td><td>0.577</td><td>0.496</td><td>0.516</td><td>0.532</td><td>0.739</td></tr><tr><td>ICDAR2015 [40]</td><td>0.613</td><td>0.247</td><td>0.294</td><td>0.302</td><td>0.338</td><td>0.599</td><td>0.639</td><td>0.260</td><td>0.307</td><td>0.313</td><td>0.345</td><td>0.623</td></tr></table>",
  "llm_description": "This table compares the performance of DocSAM-base and DocSAM-large models across four tasks—Document Layout Analysis, Ancient/Handwritten Document Segmentation, Table Structure Recognition, and Scene Text Detection—on multiple datasets, evaluating metrics including AP50, AP75, mAP, mAPb, mAF, and mIoU.",
  "weight": 1242,
  "height": 525
}

Table 4: Performance of DocSAM after dataset specific fine-tuning.   

{
  "table_id": "table_4",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_4.jpg",
  "caption": [
    "Table 4: Performance of DocSAM after dataset specific fine-tuning. "
  ],
  "content_list_index": 88,
  "table_body": "<table><tr><td rowspan=\"3\">Task</td><td rowspan=\"3\">Dataset</td><td colspan=\"6\">DocSAM-large from scratch</td><td colspan=\"6\">DocSAM-large from pretrain</td></tr><tr><td colspan=\"2\"></td><td colspan=\"3\">Instance</td><td colspan=\"2\">Semantic</td><td colspan=\"3\">Instance</td><td colspan=\"2\">Semantic</td></tr><tr><td>AP50</td><td>AP75</td><td>mAP</td><td>mAPb</td><td>mAF</td><td>mIoU</td><td>AP50</td><td>AP75</td><td>mAP</td><td>mAPb</td><td>mAF</td><td>mIoU</td></tr><tr><td rowspan=\"4\">Document Layout Analysis</td><td>D4LA[22] DocLayNet [7]</td><td>0.365 0.503</td><td>0.259 0.292</td><td>0.239 0.295</td><td>0.194 0.260</td><td>0.233 0.359</td><td>0.205 0.365</td><td>0.698 0.833</td><td>0.637 0.691</td><td>0.555 0.621</td><td>0.546 0.601</td><td>0.595 0.679</td><td>0.526 0.736</td></tr><tr><td>MDoc [8]</td><td>0.279</td><td>0.173</td><td>0.169</td><td>0.145</td><td>0.163</td><td></td><td>0.667</td><td>0.566</td><td>0.500</td><td></td><td></td><td></td></tr><tr><td>PubLayNet [6]</td><td>0.873</td><td>0.759</td><td>0.696</td><td>0.622</td><td>0.738</td><td>0.087 0.841</td><td>0.954</td><td>0.904</td><td>0.854</td><td>0.485 0.850</td><td>0.528</td><td>0.430</td></tr><tr><td></td><td>0.391</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.888 0.582</td><td>0.921 0.481</td></tr><tr><td rowspan=\"4\">Ancient and Handwritten Document Segmentation</td><td>SCUT-CAB-logical [19] SCUT-CAB-physical [19]</td><td>0.801</td><td>0.233 0.644</td><td>0.239 0.605</td><td>0.136 0.405</td><td>0.228 0.664</td><td>0.226 0.918</td><td>0.783 0.946</td><td>0.631 0.869</td><td>0.556 0.799</td><td>0.530 0.762</td><td>0.842</td><td>0.945</td></tr><tr><td>HJDataset [28]</td><td>0.848</td><td>0.835</td><td>0.752</td><td>0.606</td><td>0.777</td><td>0.812</td><td>0.983</td><td>0.948</td><td>0.905</td><td>0.895</td><td>0.911</td><td>0.822</td></tr><tr><td>CASIA-HWDB [29]</td><td>0.908</td><td>0.737</td><td>0.665</td><td>0.628</td><td>0.737</td><td>0.949</td><td>0.977</td><td>0.939</td><td>0.893</td><td>0.792</td><td></td><td>0.956</td></tr><tr><td>SCUT-HCCDoc [11]</td><td>0.807</td><td>0.492</td><td>0.460</td><td>0.423</td><td>0.541</td><td>0.853</td><td>0.904</td><td>0.684</td><td>0.580</td><td>0.589</td><td>0.916 0.658</td><td>0.862</td></tr><tr><td rowspan=\"4\">Table Structure Recognition</td><td>FinTabNet [30]</td><td>0.335</td><td>0.164</td><td>0.178</td><td>0.004</td><td>0.222</td><td>0.770</td><td>0.877</td><td>0.805</td><td>0.713</td><td>0.681</td><td>0.803</td><td>0.870</td></tr><tr><td>PubTabNet [16]</td><td>0.013</td><td>0.010</td><td>0.007</td><td>0.042</td><td>0.007</td><td>0.810</td><td>0.973</td><td>0.821</td><td>0.669</td><td>0.653</td><td>0.742</td><td>0.860</td></tr><tr><td>TableBank-latex [15]</td><td>0.762</td><td>0.612</td><td>0.565</td><td>0.020</td><td>0.641</td><td>0.913</td><td>0.968</td><td>0.954</td><td>0.926</td><td>0.909</td><td>0.947</td><td>0.958</td></tr><tr><td>TableBank-word [15]</td><td>0.594</td><td>0.446</td><td>0.435</td><td>0.045</td><td>0.619</td><td>0.823</td><td>0.908</td><td>0.877</td><td>0.871</td><td>0.859</td><td>0.881</td><td>0.873</td></tr><tr><td rowspan=\"4\">Scene Text Detection</td><td>CTW1500 [12]</td><td>0.431</td><td>0.098</td><td></td><td></td><td>0.253</td><td>0.800</td><td></td><td></td><td></td><td>0.453</td><td>0.573</td><td>0.831</td></tr><tr><td>Total-Text [13]</td><td>0.313</td><td>0.042</td><td>0.162 0.096</td><td>0.071 0.047</td><td>0.168</td><td></td><td>0.794 0.794</td><td>0.539</td><td>0.480</td><td></td><td></td><td></td></tr><tr><td>MSRA-TD500 [50]</td><td>0.506</td><td>0.189</td><td>0.222</td><td>0.076</td><td>0.295</td><td>0.749 0.731</td><td>0.809</td><td>0.517 0.604</td><td>0.460 0.524</td><td>0.466 0.541</td><td>0.502 0.555</td><td>0.775 0.744</td></tr><tr><td>ICDAR2015[40]</td><td>0.203</td><td>0.028</td><td>0.063</td><td>0.023</td><td>0.113</td><td>0.597</td><td>0.681</td><td>0.316</td><td>0.341</td><td>0.353</td><td>0.379</td><td>0.641</td></tr><tr><td rowspan=\"2\">Unseen Dataset</td><td>IIIT-AR-13K [23]</td><td>0.555</td><td>0.430</td><td>0.403</td><td>0.185</td><td>0.417</td><td>0.739</td><td>0.842</td><td>0.702</td><td>0.638</td><td>0.621</td><td>0.693</td><td>0.642</td></tr><tr><td>CHDAC-2022 [26]</td><td>0.886</td><td>0.696</td><td>0.604</td><td>0.509</td><td>0.649</td><td>0.915</td><td>0.939</td><td>0.828</td><td>0.687</td><td>0.625</td><td>0.727</td><td>0.918</td></tr></table>",
  "llm_description": "This table compares the performance of DocSAM-large models trained from scratch versus pretrained on various document analysis tasks (Document Layout Analysis, Document Segmentation, Table Structure Recognition, Scene Text Detection) across multiple datasets, reporting metrics including AP50, AP75, mAP, mAPb, mAF, and mIoU.",
  "weight": 1244,
  "height": 584
}

# 4.3.3 Comparison with State-of-the-Arts

To compare with state-of-the-art methods, we further fine-tuned DocSAM on some datasets for additional training iterations. The results are shown in table 5, table 6, and table 7. The best results are shown in bold, and the second-best results are underlined. DocSAM achieves superior or comparable performance with other methods. Note that we did not apply any specific training techniques or data augmentation, configurations for all datasets were kept consistent. We found that DocSAM exhibits much lower performance in logical layout analysis compared to physical analysis, which we attribute to its reliance only on single-modal features. Furthermore, DocSAM achieved relatively low performance on scene text detection datasets. This is likely because scene texts exhibit much greater diversity in shapes and backgrounds, requiring more carefully designed strategies to ensure model performance.

Table 5: Performance comparison on $\mathbf { M } ^ { \mathrm { 6 } } \mathbf { D } \mathbf { o c }$   

{
  "table_id": "table_5",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_5.jpg",
  "caption": [
    "Table 5: Performance comparison on $\\mathbf { M } ^ { \\mathrm { 6 } } \\mathbf { D } \\mathbf { o c }$ "
  ],
  "content_list_index": 93,
  "table_body": "<table><tr><td rowspan=2 colspan=2>Method</td><td rowspan=1 colspan=3>Object</td><td rowspan=1 colspan=3>Instance</td></tr><tr><td rowspan=1 colspan=1>mAP</td><td rowspan=1 colspan=1>AP50</td><td rowspan=1 colspan=1>AP75</td><td rowspan=1 colspan=1>mAP</td><td rowspan=1 colspan=1>AP50</td><td rowspan=1 colspan=1>AP75</td></tr><tr><td rowspan=7 colspan=2>Faster R-CNN [53]Mask R-CNN [54]Deformable DETR [3]ISTR [87]TransDLANet [8]DAT[80]DocSAM</td><td rowspan=2 colspan=1>0.4900.401</td><td rowspan=1 colspan=1>0.678</td><td rowspan=1 colspan=1>0.572</td><td rowspan=1 colspan=1>0.478</td><td rowspan=1 colspan=1>0.678</td><td rowspan=2 colspan=1>0.5520.456</td></tr><tr><td rowspan=1 colspan=1>0.584</td><td rowspan=1 colspan=1>0.462</td><td rowspan=1 colspan=1>0.397</td><td rowspan=1 colspan=1>0.584</td></tr><tr><td rowspan=1 colspan=1>0.572</td><td rowspan=1 colspan=1>0.768</td><td rowspan=1 colspan=1>0.634</td><td rowspan=1 colspan=1>0.556</td><td rowspan=1 colspan=1>0.765</td><td rowspan=1 colspan=1>0.611</td></tr><tr><td rowspan=1 colspan=1>0.627</td><td rowspan=1 colspan=1>0.808</td><td rowspan=1 colspan=1>0.708</td><td rowspan=1 colspan=1>0.620</td><td rowspan=1 colspan=1>0.807</td><td rowspan=1 colspan=1>0.702</td></tr><tr><td rowspan=1 colspan=1>0.645</td><td rowspan=1 colspan=1>0.827</td><td rowspan=1 colspan=1>0.727</td><td rowspan=1 colspan=1>0.638</td><td rowspan=3 colspan=1>0.82610.840</td><td rowspan=3 colspan=1>0.7190.750</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.712</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0.657</td></tr><tr><td rowspan=1 colspan=1>0.663</td><td rowspan=1 colspan=1>0.840</td><td rowspan=1 colspan=1>0.755</td><td rowspan=1 colspan=1>0.661</td></tr></table>",
  "llm_description": "This table compares the performance of seven object detection methods—Faster R-CNN, Mask R-CNN, Deformable DETR, ISTR, TransDLANet, DAT, and DocSAM—across two tasks (Object and Instance detection), measured by mAP, AP50, and AP75 metrics. Results show DAT achieves the highest scores overall (mAP: 0.712, AP50: 0.840, AP75: 0.755), while DocSAM performs best in instance detection (mAP: 0.661, AP50: 0.840, AP75: 0.750).",
  "weight": 605,
  "height": 230
}

Table 6: Performance comparison on SCUT-CAB.   

{
  "table_id": "table_6",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_6.jpg",
  "caption": [
    "Table 6: Performance comparison on SCUT-CAB. "
  ],
  "content_list_index": 94,
  "table_body": "<table><tr><td rowspan=\"3\">Method</td><td colspan=\"6\">Physical</td><td colspan=\"6\">Logical</td></tr><tr><td colspan=\"3\">Object</td><td></td><td colspan=\"2\">Instance</td><td></td><td colspan=\"2\">Object</td><td></td><td colspan=\"2\">Instance</td></tr><tr><td>mAP</td><td>AP50</td><td>AP75</td><td>mAP</td><td>AP50</td><td>AP75</td><td>mAP</td><td>AP50</td><td>AP75</td><td>mAP</td><td>AP50</td><td>AP75</td></tr><tr><td>Faster R-CNN [53]</td><td>0.775</td><td>0.913</td><td>0.861</td><td>0.753</td><td>0.910</td><td>0.834</td><td>0.549</td><td>0.774</td><td>0.613</td><td>0.542</td><td>0.773</td><td>0.606</td></tr><tr><td>Mask R-CNN [54]</td><td>0.791</td><td>0.921</td><td>0.877</td><td>0.795</td><td>0.917</td><td>0.872</td><td>0.551</td><td>0.785</td><td>0.619</td><td>0.553</td><td>0.777</td><td>0.631</td></tr><tr><td>SCNet [104]</td><td>0.813</td><td>0.941</td><td>0.890</td><td>0.820</td><td>0.941</td><td>0.891</td><td>0.602</td><td>0.836</td><td>0.673</td><td>0.603</td><td>0.836</td><td>0.680</td></tr><tr><td>Deformable DETR [3]</td><td>0.799</td><td>0.923</td><td>0.871</td><td>0.779</td><td>0.921</td><td>0.843</td><td>0.627</td><td>0.852</td><td>0.717</td><td>0.620</td><td>0.851</td><td>0.703</td></tr><tr><td>VSR[105]</td><td>0.787</td><td>0.919</td><td>0.860</td><td>0.787</td><td>0.919</td><td>0.852</td><td>0.557</td><td>0.783</td><td>0.616</td><td>0.551</td><td>0.782</td><td>0.611</td></tr><tr><td>DocSAM</td><td>0.774</td><td>0.947</td><td>0.860</td><td>0.811</td><td>0.948</td><td>0.891</td><td>0.548</td><td>0.769</td><td>0.632</td><td>0.575</td><td>0.779</td><td>0.667</td></tr></table>",
  "llm_description": "This table compares the performance of six object detection methods—Faster R-CNN, Mask R-CNN, SCNet, Deformable DETR, VSR, and DocSAM—across physical and logical object/instance detection metrics (mAP, AP50, AP75) on two task categories. SCNet achieves the highest overall accuracy with 0.813 mAP for physical objects, while Deformable DETR leads in logical instance detection with 0.851 mAP.",
  "weight": 1008,
  "height": 231
}

Table 7: Performance comparison on CTW1500 and Total-Text.   

{
  "table_id": "table_7",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_7.jpg",
  "caption": [
    "Table 7: Performance comparison on CTW1500 and Total-Text. "
  ],
  "content_list_index": 95,
  "table_body": "<table><tr><td rowspan=\"2\">Method</td><td colspan=\"3\">CTW1500</td><td colspan=\"3\">Total-Text</td></tr><tr><td>P</td><td>R</td><td>F</td><td>P</td><td>R</td><td>F</td></tr><tr><td>HierText [47]</td><td>0.846</td><td>0.874</td><td>0.860</td><td>0.855</td><td>0.905</td><td>0.879</td></tr><tr><td>SIR[106]</td><td>0.874</td><td>0.837</td><td>0.855</td><td>0.909</td><td>0.856</td><td>0.882</td></tr><tr><td>DPText-DETR [107]</td><td>0.917</td><td>0.862</td><td>0.888</td><td>0.918</td><td>0.864</td><td>0.890</td></tr><tr><td>UNITS [108]</td><td>1</td><td>1</td><td></td><td>1</td><td>1</td><td>0.898</td></tr><tr><td>ESTextSpotter [109]</td><td>0.915</td><td>0.886</td><td>0.900</td><td>0.920</td><td>0.881</td><td>0.900</td></tr><tr><td>DAT-DET [80]</td><td>0.893</td><td>0.893</td><td>0.893</td><td>0.940</td><td>0.882</td><td>0.910</td></tr><tr><td>DAT-SEG [80]</td><td>0.925</td><td>0.909</td><td>0.917</td><td>0.950</td><td>0.892</td><td>0.920</td></tr><tr><td>DocSAM</td><td>0.805</td><td>0.881</td><td>0.842</td><td>0.721</td><td>0.826</td><td>0.770</td></tr></table>",
  "llm_description": "This table compares the performance of eight text detection methods on two benchmarks—CTW1500 and Total-Text—using precision (P), recall (R), and F1-score (F) metrics. HierText [47] achieves the highest overall score (0.905 F1 on Total-Text), while DAT-SEG [80] shows strong balanced performance across both datasets, particularly excelling on CTW1500 with a 0.917 F1 score.",
  "weight": 589,
  "height": 253
}

# 4.4 Discussion

The goal of this paper is not to achieve state-of-the-art performance on specific dataset and task through meticulously designed model architectures or training strategies. Instead, we aim to design a simple and unified document segmentation model that can be applied to a wide variety of datasets and tasks. Additionally, the trained model should possess good scalability and the ability to continue learning. In this regard, DocSAM is quite successful. It exhibits decent performance on various datasets and tasks and shows great potential for downstream applications both as a versatile segmenter and a pre-trained model. However, experimental results also reveal some weaknesses and limitations of DocSAM, such as long training time and unsatisfactory performance on complex scenarios. We believe that DocSAM can greatly benefit from more sophisticated model design and better data augmentation and training strategies to further accelerate its convergence and improve its performance.

# 5 Conclusion

In this paper, we propose DocSAM, a transformer-based unified framework for various document image segmentation tasks. DocSAM integrates layout analysis, multi-grained text segmentation, and table structure decomposition into a single model, reducing the need for specialized models and enhancing efficiency. Trained on heterogeneous datasets, DocSAM demonstrates robust and generalizable performance, effectively handling diverse document types and structures. This approach also reduces computational and storage requirements, making DocSAM suitable for practical deployment in resource-constrained environments. Extensive experiments show that DocSAM outperforms existing methods in terms of accuracy, efficiency, and adaptability. Overall, we believe that DocSAM represents a significant step forward for document image segmentation, and we look forward to its continued development and application in practical scenarios. In the future, we plan to extend DocSAM to a multi-modal version and explore better training strategies to further accelerate its convergence and improve its performance.

# Acknowledgement

This work is supported by the National Natural Science Foundation of China(NSFC) Grant U23B2029.

# References

[1] Cheng-Lin Liu, Lianwen Jin, Xiang Bai, Xiaohui Li, and Fei Yin. Frontiers of intelligent document analysis and recognition: review and prospects. Journal of Image and Graphics, 28(08):2223–2252, 2023.   
[2] N Reimers. Sentence-bert: Sentence embeddings using siamese bert-networks. arXiv preprint arXiv:1908.10084, 2019.   
[3] Xingyi Zhu, Junwei Dai, Lu Lu, Yuwen Zhang, Peizhao Wang, Yisen Sun, Wanli Ouyang, and Ping Luo. Deformable detr: Deformable transformers for end-to-end object detection. In ICCV, pages 12352–12361, 2021.   
[4] Liangcai Gao, Xiaohan Yi, Zhuoren Jiang, Leipeng Hao, and Zhi Tang. Icdar2017 competition on page object detection. In ICDAR, volume 1, pages 1417–1422. IEEE, 2017.   
[5] Minghao Li, Yiheng Xu, Lei Cui, Shaohan Huang, Furu Wei, Zhoujun Li, and Ming Zhou. Docbank: A benchmark dataset for document layout analysis. arXiv preprint arXiv:2006.01038, 2020.   
[6] Xu Zhong, Jianbin Tang, and Antonio Jimeno Yepes. Publaynet: largest dataset ever for document layout analysis. In ICDAR, pages 1015–1022. IEEE, 2019.   
[7] Birgit Pfitzmann, Christoph Auer, Michele Dolfi, Ahmed S. Nassar, and Peter Staar. Doclaynet: A large human-annotated dataset for document-layout analysis. In ACM SIGKDD, pages 3743–3751. 2022.   
[8] Hiuyi Cheng, Peirong Zhang, Sihang Wu, Jiaxin Zhang, Qiyuan Zhu, Zecheng Xie, Jing Li, Kai Ding, and Lianwen Jin. M6doc: A large-scale multi-format, multi-type, multi-layout, multi-language, multi-annotation category dataset for modern document layout analysis. In CVPR, pages 15138–15147, 2023.   
[9] Yukun Zhai, Xiaoqiang Zhang, Xiameng Qin, Sanyuan Zhao, Xingping Dong, and Jianbing Shen. Textformer: A query-based end-to-end text spotter with mixed supervision. Machine Intelligence Research, 21(4):704–717, 2024.   
[10] Weihong Ma, Hesuo Zhang, Lianwen Jin, Sihang Wu, Jiapeng Wang, and Yongpan Wang. Joint layout analysis, character detection and recognition for historical document digitization. In ICFHR, pages 31–36. IEEE, 2020.   
[11] Hesuo Zhang, Lingyu Liang, and Lianwen Jin. Scut-hccdoc: A new benchmark dataset of handwritten chinese text in unconstrained camera-captured documents. Pattern Recognition, 108:107559, 2020.   
[12] Yuliang Liu, Lianwen Jin, Shuaitao Zhang, Canjie Luo, and Sheng Zhang. Curved scene text detection via transverse and longitudinal sequence connection. Pattern Recognition, 90:337–345, 2019.   
[13] Chee Kheng Ch’ng and Chee Seng Chan. Total-text: A comprehensive dataset for scene text detection and recognition. In ICDAR, volume 1, pages 935–942. IEEE, 2017.   
[14] Liangcai Gao, Yilun Huang, Hervé Déjean, Jean-Luc Meunier, Qinqin Yan, Yu Fang, Florian Kleber, and Eva Lang. Icdar 2019 competition on table detection and recognition (ctdar). In ICDAR, pages 1510–1515. IEEE, 2019.   
[15] Minghao Li, Lei Cui, Shaohan Huang, Furu Wei, Ming Zhou, and Zhoujun Li. Tablebank: Table benchmark for image-based table detection and recognition. In LREC, pages 1918–1925, 2020.   
[16] Xu Zhong, Elaheh ShafieiBavani, and Antonio Jimeno Yepes. Image-based table recognition: data, model, and evaluation. In ECCV, pages 564–580. Springer, 2020.   
[17] Xiao-Hui Li, Fei Yin, He-Sen Dai, and Cheng-Lin Liu. Table structure recognition and form parsing by end-to-end object detection and relation parsing. Pattern Recognition, 132:108946, 2022.   
[18] Brandon Smock, Rohith Pesala, and Robin Abraham. Pubtables-1m: Towards comprehensive table extraction from unstructured documents. In CVPR, pages 4634–4642, 2022.   
[19] Hiuyi Cheng, Cheng Jian, Sihang Wu, and Lianwen Jin. Scut-cab: a new benchmark dataset of ancient chinese books with complex layouts for document layout analysis. In ICFHR, pages 436–451. Springer, 2022.   
[20] Md Istiak Hossain Shihab, Md Rakibul Hasan, Mahfuzur Rahman Emon, Syed Mobassir Hossen, Md Nazmuddoha Ansary, Intesur Ahmed, Fazle Rabbi Rakib, Shahriar Elahi Dhruvo, Souhardya Saha Dip, Akib Hasan Pavel, et al. Badlad: A large multi-domain bengali document layout analysis dataset. In ICDAR, pages 326–341. Springer, 2023.   
[21] buptlihang. CDLA: A Benchmark Dataset for Cross-Domain Layout Analysis. https://github.com/ buptlihang/CDLA, 2023. Accessed: 2024-10-31.   
[22] Cheng Da, Chuwei Luo, Qi Zheng, and Cong Yao. Vision grid transformer for document layout analysis. In ICCV, pages 19462–19472, 2023.   
[23] Ajoy Mondal, Peter Lipps, and CV Jawahar. Iiit-ar-13k: A new dataset for graphical object detection in documents. In DAS, pages 216–230. Springer, 2020.   
[24] Avinash Anand, Raj Jaiswal, Mohit Gupta, Siddhesh S Bangar, Pijush Bhuyan, Naman Lal, Rajeev Singh, Ritika Jha, Rajiv Ratn Shah, and Shin’Ichi Satoh. Ranlaynet: A dataset for document layout detection used for domain adaptation and generalization. In ACM MM Asia, pages 1–6, 2023.   
[25] Yue Xu, Fei Yin, Da-Han Wang, Xu-Yao Zhang, Zhaoxiang Zhang, and Cheng-Lin Liu. Casia-ahcdb: A large-scale chinese ancient handwritten characters database. In ICDAR, pages 793–798. IEEE, 2019.   
[26] Pazhou Lab. IACC competition on Chinese Historical Document Analysis Challenge. https://iacc. pazhoulab-huangpu.com/contestdetail?id $\equiv$ 6497f74cd97a2dae9dcaeff8&award ${ = } 1$ ,000,000, 2022. Accessed: 2024-10-31.   
[27] Rajkumar Saini, Derek Dobson, Jon Morrey, Marcus Liwicki, and Foteini Simistira Liwicki. Icdar 2019 historical document reading challenge on large structured chinese family records. In ICDAR, pages 1499–1504. IEEE, 2019.   
[28] Zejiang Shen, Kaixuan Zhang, and Melissa Dell. A large dataset of historical japanese documents with complex layouts. In CVPR Workshops, pages 548–549, 2020.   
[29] Cheng-Lin Liu, Fei Yin, Da-Han Wang, and Qiu-Feng Wang. Casia online and offline chinese handwriting databases. In ICDAR, pages 37–41. IEEE, 2011.   
[30] Xinyi Zheng, Douglas Burdick, Lucian Popa, Xu Zhong, and Nancy Xin Ru Wang. Global table extractor (gte): A framework for joint table identification and cell structure recognition using visual context. In WACV, pages 697–706, 2021.   
[31] Max Göbel, Tamir Hassan, Ermelinda Oro, and Giorgio Orsi. Icdar 2013 table competition. In ICDAR, pages 1449–1453. IEEE, 2013.   
[32] Ziyi Zhu, Liangcai Gao, Yibo Li, Yilun Huang, Lin Du, Ning Lu, and Xianfeng Wang. Ntable: a dataset for camera-based table detection. In ICDAR, pages 117–129. Springer, 2021.   
[33] Mrinal Haloi, Shashank Shekhar, Nikhil Fande, Siddhant Swaroop Dash, et al. Table detection in the wild: A novel diverse table detection dataset and method. arXiv preprint arXiv:2209.09207, 2022.   
[34] Abdelrahman Abdallah, Alexander Berendeyev, Islam Nuradin, and Daniyar Nurseitov. Tncr: Table net detection and classification dataset. Neurocomputing, 473:79–97, 2022.   
[35] Rujiao Long, Wen Wang, Nan Xue, Feiyu Gao, Zhibo Yang, Yongpan Wang, and Gui-Song Xia. Parsing table structures in the wild. In ICCV, pages 944–952, 2021.   
[36] Wenhao He, Xu-Yao Zhang, Fei Yin, and Cheng-Lin Liu. Multi-oriented and multi-lingual scene text detection with direct regression. ICIP, 27(11):5406–5419, 2018.   
[37] Andreas Veit, Tomas Matera, Lukas Neumann, Jiri Matas, and Serge Belongie. Coco-text: Dataset and benchmark for text detection and recognition in natural images. arXiv preprint arXiv:1601.07140, 2016.   
[38] Tai-Ling Yuan, Zhe Zhu, Kun Xu, Cheng-Jun Li, Tai-Jiang Mu, and Shi-Min Hu. A large chinese text dataset in the wild. J. Comput. Sci. Tech., 34:509–521, 2019.   
[39] Cong Yao, Xiang Bai, and Wenyu Liu. A unified framework for multioriented text detection and recognition. ICIP, 23(11):4737–4749, 2014.   
[40] Dimosthenis Karatzas, Lluis Gomez-Bigorda, Anguelos Nicolaou, Suman Ghosh, Andrew Bagdanov, Masakazu Iwamura, Jiri Matas, Lukas Neumann, Vijay Ramaseshan Chandrasekhar, Shijian Lu, et al. Icdar 2015 competition on robust reading. In ICDAR, pages 1156–1160. IEEE, 2015.   
[41] Baoguang Shi, Cong Yao, Minghui Liao, Mingkun Yang, Pei Xu, Linyan Cui, Serge Belongie, Shijian Lu, and Xiang Bai. Icdar2017 competition on reading chinese text in the wild (rctw-17). In ICDAR, volume 1, pages 1429–1434. IEEE, 2017.   
[42] Nibal Nayef, Fei Yin, Imen Bizid, Hyunsoo Choi, Yuan Feng, Dimosthenis Karatzas, Zhenbo Luo, Umapada Pal, Christophe Rigaud, Joseph Chazalon, et al. Icdar2017 robust reading challenge on multi-lingual scene text detection and script identification-rrc-mlt. In ICDAR, volume 1, pages 1454–1459. IEEE, 2017.   
[43] Chee Kheng Chng, Yuliang Liu, Yipeng Sun, Chun Chet Ng, Canjie Luo, Zihan Ni, ChuanMing Fang, Shuaitao Zhang, Junyu Han, Errui Ding, et al. Icdar2019 robust reading challenge on arbitrary-shaped text-rrc-art. In ICDAR, pages 1571–1576. IEEE, 2019.   
[44] Yipeng Sun, Zihan Ni, Chee-Kheng Chng, Yuliang Liu, Canjie Luo, Chun Chet Ng, Junyu Han, Errui Ding, Jingtuo Liu, Dimosthenis Karatzas, et al. Icdar 2019 competition on large-scale street view text with partial labeling-rrc-lsvt. In ICDAR, pages 1557–1562. IEEE, 2019.   
[45] Nibal Nayef, Yash Patel, Michal Busta, Pinaki Nath Chowdhury, Dimosthenis Karatzas, Wafa Khlif, Jiri Matas, Umapada Pal, Jean-Christophe Burie, Cheng-lin Liu, et al. Icdar2019 robust reading challenge on multi-lingual scene text detection and recognition—rrc-mlt-2019. In ICDAR, pages 1582–1587. IEEE, 2019.   
[46] Rui Zhang, Yongsheng Zhou, Qianyi Jiang, Qi Song, Nan Li, Kai Zhou, Lei Wang, Dong Wang, Minghui Liao, Mingkun Yang, et al. Icdar 2019 robust reading challenge on reading chinese text on signboard. In ICDAR, pages 1577–1581. IEEE, 2019.   
[47] Shangbang Long, Siyang Qin, Dmitry Panteleev, Alessandro Bissacco, Yasuhisa Fujii, and Michalis Raptis. Towards end-to-end unified scene text detection and layout analysis. In CVPR, pages 1049–1059, 2022.   
[48] Wenwen Yu, Mingyu Liu, Mingrui Chen, Ning Lu, Yinlong Wen, Yuliang Liu, Dimosthenis Karatzas, and Xiang Bai. Icdar 2023 competition on reading the seal title. In ICDAR, pages 522–535. Springer, 2023.   
[49] Mengchao He, Yuliang Liu, Zhibo Yang, Sheng Zhang, Canjie Luo, Feiyu Gao, Qi Zheng, Yongpan Wang, Xin Zhang, and Lianwen Jin. Icpr2018 contest on robust reading for multi-type web images. In ICPR, pages 7–12. IEEE, 2018.   
[50] Cong Yao, Xiang Bai, Wenyu Liu, Yi Ma, and Zhuowen Tu. Detecting texts of arbitrary orientations in natural images. In CVPR, pages 1083–1090. IEEE, 2012.   
[51] Chongsheng Zhang, Guowen Peng, Yuefeng Tao, Feifei Fu, Wei Jiang, George Almpanidis, and Ke Chen. Shopsign: A diverse scene text dataset of chinese shop signs in street views. arXiv preprint arXiv:1903.10412, 2019.   
[52] Xu-Cheng Yin, Xuwang Yin, Kaizhu Huang, and Hong-Wei Hao. Robust text detection in natural scene images. IEEE Trans. Pattern Anal. Mach. Intell., 36(5):970–983, 2013.   
[53] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. Faster r-cnn: Towards real-time object detection with region proposal networks. In NeurIPS, volume 28, pages 91–99, 2015.   
[54] Kaiming He, Georgia Gkioxari, Piotr Dollar, and Ross Girshick. Mask r-cnn. In ICCV, pages 2961–2969, 2017.   
[55] Joseph Redmon and Ali Farhadi. You only look once: Unified, real-time object detection. In CVPR, pages 779–788, 2016.   
[56] Joseph Redmon and Ali Farhadi. Yolov3: An incremental improvement, 2018.   
[57] Jonathan Long, Evan Shelhamer, and Trevor Darrell. Fully convolutional networks for semantic segmentation. In CVPR, pages 3431–3440, 2015.   
[58] Olaf Ronneberger, Philipp Fischer, and Thomas Brox. U-net: Convolutional networks for biomedical image segmentation. In MICCAI, pages 234–241. Springer, 2015.   
[59] Liang-Chieh Chen, George Papandreou, Iasonas Kokkinos, Vladimir Koltun, and Alan Garg. Deeplab: Semantic image segmentation with deep convolutional nets, atrous convolution, and fully connected crfs. In IEEE Trans. Pattern Anal. Mach. Intell., volume 40, pages 834–848, 2018.   
[60] Zonghan Wu, Shirui Pan, Fengwen Chen, Guodong Long, Chengqi Zhang, and S Yu Philip. A comprehensive survey on graph neural networks. IEEE Trans. Neural Netw. Learn. Syst., 32(1):4–24, 2020.   
[61] John Lafferty, Andrew McCallum, Fernando Pereira, et al. Conditional random fields: Probabilistic models for segmenting and labeling sequence data. In ICML, volume 1, page 3. Williamstown, MA, 2001.   
[62] Xiao-Hui Li, Fei Yin, and Cheng-Lin Liu. Page segmentation using convolutional neural network and graphical model. In DAS, pages 231–245. Springer, 2020.   
[63] Siwen Luo, Yihao Ding, Siqu Long, Josiah Poon, and Soyeon Caren Han. Doc-gcn: Heterogeneous graph convolutional networks for document layout analysis. arXiv preprint arXiv:2208.10970, 2022.   
[64] Zewen Chi, Heyan Huang, Heng-Da Xu, Houjin Yu, Wanxuan Yin, and Xian-Ling Mao. Complicated table structure recognition. arXiv preprint arXiv:1908.04729, 2019.   
[65] Shangbang Long, Jiaqiang Ruan, Wenjie Zhang, Xin He, Wenhao Wu, and Cong Yao. Textsnake: A flexible representation for detecting text of arbitrary shapes. In ECCV, pages 20–36, 2018.   
[66] Shi-Xue Zhang, Xiaobin Zhu, Jie-Bo Hou, Chang Liu, Chun Yang, Hongfa Wang, and Xu-Cheng Yin. Deep relational reasoning graph network for arbitrary shape text detection. In CVPR, pages 9699–9708, 2020.   
[67] Yupan Huang, Tengchao Lv, Lei Cui, Yutong Lu, and Furu Wei. Layoutlmv3: Pre-training for document ai with unified text and image masking. In ACM MM, pages 4083–4091, 2022.   
[68] Junlong Li, Yiheng Xu, Tengchao Lv, Lei Cui, Cha Zhang, and Furu Wei. Dit: Self-supervised pre-training for document image transformer. In ACM MM, pages 3530–3539, 2022.   
[69] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. arXiv preprint arXiv:2303.18223, 2023.   
[70] Zineng Tang, Ziyi Yang, Guoxin Wang, Yuwei Fang, Yang Liu, Chenguang Zhu, Michael Zeng, Cha Zhang, and Mohit Bansal. Unifying vision, text, and layout for universal document processing. In CVPR, pages 19254–19264, 2023.   
[71] Hao Feng, Zijian Wang, Jingqun Tang, Jinghui Lu, Wengang Zhou, Houqiang Li, and Can Huang. Unidoc: A universal large multimodal model for simultaneous text detection, recognition, spotting and understanding. arXiv preprint arXiv:2308.11592, 2023.   
[72] Hao Feng, Qi Liu, Hao Liu, Wengang Zhou, Houqiang Li, and Can Huang. Docpedia: Unleashing the power of large multimodal model in the frequency domain for versatile document understanding. arXiv preprint arXiv:2311.11810, 2023.   
[73] Dongsheng Wang, Natraj Raman, Mathieu Sibue, Zhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, and Xiaomo Liu. Docllm: A layout-aware generative language model for multimodal document understanding. arXiv preprint arXiv:2401.00908, 2023.   
[74] Yuliang Liu, Biao Yang, Qiang Liu, Zhang Li, Zhiyin Ma, Shuo Zhang, and Xiang Bai. Textmonkey: An ocr-free large multimodal model for understanding document. arXiv preprint arXiv:2403.04473, 2024.   
[75] Jiabo Ye, Anwen Hu, Haiyang Xu, Qinghao Ye, Ming Yan, Yuhao Dan, Chenlin Zhao, Guohai Xu, Chenliang Li, Junfeng Tian, et al. mplug-docowl: Modularized multimodal large language model for document understanding. arXiv preprint arXiv:2307.02499, 2023.   
[76] Anwen Hu, Haiyang Xu, Jiabo Ye, Ming Yan, Liang Zhang, Bo Zhang, Chen Li, Ji Zhang, Qin Jin, Fei Huang, et al. mplug-docowl 1.5: Unified structure learning for ocr-free document understanding. arXiv preprint arXiv:2403.12895, 2024.   
[77] Dezhi Peng, Zhenhua Yang, Jiaxin Zhang, Chongyu Liu, Yongxin Shi, Kai Ding, Fengjun Guo, and Lianwen Jin. Upocr: Towards unified pixel-level ocr interface. In ICML, 2023.   
[78] Jiaxin Zhang, Dezhi Peng, Chongyu Liu, Peirong Zhang, and Lianwen Jin. Docres: A generalist model toward unifying document image restoration tasks. In CVPR, pages 15654–15664, 2024.   
[79] Jianqiang Wan, Sibo Song, Wenwen Yu, Yuliang Liu, Wenqing Cheng, Fei Huang, Xiang Bai, Cong Yao, and Zhibo Yang. Omniparser: A unified framework for text spotting key information extraction and table recognition. In CVPR, pages 15641–15653, 2024.   
[80] Xingyu Wan, Chengquan Zhang, Pengyuan Lyu, Sen Fan, Zihan Ni, Kun Yao, Errui Ding, and Jingdong Wang. Towards unified multi-granularity text detection with interactive attention. arXiv preprint arXiv:2405.19765, 2024.   
[81] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sylvain Gelly. End-to-end object detection with transformers. In ECCV, pages 213–229. Springer, 2020.   
[82] Feng Li, Hao Zhang, Shilong Liu, Jian Guo, Lionel M Ni, and Lei Zhang. Dn-detr: Accelerate detr training by introducing query denoising. In CVPR, pages 13619–13627, 2022.   
[83] Hao Zhang, Feng Li, Shilong Liu, Lei Zhang, Hang Su, Jun Zhu, Lionel M Ni, and Heung-Yeung Shum. Dino: Detr with improved denoising anchor boxes for end-to-end object detection. arXiv preprint arXiv:2203.03605, 2022.   
[84] Xingyi Sun, Ziyi Zhou, Peizhao Wang, Junwei Dai, Lu Lu, Wanli Ouyang, and Ping Luo. Sparse r-cnn: End-to-end object detection with learnable proposals. In CVPR, pages 13164–13173, 2021.   
[85] Enze Zheng, Zhiwei Wang, Gang Yu, Xingyi Zhang, Yuheng Wu, Hongsheng Li, and Yonghong Tian. Rethinking semantic segmentation from a sequence-to-sequence perspective with transformers. In CVPR, pages 12164– 12173, 2021.   
[86] Enze Xie, Zhiwei Wang, Gang Yu, Xingyi Zhang, Yuheng Wu, Hongsheng Li, and Yonghong Tian. Segformer: Simple and efficient design for semantic segmentation with transformers. In ICCV, pages 14125–14134, 2021.   
[87] Jie Hu, Liujuan Cao, Yao Lu, ShengChuan Zhang, Yan Wang, Ke Li, Feiyue Huang, Ling Shao, and Rongrong Ji. Istr: End-to-end instance segmentation with transformers. arXiv preprint arXiv:2105.00637, 2021.   
[88] Jie Hu, Yao Lu, Shengchuan Zhang, and Liujuan Cao. Istr: Mask-embedding-based instance segmentation transformer. IEEE Trans. Image Process., 2024. [89] Bowen Cheng, Alex Schwing, and Alexander Kirillov. Per-pixel classification is not all you need for semantic segmentation. NeurIPS, 34:17864–17875, 2021.   
[90] Bowen Cheng, Ishan Misra, Alexander G Schwing, Alexander Kirillov, and Rohit Girdhar. Masked-attention mask transformer for universal image segmentation. In CVPR, pages 1290–1299, 2022.   
[91] Hao Zhang, Feng Li, Huaizhe Xu, Shijia Huang, Shilong Liu, Lionel M Ni, and Lei Zhang. Mp-former: Mask-piloted transformer for image segmentation. In CVPR, pages 18074–18083, 2023.   
[92] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In ICCV, pages 4015–4026, 2023.   
[93] Ze Liu, Yutong Lin, Yan Cao, Yue Hu, Yu Wei, Zhiqiang Zhang, Jiahui Lin, Han Wang, Cheng Lu, Changhu Wang, et al. Swin transformer: Hierarchical vision transformer using shifted windows. In ICCV, pages 12226–12235, 2021.   
[94] Tsung-Yi Lin, Piotr Dollár, Ross Girshick, Kaiming He, Bharath Hariharan, and Serge Belongie. Feature pyramid networks for object detection. In CVPR, pages 2117–2125, 2017.   
[95] T-YLPG Ross and GKHP Dollár. Focal loss for dense object detection. In CVPR, pages 2980–2988, 2017.   
[96] Fausto Milletari, Nassir Navab, and Seyed-Ahmad Ahmadi. V-net: Fully convolutional neural networks for volumetric medical image segmentation. In 3DV, pages 565–571. Ieee, 2016. [97] Zhaohui Zheng, Ping Wang, Wei Liu, Jinze Li, Rongguang Ye, and Dongwei Ren. Distance-iou loss: Faster and better learning for bounding box regression. In AAAI, volume 34, pages 12993–13000, 2020.   
[98] Zhenda Xie, Zheng Zhang, Yue Cao, Yutong Lin, Jianmin Bao, Zhuliang Yao, Qi Dai, and Han Hu. Simmim: A simple framework for masked image modeling. In CVPR, pages 9653–9663, 2022.   
[99] Xin Wang, Yudong Chen, and Wenwu Zhu. A survey on curriculum learning. IEEE Trans. Pattern Anal. Mach. Intell., 44(9):4555–4576, 2021.   
[100] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, and C Lawrence Zitnick. Microsoft coco: Common objects in context. In ECCV, pages 740–755. Springer, 2014.   
[101] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, et al. Pytorch: An imperative style, high-performance deep learning library. NeurIPS, 32, 2019.   
[102] I Loshchilov. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017.   
[103] Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. arXiv preprint arXiv:1608.03983, 2016.   
[104] Thang Vu, Haeyong Kang, and Chang D Yoo. Scnet: Training inference sample consistency for instance segmentation. In AAAI, volume 35, pages 2701–2709, 2021.   
[105] Peng Zhang, Can Li, Liang Qiao, Zhanzhan Cheng, Shiliang Pu, Yi Niu, and Fei Wu. Vsr: a unified framework for document layout analysis combining vision, semantics and relations. In ICDAR, pages 115–130. Springer, 2021.   
[106] Xugong Qin, Pengyuan Lyu, Chengquan Zhang, Yu Zhou, Kun Yao, Peng Zhang, Hailun Lin, and Weiping Wang. Towards robust real-time scene text detection: From semantic to instance representation learning. In ACM MM, pages 2025–2034, 2023.   
[107] Maoyuan Ye, Jing Zhang, Shanshan Zhao, Juhua Liu, Bo Du, and Dacheng Tao. Dptext-detr: Towards better scene text detection with dynamic points in transformer. In AAAI, volume 37, pages 3241–3249, 2023.   
[108] Taeho Kil, Seonghyeon Kim, Sukmin Seo, Yoonsik Kim, and Daehee Kim. Towards unified scene text spotting based on sequence generation. In CVPR, pages 15223–15232, 2023.   
[109] Mingxin Huang, Jiaxin Zhang, Dezhi Peng, Hao Lu, Can Huang, Yuliang Liu, Xiang Bai, and Lianwen Jin. Estextspotter: Towards better scene text spotting with explicit synergy in transformer. In ICCV, pages 19495–19505, 2023.

# Supplementary Material

# A Dataset Statistics

Statistics of datasets involved in this paper are listed in table 8. Datasets with underline (15 datasets) are used for ablation study, mixed pre-training and dataset specific fine-tuning, then all datasets(48 datasets) are used for training the final DocSAM model. Please note that some datasets may contain multiple subsets. These datasets cover various domains and tasks and exhibit great heterogeneity in document types, annotation formats and many other aspects. Typical examples of these datasets can be found in fig. 1. In the following, we briefly introduce the 15 datasets used in our experiments, and for other datasets which are only used to train the final DocSAM model, we recommend the readers to read their original papers for more details.

PubLayNet [6] is a large-scale dataset for layout analysis of English scientific papers. It contains over 364,000 pages, which are divided into training, validation, and test sets containing 340,391, 11,858, and 11,983 pages, respectively. Five classes of page regions are annotated in this dataset including text, title, list, table, and figure. Though large-scale it is, the diversity of this dataset is limited.

DocLayNet [7] is a large-scale dataset designed for document layout analysis and understanding. It contains over 80,000 annotated pages from diverse document types, including scientific papers, reports, and forms. Each page is labeled with detailed layout information, such as text blocks, figures, tables, and captions. The dataset supports tasks like document image segmentation, object detection, and layout recognition.

$\mathbf { D ^ { 4 } L A }$ [22] is a diverse and detailed dataset for document layout analysis which contains 12 types of documents and defines 27 document layout categories. It contains over 11,000 annotated pages which are divided into training and validation sets containing 8,868 and 2,224 pages, respectively.

$\mathbf { M } ^ { 6 } \mathbf { D o c }$ [8] is by far the most diverse dataset for document layout analysis which contains 9 types of documents and defines 74 document layout categories. It contains over 9,000 annotated pages of different languages which are divided into training, validation and test sets containing 5,448, 908 and 2,724 pages, respectively.

SCUT-CAB [19] is a large-scale dataset for layout analysis of complex ancient Chinese books. It contains 4,000 annotated images, encompassing 31,925 layout elements that vary in binding styles, fonts, and preservation conditions. To support various tasks in document layout analysis, the dataset is divided into two subsets: SCUT-CAB-Physical for physical layout analysis, with four categories, and SCUT-CAB-Logical for logical layout analysis, comprising 27 categories.

HJDataset [28] is a large dataset of historical Japanese documents with complex layouts. It contains 2,271 document image scans and over 250,000 layout element annotations of seven types. In addition to bounding boxes and masks of the con- tent regions, it also includes the hierarchical structures and reading orders for layout elements.

CASIA-HWDB [29] is a large-scale handwritten dataset for Chinese text recognition. It contains ovwe 6,000 pages which are split into training and test sets containing 4875 and 1215 pages, respectively. Since it also contains bounding boxes annotations for characters and text lines, we can use it to train our DocSAM.

SCUT-HCCDoc [11] is a large-scale handwritten Chinese dataset containing 12,253 camera-captured document images of diverse styles with 116,629 text lines and 1,155,801 characters. The dataset can used for text detection, recognition or end-to-end text spotting.

TableBank [15] is a large-scale dataset for table detection and recognition which contains over 278,000 latex or word pages for table detection and over 145,000 cropped table images for table recognition. In this paper,we only use the detection subset of TableBank since the recognition subset doesn’t contain cell bounding box annotations.

PubTabNet [16] is a large-scale dataset for table structure recognition, containing over 619,000 table images. Originally designed for end-to-end table recognition, PubTabNet 2.0.0 added bounding box annotations for non-empty cells, enabling cell region detection. It provides instance annotations for two classes: table and cell. However, since the images are already cropped to focus on tables, making table detection a trivial task. Therefore, we only report results for the cell class.

FinTabNet [30] is a real-world and complex scientific and financial datasets with detailed annotations which can be used for both table detection and recognition. It contains table and cell bounding boxes annotations for over 76,000 pages which are divided into training, validation and test sets containing 61,801, 7,191 and 7,085 pages, respectively.

MSRA-TD500 [50] is a dataset for multi-oriented scene text detection. It contains 500 natural scene images with multi-oriented scene texts annotated with quadrilateral points, among which 300 are used for training and 200 are used for testing.

Table 8: Dataset statistics. Numbers with “†” means the datasets or their ground-truth annotations are not public available.   

{
  "table_id": "table_8",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_8.jpg",
  "caption": [
    "Table 8: Dataset statistics. Numbers with “†” means the datasets or their ground-truth annotations are not public available. "
  ],
  "content_list_index": 130,
  "table_body": "<table><tr><td rowspan=\"2\">Task</td><td rowspan=\"2\">Dataset</td><td colspan=\"3\">#Images</td><td rowspan=\"2\">#Classes</td><td rowspan=\"2\">Language</td><td rowspan=\"2\">Dataset</td><td colspan=\"3\">#Images Test</td><td rowspan=\"2\">#Classes</td><td rowspan=\"2\">Language</td></tr><tr><td>Train</td><td>Val</td><td>Test</td><td></td><td>Train</td><td>Val</td></tr><tr><td rowspan=\"6\">DLA</td><td>BaDLAD [20]</td><td>20,365</td><td>一</td><td>13,328t</td><td>4</td><td>Bengali</td><td>CDLA [21]</td><td>5,000</td><td>1,000</td><td>一</td><td>10</td><td>Chinese</td></tr><tr><td>D4LA [22]</td><td>8,868</td><td>2.224</td><td></td><td>27</td><td>English</td><td>DocBank [5]</td><td>40.000</td><td>5,000</td><td>5,000</td><td>13</td><td>English</td></tr><tr><td>DocLayNet [7]</td><td>69,375</td><td>6,489</td><td>4,999</td><td>11</td><td>English</td><td>ICDAR2017-POD [4]</td><td>1,600</td><td>一</td><td>817</td><td>3</td><td>English</td></tr><tr><td>IIIT-AR-13K [23]</td><td>9,333</td><td>1,955</td><td>2,120</td><td>5</td><td>English</td><td>MDoc [8]</td><td>5.448</td><td>908</td><td>2.724</td><td>74</td><td>Multilingual</td></tr><tr><td>PubLayNet [6]</td><td>340,391</td><td>11,858</td><td>11,983</td><td>5</td><td>English</td><td>RanLayNet [24]</td><td>6.998</td><td>500</td><td>1</td><td>5</td><td>English</td></tr><tr><td>CASIA-AHCDB-style1 [25]</td><td>5,854</td><td></td><td>1,679</td><td>2</td><td>Chinese</td><td>CASIA-AHCDB-style2 [25]</td><td>3,215</td><td></td><td>1,068</td><td>2</td><td>Chinese</td></tr><tr><td rowspan=\"5\">AHDS</td><td>CHDAC-2022 [26]</td><td>2.000</td><td>1 1</td><td>1,000t</td><td>1</td><td>Chinese</td><td>ICDAR2019-HDRC [27]</td><td>11,715</td><td>1 1</td><td>1,135t</td><td>2</td><td>Chinese</td></tr><tr><td>SCUT-CAB-physical [19]</td><td>3,200</td><td></td><td>800</td><td>4</td><td>Chinese</td><td>SCUT-CAB-logical [19]</td><td>3,200</td><td>一</td><td>800</td><td>27</td><td>Chinese</td></tr><tr><td>MTHv2[10]</td><td>2.399</td><td></td><td>800</td><td>2</td><td>Chinese</td><td>HJDataset [28]</td><td>1,433</td><td>307</td><td>308</td><td>7</td><td>Japanese</td></tr><tr><td>CASIA-HWDB [29]</td><td>4,875</td><td></td><td>1,215</td><td>2</td><td>Chinese</td><td>SCUT-HCCDoc [11]</td><td>9,801</td><td></td><td>2,452</td><td>1</td><td>Chinese</td></tr><tr><td>FinTabNet [30]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=\"8\">TSR</td><td></td><td>61,801</td><td>7,191</td><td>7,085</td><td>2</td><td>English</td><td>PubTabNet [16]</td><td>500,777</td><td>9,115</td><td>9,138†</td><td>2</td><td>English</td></tr><tr><td>ICDAR2013[31]</td><td></td><td>1</td><td>156</td><td>2</td><td>English</td><td>ICDAR2017-POD [4,17]</td><td>549</td><td></td><td>243</td><td>2</td><td>English</td></tr><tr><td>cTDaR-modern [14,17]</td><td>600</td><td></td><td>340</td><td>2</td><td>English</td><td>cTDaR-archival [14]</td><td>600</td><td></td><td>499</td><td>2</td><td>English</td></tr><tr><td>NTable-cam [32]</td><td>11,904</td><td>3,408</td><td>1,696</td><td>1</td><td>Multilingual</td><td>NTable-gen [32]</td><td>11,984</td><td>3,424</td><td>1,712</td><td>1</td><td>Multilingual</td></tr><tr><td>PubTables-1M-TD [18]</td><td>460,589</td><td>57,591</td><td>57,125</td><td>2</td><td>English</td><td>PubTables-1M-TSR [18]</td><td>758,849</td><td>94,959</td><td>93.834</td><td>6</td><td>English</td></tr><tr><td>TableBank-latex [15]</td><td>187,199</td><td>7,265</td><td>5,719</td><td>1</td><td>English</td><td>TableBank-word [15]</td><td>73,383</td><td>2,735</td><td>2,281</td><td>1</td><td>English</td></tr><tr><td>TNCR [34] WTW[35]</td><td>4,634 10,970</td><td>1,015 1</td><td>1,000</td><td>5 1</td><td>English</td><td>STDW[33]</td><td>7470</td><td></td><td>1</td><td>1</td><td>English</td></tr><tr><td></td><td></td><td></td><td>3.611</td><td></td><td>Multilingual</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=\"10\">STD</td><td>CASIA-10k [36]</td><td>7,000</td><td>1</td><td>3,000</td><td>1</td><td>Chinese</td><td>COCO-Text [37]</td><td>43.686</td><td>10,000</td><td>10.000+</td><td>1</td><td>English</td></tr><tr><td>CTW1500[12]</td><td>1,000</td><td>一</td><td>500</td><td>1</td><td>English</td><td>CTW-Public [38]</td><td>24,290</td><td>1,597</td><td>3,270</td><td>1</td><td>Chinese</td></tr><tr><td>HUST-TR400 [39]</td><td></td><td></td><td>400</td><td>1</td><td>English</td><td>ICDAR2015[40]</td><td>1,000</td><td></td><td>500</td><td>1</td><td>English</td></tr><tr><td>ICDAR2017-RCTW [41]</td><td>8.034</td><td></td><td>4,229†</td><td>1</td><td>Chinese</td><td>ICDAR2017-MLT[42]</td><td>7200</td><td>1800</td><td>9.000t</td><td>1</td><td>Multilingual</td></tr><tr><td>ICDAR2019-ArT [43]</td><td>5,603</td><td></td><td>4,563t</td><td>1</td><td>English</td><td>ICDAR2019-LSVT [44]</td><td>30.000</td><td>一</td><td>20.000</td><td>1</td><td>Chinese</td></tr><tr><td>ICDAR2019-MLT [45]</td><td>10,000</td><td></td><td>10.000+</td><td>1</td><td>Multilingual</td><td>ICDAR2019-ReCTS [46]</td><td>20.000</td><td>一</td><td>5.000+</td><td>2</td><td>Chinese</td></tr><tr><td>ICDAR2023-HierText [47]</td><td>8,281</td><td>1,724</td><td>1,634t</td><td>3</td><td>English</td><td>ICDAR2023-ReST[48]</td><td>5,000</td><td></td><td>5,000t</td><td>1</td><td>Chinese</td></tr><tr><td>ICPR2018-MTWI[49]</td><td>10,000</td><td></td><td>10,000+</td><td>1</td><td>Multilingual</td><td>MSRA-TD500 [50]</td><td>300</td><td></td><td>200</td><td>1</td><td>Multilingual</td></tr><tr><td>ShopSign [51]</td><td>1265</td><td>1</td><td></td><td>1</td><td>Multilingual</td><td>Total-Text [13]</td><td>1,255</td><td></td><td>300</td><td>1</td><td>English</td></tr><tr><td>USTB-SV1K [52]</td><td>500</td><td>1</td><td>500</td><td>1</td><td>English</td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>",
  "llm_description": "This table presents a comprehensive survey of datasets used in four key text recognition tasks—Document Layout Analysis (DLA), Handwritten/Printed Document Recognition (AHDS), Text Spotting in Real-world Scenes (TSR), and Scene Text Detection (STD)—detailing their split sizes (Train/Val/Test), number of classes, and primary language for each dataset.",
  "weight": 1350,
  "height": 775
}

ICDAR2015 [40] incidental scene text dataset comprises 1,670 images and 17,548 annotated regions, and 1,500 of the images have been made publicly available, among which 1,000 images are used for training and 500 images are used for testing. The remaining 170 images comprise a sequestered, private set.

CTW1500 [12] is a dataset for scene text detection and recognition, containing 1,500 images collected from real-world scenes. The dataset is divided into a training set with 1,000 images and a testing set with 500 images. Each image is annotated with text bounding boxes and transcriptions, making it suitable for evaluating text detection and recognition algorithms in complex scenes.

Total-Text [13] is a dataset for scene text detection and recognition, consisting of 1,255 natural scene images. The dataset is divided into a training set with 750 images and a testing set with 505 images. Each image is annotated with word-level irregular text instances, including curved and multi-oriented text, making it suitable for evaluating advanced text detection and recognition algorithms.

# B Train Details

Due to the significant differences in the size of various datasets, directly combining them to build a mixed heterogeneous dataset would lead to serious imbalance among the datasets. Training directly on such an imbalanced heterogeneous dataset would degrade the overall performance of DocSAM. Therefore, we propose a more reasonable strategy to address this issue. Specifically speaking, for each iteration during training we randomly sample √ $B$ samples from all√ datasets to constitute a batch, with the sampling probability of each dataset proportional to $\sqrt { C _ { i } }$ , where $\sqrt { C _ { i } }$ is the number of classes in the ith dataset. This adjusted sampling probability ensures that more complex datasets, which typically contain a greater number of classes, receive more attention during training.

Considering that some datasets may contain hundreds or even thousands of instances, such as characters, words, or cells, directly training and testing on entire images could result in low recall. To mitigate this issue, we adopt a cropped training and testing strategy. During training, we first scale the input images so that the shorter side is within the range of [704, 896] pixels, and then randomly crop them into patches of size $6 4 0 \times 6 4 0$ pixels. Alternatively, with a probability of 0.2, we resize the entire image to $6 4 0 \times 6 4 0$ pixels. During testing, we initially process the resized whole images $6 4 0 \times 6 4 0$ pixels) and then combine these results with those obtained from patches. For the patch-based approach, we first scale the entire image so that the shorter side is 800 pixels, and then crop it into patches using a sliding window method. Low-resolution whole images are used to detect larger objects or objects that span across patches, while high-resolution patches focus on smaller objects. When combining results, we reduce the confidence scores of objects detected near the boundaries of patches, as these detections are more likely to be fragmented. Finally, after combining the results, we apply non-maxima suppression to eliminate duplicate predictions arising from different patches and whole images.

Table 9: Performance of DocSAM on heterogeneous datasets and tasks.   

{
  "table_id": "table_9",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/tables/table_9.jpg",
  "caption": [
    "Table 9: Performance of DocSAM on heterogeneous datasets and tasks. "
  ],
  "content_list_index": 138,
  "table_body": "<table><tr><td rowspan=\"2\">Task</td><td rowspan=\"2\">Dataset</td><td colspan=\"4\">Instance</td><td rowspan=\"2\">Semantic</td><td rowspan=\"2\"></td><td rowspan=\"2\">Dataset</td><td colspan=\"5\">Instance mAP</td><td rowspan=\"2\">Semantic mIoU</td></tr><tr><td>AP50|AP75mAP</td><td></td><td>mAPb</td><td>mAF</td><td>mIoU</td><td colspan=\"2\">AP50|AP75</td><td colspan=\"2\">|mAPb mAF</td></tr><tr><td rowspan=\"5\">DLA</td><td>BaDLAD [20]</td><td>0.686 0.478</td><td></td><td>0.459</td><td>0.468</td><td>0.560</td><td>0.682</td><td>CDLA [21]</td><td>|0.948</td><td>0.878</td><td>0.781</td><td>0.769</td><td>|0.804</td><td>0.860</td></tr><tr><td>D4LA[22]</td><td>0.660</td><td>0.590</td><td>0.516</td><td>0.504</td><td>0.557</td><td>0.476</td><td>DocBank [5]</td><td>0.631</td><td>0.479</td><td>0.445</td><td>0.434</td><td>0.522</td><td>0.655</td></tr><tr><td>DocLayNet[7]</td><td>0.772</td><td>0.616</td><td>0.556</td><td>0.539</td><td>0.623</td><td>0.703</td><td>ICDAR2017-POD [4]</td><td>0.900</td><td>0.847</td><td>0.800</td><td>0.783</td><td>0.816</td><td>0.922</td></tr><tr><td>IT-AR-13K [23]</td><td>0.796</td><td>0.618</td><td>0.568</td><td>0.581</td><td>0.618</td><td>0.626</td><td>MDoc [8]</td><td>0.590</td><td>0.492</td><td>0.434</td><td>0.416</td><td>0.448</td><td>0.319</td></tr><tr><td>PubLayNet [6]</td><td>0.951</td><td>0.900</td><td>0.848</td><td>0.840</td><td>0.884</td><td>0.918</td><td>RanLayNet [24]</td><td>0.922</td><td>0.887</td><td>0.838</td><td>0.833</td><td>0.857</td><td>0.854</td></tr><tr><td rowspan=\"5\">AHDS</td><td>CASIA-AHCDB-style1 [25]</td><td>0.958 0.920</td><td></td><td>0.846</td><td>0.821</td><td>0.884</td><td>0.940</td><td>CASIA-AHCDB-style2 [25]</td><td>|0.951</td><td>0.918</td><td>0.813</td><td>0.799</td><td>0.864</td><td>0.913</td></tr><tr><td>CHDAC-2022 [26]</td><td>0.845</td><td>0.645</td><td>0.558</td><td>0.489</td><td>0.603</td><td>0.905</td><td>ICDAR2019-HDRC[27]</td><td>0.947</td><td>0.801</td><td>0.753</td><td>0.681</td><td>0.815</td><td>0.909</td></tr><tr><td>SCUT-CAB-physical [19]</td><td>0.950 0.871</td><td></td><td>0.805</td><td>0.774</td><td>0.849</td><td>0.948</td><td>SCUT-CAB-logical [19]</td><td>0.726</td><td>0.605</td><td>0.526</td><td>0.512</td><td>0.552</td><td>0.473</td></tr><tr><td>MTHv2[10]</td><td>0.928 0.804</td><td></td><td>0.677</td><td>0.657</td><td>0.703</td><td>0.913</td><td>HJDataset [28]</td><td>0.967</td><td>0.935</td><td>0.894</td><td>0.883</td><td>0.905</td><td>0.822</td></tr><tr><td>CASIA-HWDB [29]</td><td>0.948 0.840</td><td></td><td>0.784</td><td>0.708</td><td>0.838</td><td>0.945</td><td>SCUT-HCCDoc [11]</td><td>0.867</td><td>0.663</td><td>0.559</td><td>0.567</td><td>0.635</td><td>0.855</td></tr><tr><td rowspan=\"8\">TSR</td><td>FinTabNet [30]</td><td>0.885 |0.809</td><td></td><td>|0.718</td><td>0.698</td><td>0.799</td><td>0.870</td><td>PubTabNet [16]</td><td>|0.972</td><td>|0.803</td><td>|0.662</td><td>0.650</td><td>[0.739</td><td>0.860</td></tr><tr><td>ICDAR2013 [31]</td><td>0.942 0.564</td><td></td><td>0.612</td><td>0.520</td><td>0.566</td><td>0.844</td><td>ICDAR2017-POD [4,17]</td><td>0.941</td><td>0.854</td><td>0.764</td><td>0.735</td><td>0.799</td><td>0.897</td></tr><tr><td>cTDaR-modern [14,17]</td><td>0.919 0.575</td><td></td><td>0.646</td><td>0.601</td><td>0.706</td><td>0.878</td><td>cTDaR-archival [14]</td><td>0.897</td><td>0.717</td><td>0.672</td><td>0.627</td><td>0.691</td><td>0.956</td></tr><tr><td>NTable-cam [32]</td><td>0.893 0.803</td><td></td><td>0.714</td><td>0.727</td><td>0.770</td><td>0.875</td><td>NTable-gen [32]</td><td>0.951</td><td>0.920</td><td>0.861</td><td>0.862</td><td>0.909</td><td>0.947</td></tr><tr><td>PubTables-1M-TD [18]</td><td>0.968 0.915</td><td></td><td>0.829</td><td>0.797</td><td>0.855</td><td>0.931</td><td>PubTables-1M-TSR [18]</td><td>0.826</td><td>0.689</td><td>0.637</td><td>0.582</td><td>0.702</td><td>0.806</td></tr><tr><td>TableBank-latex [15]</td><td>0.966</td><td>0.953</td><td>0.922</td><td>0.912</td><td>0.945</td><td>0.953</td><td>TableBank-word [15]</td><td>0.886</td><td>0.848</td><td>0.845</td><td>0.829</td><td>0.864</td><td>0.857</td></tr><tr><td>TNCR [34]</td><td>0.607</td><td>0.545</td><td>0.526</td><td>0.514</td><td>0.473</td><td>0.386</td><td>STDW [33]</td><td>0.956</td><td>0.941</td><td>0.908</td><td>0.878</td><td>0.930</td><td>0.972</td></tr><tr><td>WTW [35]</td><td>0.949 0.897</td><td></td><td>0.795</td><td>0.788</td><td>0.813</td><td>0.975</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=\"9\">STD</td><td></td><td>0.652</td><td></td><td>0.386</td><td></td><td>0.428</td><td>0.807</td><td>COCO-Text [37]</td><td>0.538</td><td>0.248</td><td>0.270</td><td>0.275</td><td>[0.300</td><td>0.642</td></tr><tr><td>CASIA-10k [36] CTW1500[12]</td><td>0.800 0.518</td><td>0.408</td><td>0.469</td><td>0.385 0.438</td><td>0.564</td><td>0.822</td><td>CTW-Public [38]</td><td>0.365</td><td>0.101</td><td>0.145</td><td>0.122</td><td>0.183</td><td>0.563</td></tr><tr><td>HUST-TR400 [39]</td><td>0.850 0.746</td><td></td><td>0.632</td><td>0.601</td><td>0.682</td><td>0.863</td><td>ICDAR2015 [40]</td><td>0.688</td><td>0.302</td><td>0.340</td><td>0.346</td><td>0.381</td><td>0.630</td></tr><tr><td>ICDAR2017-RCTW[41]</td><td>0.611 0.301</td><td></td><td>0.318</td><td>0.335</td><td>0.381</td><td>0.805</td><td>ICDAR2017-MLT[42]</td><td>0.685</td><td>0.476</td><td>0.427</td><td>0.425</td><td>0.477</td><td>0.840</td></tr><tr><td>ICDAR2019-ArT[43]</td><td>0.761</td><td>0.480</td><td>0.442</td><td>0.457</td><td>0.496</td><td>0.799</td><td>ICDAR2019-LSVT [44]</td><td>0.630</td><td>0.384</td><td>0.368</td><td>0.370</td><td>0.423</td><td>0.816</td></tr><tr><td>ICDAR2019-MLT[45]</td><td>0.721</td><td>0.510</td><td>0.456</td><td>0.454</td><td>0.508</td><td>0.851</td><td>ICDAR2019-ReCTS [46]</td><td>0.737</td><td>0.533</td><td>0.478</td><td>0.470</td><td>0.527</td><td>0.846</td></tr><tr><td>ICDAR2023-HierText [47]</td><td>0.558</td><td>0.287</td><td>0.293</td><td>0.282</td><td>0.335</td><td>0.669</td><td>ICDAR2023-ReST [48]</td><td>0.949</td><td>0.870</td><td>0.743</td><td>0.825</td><td>0.774</td><td>0.827</td></tr><tr><td>ICPR2018-MTWI [49]</td><td>0.649</td><td>0.390</td><td>0.380</td><td>0.384</td><td>0.445</td><td>0.843</td><td>MSRA-TD500 [50]</td><td>0.832</td><td>0.617</td><td>0.532</td><td>0.570</td><td>0.574</td><td>0.763</td></tr><tr><td>ShopSign [51]</td><td>0.666</td><td>0.272 0.428</td><td>0.320 0.450</td><td>0.332 0.442</td><td>0.392 0.492</td><td>0.814 0.718</td><td>Total-Text [13]</td><td>0.783</td><td>0.483</td><td>0.443</td><td>0.456</td><td>0.493</td><td>0.782</td></tr><tr></table>",
  "llm_description": "This table presents performance metrics (AP50, AP75, mAP, mAP_b, mAF, mIoU) for three text detection tasks—DLA, AHDS, and TSR—across 23 datasets, alongside results for the STD task across 13 datasets. Each task’s performance is evaluated on two sets of datasets (left and right columns), with metrics indicating precision/recall at varying thresholds and localization accuracy.",
  "weight": 1280,
  "height": 756
}

# C Additional Results

We train the final DocSAM model using Swin-Large [93] as the vision backbone on all 48 datasets listed in table 8 and report the testing results of DocSAM on these datasets in table 9. If the ground-truth annotations for the test set or validation set of a specific dataset are publicly available, we test and report the results of DocSAM on the standard test set or validation set. Otherwise, we randomly split the original training set into a new training set and a validation set at a ratio of 9:1 and use these new sets for training and evaluation. Please note that this is intended to provide an intuitive sense of DocSAM’s performance on these datasets and is not suitable for direct comparison with the results of other works.

From table 9, we can see that as a single all-in-one model, DocSAM provides fairly good results across all datasets with various tasks and heterogeneous document types, despite variations in performance due to differing levels of difficulty. This demonstrates the superiority and effectiveness of DocSAM. As a single-modal model, DocSAM may underperform on datasets like $\mathrm { D ^ { 4 } L A }$ [22], DocLayNet [7], $\mathbf { M } ^ { 6 } \mathbf { D o c }$ [8], and SCUT-CAB-Logical [19], which often contain more classes and require multi-modal information for fine-grained logical layout analysis. This is also indirectly verified by the relatively low performance of semantic segmentation on these datasets. Additionally, DocSAM achieved lower performance on scene text detection datasets, likely due to the greater diversity in shapes and backgrounds of scene texts, which require more carefully designed strategies to ensure model performance. Despite these challenges, DocSAM is quite successful in achieving its goal of being a simple and unified document segmentation model applicable to a wide variety of datasets and tasks. It shows decent performance across various datasets and tasks and holds great potential for downstream applications, both as a versatile segmenter and as a pre-trained model. We believe that DocSAM can greatly benefit from more sophisticated model design and better data augmentation and training strategies to further accelerate its convergence and improve its performance.

![]({
  "fig_id": "fig_4",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_4.jpg",
  "caption": [
    "Figure 4: Qualitative results on public document layout analysis benchmarks produced by our DocSAM model. "
  ],
  "content_list_index": 144,
  "llm_description": "A grid displaying ten distinct document layout datasets — BaDLAD, CDLA, D4LA, DocBank, DocLayNet, ICDAR2017-POD, IIIIT-AR-13K, M6Doc, PubLayNet, RanLayNet — each shown with its sample page featuring varied text blocks, images, tables, and color-coded regions to illustrate diverse layout structures for document analysis.",
  "weight": 1319,
  "height": 614
})  
Figure 4: Qualitative results on public document layout analysis benchmarks produced by our DocSAM model.

![]({
  "fig_id": "fig_5",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_5.jpg",
  "caption": [
    "Figure 5: Qualitative results on public ancient and handwritten document segmentation benchmarks produced by our DocSAM model. "
  ],
  "content_list_index": 145,
  "llm_description": "A grid of ten annotated historical document images from diverse datasets (CASIA-AHCDB, CHDAC-2022, ICDAR2019-HDRC, MTHv2, SCUT-CAB, HJDataset, CASIA-HWDB, SCUT-HCCDoc), each showcasing complex layouts with overlapping text blocks highlighted in varied colors for layout analysis and recognition tasks.",
  "weight": 1314,
  "height": 612
})  
Figure 5: Qualitative results on public ancient and handwritten document segmentation benchmarks produced by our DocSAM model.

# D Qualitative results

Finally, we present some qualitative results of DocSAM on representative datasets and tasks in fig. 4, fig. 5, fig. 6, and fig. 7. From these figures, it is evident that DocSAM produces reliable predictions across a wide range of datasets and tasks, including modern and historical document layout analysis, table structure decomposition, handwritten text detection, scene text detection, and more. Specifically, DocSAM demonstrates robust performance in modern and historical document layout analysis, where it accurately identifies and segments various elements such as figures, tables, and text blocks. In table structure decomposition, DocSAM effectively recognizes and separates table cells, even in complex layouts with dense rows and columns. For handwritten text detection, the model successfully identifies and localizes individual characters and lines, even in challenging scripts and varying handwriting styles. Additionally, in scene text detection, DocSAM shows strong capabilities in detecting text in real-world images, handling diverse scenarios such as curved and multilingual texts. These results underscore the versatility and effectiveness of DocSAM

![]({
  "fig_id": "fig_6",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_6.jpg",
  "caption": [
    "across a wide range of document processing tasks, highlighting its potential for practical applications in various domains. ",
    "Figure 6: Qualitative results on public table detection and structure recognition benchmarks produced by our DocSAM model. "
  ],
  "content_list_index": 149,
  "llm_description": "A grid of 16 labeled images showcasing diverse table datasets and benchmarks used in computer vision research, including FinTabNet, PubTabNet, ICDAR competitions, cTDaR variants, NTTable series, TableBank formats, TNCr, STDW, and WTW — each displaying unique table structures, layouts, and visual styles from academic papers, technical manuals, and real-world documents.",
  "weight": 1314,
  "height": 917
})  
across a wide range of document processing tasks, highlighting its potential for practical applications in various domains.   
Figure 6: Qualitative results on public table detection and structure recognition benchmarks produced by our DocSAM model.

We also highlight some failure cases in fig. 8. Typical failure cases for document layout analysis primarily involve over-segmentation, which is often due to annotation ambiguity across different datasets. Over-segmentation is also particularly common in large table cells that contain numerous lines and paragraphs. Another frequent issue in layout analysis and table structure recognition is the imprecise prediction of bounding boxes for dense and curved text lines and cells. For scene text detection, typical failure cases mainly involve dense, curved, blurred, tiny, and occluded texts. These challenging scenarios can significantly impact the accuracy of the model, highlighting areas where further improvements are needed. By identifying these failure cases, we can better understand the limitations of DocSAM and guide future research and development efforts to enhance its performance in these challenging scenarios.

![]({
  "fig_id": "fig_7",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_7.jpg",
  "caption": [
    "Figure 7: Qualitative results on public scene text detection benchmarks produced by our DocSAM model. "
  ],
  "content_list_index": 152,
  "llm_description": "A grid of 20 diverse real-world text images showcasing various OCR datasets, including storefront signs, billboards, street signs, product packaging, and handwritten text, each labeled with its corresponding dataset name.",
  "weight": 1314,
  "height": 1259
})  
Figure 7: Qualitative results on public scene text detection benchmarks produced by our DocSAM model.

![]({
  "fig_id": "fig_8",
  "path": "/data/huangyc/Document2All/data/output2/docsam/visuals/images/fig_8.jpg",
  "caption": [
    "Figure 8: Failure cases produced by our DocSAM model. “GT” means ground-truth and “DT” means detection results. "
  ],
  "content_list_index": 154,
  "llm_description": "This image displays a comparative evaluation of six document layout analysis models (DocLayNet, M6Doc, CHDAC-2022, cTDaR-modern, cTDaR-archival) and four scene text recognition datasets (ICDAR2023-HierText, CTW-1500, ICDAR2019-ArT, CTW-Public, ICDAR2017-MLT), arranged in three rows. Each column presents the ground truth (GT) image alongside the corresponding model's or dataset's detected text regions, shown as colored bounding boxes overlaid on the original image. The top row features scanned documents with complex layouts, while the bottom row showcases real-world images including smartphones, signs, logos, and street scenes, demonstrating the models' ability to accurately localize text in diverse visual contexts.",
  "weight": 1300,
  "height": 1203
})  
Figure 8: Failure cases produced by our DocSAM model. “GT” means ground-truth and “DT” means detection results.