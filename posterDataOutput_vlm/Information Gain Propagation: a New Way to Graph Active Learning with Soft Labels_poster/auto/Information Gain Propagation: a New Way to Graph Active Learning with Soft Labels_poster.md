# Information Gain Propagation: a new way to Graph Active Learning with Soft Labels

WentaoZhang1,2,Yexin Wang1,Zhenbang You1,Meng Cao²,Ping Huang²,Jiulong Shan2,ZhiYang1,BinCui1   
ICLR2022 $\cdot$ Peking University1,Apple Inc.2

# Abstract

Graph Neural Networks (GNNs) have achieved great success in various tasks,but their performance highly relies ona large number of labeled nodes,which typically requires considerable human effort. GNN-based Active Learning (AL) methods are proposed to improve the labeling efficiency by selecting the most valuable nodes to label. Existing methods assumean oracle can correctlycategorize all the selected nodes and thus just focus on the node selection. However, such an exact labeling task is costly, especially when the categorization is out of the domain of individual expert (oracle).The paper goes further,presenting a soft-label approach to AL on GNNs. Our key innovations are: i) relaxed queries where a domain expert (oracle) only judges the correctness of the predicted labels (a binary question) rather than identifying the exact class (a multi-class question),and ii) new criteria of maximizing information gain propagation for active learnerwith relaxed queriesand soft labels.

# Methods

# Objectives

Design a novel active learning paradigm for GNNs in which onlysoft labelsare required.

# MainProblem

Previous AL methods assume the hard label (namely the exact label,However,when theactive learners in the aforementioned methods ask questions like “which category does it exactly belong to?". Such queries and assumptions exceed the capability of oracle in many labeling tasks requiring domain knowledge. For example, the task in ogbnpapers1ooM is to leverage the citation graph to infer the labels of the arXiv papers into 172 arXiv subject areas . In this example,a specialist/expert in the subject areas of machine learning is incapable of labeling query instances with subject areas of finance (such as mathematical finance or computational finance).

This part presents IGP, the first graph-based AL framework that considers the relaxed queries and soft labels.We measure the information gain of selecting a single node. To extend the information gain of a single node to the full graph, we firstly estimate the influence magnitude of graph propagation,and then combine it with the information gain and introduce the new criterion: information gain propagation.Last,we propose to select nodes which can maximize the information gain propagation.

# Information Gain

Different from the previous annotation method, which asks the oracle to directly provide annotated class l, the oracle in IGP only needs to judge whether the model prediction is correct. Rather than discard the incorrect prediction, we propose that both the correct and incorrect predictions will provide the information gain and thus enhance the label supervision.

# Influence Magnitude Estimation

Each newly annotated node will propagate its label information to its $\mathbf { k }$ -hop neighbors in a k-layer GNN and correspondingly influences the label distribution of these nodes. Since the influence of a node on its different neighbors can be various,we measure it by calculating how much change in the input label of node Vi affects the propagated label of node $\mathsf { v } _ { \mathrm { j } }$ after k-steps propagation.

# Information Gain Propagation

For a k-layer GNN, the supervision signal of one node can be propagated to its k-hop neighborhood nodes and then influences the label distribution of these neighbors. Therefore,it is unsuitable to just consider the information gain of the node itself in the node selection process. So,we extend the information gain of a single node to its k-hop neighbors in the graph.We firstly combine the influence magnitude with the normalized soft label and thenmeasure the information gain propagation of all the influenced nodes.

# Maximizing Information Gain Propagation

To maximize the uncertainty of all the influenced nodes in the semi-supervised GNN training, we aim to select and annotatea subset $\mathsf { V } _ { \parallel }$ from V so that the maximum information gainpropagationcan beachieved.

# Working Pipeline

Node Selection.Without losing generality, consider a batch setting where b nodes are selected in each iteration. Algorithm1 provides a sketch of our greedy selection method for GNNs.

Node Labeling. After getting a batch of the selected nodeset $v _ { \flat }$ ,weacquire the label from an oracle.As introduced before,different from previous works which require the oracle to annotate the hard label directly, the oracle in our framework only needs to judge the correctness of the pseudo label.

# Results

Model Training. Intuitively,a node with smaller entropy contains contributes more to the training process. In other words,a one-hot label contributes most,while other normalized soft labels also provide weak supervision.

# Datasets.

We evaluate IGP in both inductive and transductive settings: three citation networks (i.e., Citeseer, Cora,and PubMed)， one large social network (Reddit), and one OGB dataset (ogbn-arxiv).

# End-to-end Comparison.

We choose the labeling budget as 20 labels per class to show the end-to-end accuracy. Table 1 shows that GRAIN, ALG,AGE,and ANRMAB outperform Random in all the datasets,as they are specially designed for GNNs. Remarkably, IGP improves the test accuracy of the best baseline, i.e., GRAIN, by $1 . 6 { - } 2 . 2 \%$ on the three citation networks, $0 . 9 \%$ on Reddit, and $0 . 6 \%$ on ogbn-arxiv.

<table><tr><td>Method</td><td>Cora</td><td>Citeseer</td><td>PubMed</td><td>Reddit</td><td>ogbn-arxiv</td></tr><tr><td>Random</td><td>65.2(±0.8)</td><td>57.5(±0.9)</td><td>67.4(±0.6)</td><td>68.3(±0.5)</td><td>56.6(±0.4)</td></tr><tr><td>AGE</td><td>69.8(±0.6)</td><td>62.3(±0.6)</td><td>70.5(±0.4)</td><td>70.1(±0.3)</td><td>59.5(±0.3)</td></tr><tr><td>ANRMAB</td><td>70.4(±0.5)</td><td>62.2(±0.6)</td><td>70.7(±0.3)</td><td>70.4(±0.3)</td><td>59.1(±0.2)</td></tr><tr><td>GPA</td><td>71.1(±0.4)</td><td>62.8(±0.4)</td><td>71.8(±0.5)</td><td>70.9(±0.2)</td><td>59.7(±0.3)</td></tr><tr><td>SEAL</td><td>71.6(±0.5)</td><td>63.1(±0.4)</td><td>72.4(±0.4)</td><td>71.2(±0.3)</td><td>60.1(±0.1)</td></tr><tr><td>ALG</td><td>72.2(±0.6)</td><td>63.7(±0.5)</td><td>73.2(±0.3)</td><td>71.5(±0.3)</td><td>60.5(±0.2)</td></tr><tr><td>GRAIN</td><td>74.5(±0.3)</td><td>64.3(±0.3)</td><td>74.8(±0.2)</td><td>72.1(±0.1)</td><td>60.8(±0.2)</td></tr><tr><td>IGP</td><td>78.1(±0.6)</td><td>66.2(±0.3)</td><td>77.3(±0.5)</td><td>75.4(±0.2)</td><td>62.1(±0.3)</td></tr></table>

# Conclusion

This paper presents Informatioin Gain Propagation (IGP), the first GNN-based AL method which explicitly considers AL with soft labels. Concretely,we provide a new way for active learners to exhaustively label nodes with a limited budget, using a combination of domain experts and GNN model. IGP allows us to use relaxed queries where domain expert (oracle) only judges the correctness of the predicted labels rather than the exact categorization,and ii) new criteria of maximizing information gain propagation for the active learner with relaxed queries and soft labels. Empirical studies on real-world graphs show that our approach outperforms competitive baselines by a large margin, especially when the number of classes is large.