# Visual Correspondence Hallucination

Hugo Germain1 Vincent Lepetit1 Guillaume Bourmaud2

# 1. Low-overlap keypoint matching

# 2. Introducing NeurHal

Keypoint matching is key for fundamental matrix& camera pose estimation

In low-overlap scenarios however, finding correspondences is very challenging

Existing methods will tend to find correspondences in non-covisible areas

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_1.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_2.jpg)  
SuperPoint $^ +$ SuperGlue

We predict correspondence maps on extended field-of-views

→ → →

Training is done on both covisible and non-covisible samples

We resort toa Transformer-based image processing backbone

Correct matches within image boundaries provide poor constraints

# 3. Application to absolute camera pose estimation

We provide quantitative analysis of NeurHal's ability to hallucinate

→

NeurHal achieves sota on absolute pose estimation for low-overlap image pairs

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_3.jpg)

→

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_4.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_5.jpg)

More results in our paper !

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_6.jpg)  
Source

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_7.jpg)  
Target

NeurHal on validation image pair (novel scene)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Visual Correspondence Hallucination_poster/auto/images/images/fig_8.jpg)  
Predicted NRE Map