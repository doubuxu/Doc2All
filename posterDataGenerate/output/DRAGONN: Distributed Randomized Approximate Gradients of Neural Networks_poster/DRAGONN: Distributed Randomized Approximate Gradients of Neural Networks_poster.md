# DRAGONN: Distributed Randomized Approximate Gradients of Neural Networks

Zhuang Wang*, Zhaozhuo Xu*, Xinyu Crystal Wu, Anshumali Shrivastava,and T.S. Eugene Ng

* equal contribution

# Introduction

![](visuals/images/fig_1.jpg)  
Data-parallel Distributed Training (DDT)   
Training with multiple GPUs

# Communication bottleneck in DDT

# Computation gets faster

·Advanced DNN accelerators   
。P100->V100->A100   
·Advanced DNN compilers   
  
·The single-GPU iteration time of ResNet50 has reduced by 22x

![](visuals/images/fig_2.jpg)

![](visuals/images/fig_3.jpg)  
Communicationbecomesthe performance bottleneck

# Gradient Sparsification (GS)

# Selecttop-k gradients for synchronization

·Exact TopKGS   
·Approximate TopK GS,e.g.,DGC

# Save up to 99.9% the gradient exchange

·Greatly reduce the communication time

![](visuals/images/fig_4.jpg)

![](visuals/images/fig_5.jpg)

![](visuals/images/fig_6.jpg)

![](visuals/images/fig_7.jpg)

![](visuals/images/fig_8.jpg)

![](visuals/images/fig_9.jpg)

![](visuals/images/fig_10.jpg)

![](visuals/images/fig_11.jpg)  
Limitations of previous GS

# Method

# GS does not always help

·Full synchronization is better than DGC forsmaller tensors

![](visuals/images/fig_12.jpg)

# GSbecomes the major bottleneck

. Compression time exceeds communication time

![](visuals/images/fig_13.jpg)  
DRAGONN: a hashing-based compressor

# Cheap encoding operations

![](visuals/images/fig_14.jpg)

# Deploying DRAGONN in Practice

# Efficiency-awaretensor selectionforGS

·Apply DRAGONN to tensors only when itbenefits the iteration time

# Sparse decoding

·Minimize the decoding overhead after communication

# Experiment

Evaluations

# Training throughput

![](visuals/images/fig_15.jpg)  
ResNet50 overImageNet

![](visuals/images/fig_16.jpg)  
XMLover Wiki10-31K

![](visuals/images/fig_17.jpg)  
ViT over ImageNet

# Accuracy vs Iteration

![](visuals/images/fig_18.jpg)  
ResNet50

![](visuals/images/fig_19.jpg)  
XML

![](visuals/images/fig_20.jpg)  
ViT

# Improvementbreakdown

![](visuals/images/fig_21.jpg)  
ResNet50

![](visuals/images/fig_22.jpg)  
XML

![](visuals/images/fig_23.jpg)  
ViT

# Acknowledgements

NSF, ONR DURIP, ONR BRC and Ken Kennedy Institute BP fellowship