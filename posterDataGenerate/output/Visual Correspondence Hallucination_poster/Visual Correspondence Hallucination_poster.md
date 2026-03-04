hugogermain.com/neurhal

# Visual Correspondence Hallucination

Hugo Germain1

Vincent Lepetit1

Guillaume Bourmaud2

# 1. Low-overlap keypoint matching

Keypoint matching is key for fundamental matrix& camera pose estimation   
In low-overlap scenarios however, finding correspondences is very challenging   
Existing methods will tend to find correspondences in non-covisible areas

![](visuals/images/fig_1.jpg)

![](visuals/images/fig_2.jpg)  
SuperPoint $^ +$ SuperGlue

Correct matches within image boundaries provide poor constraints

![](visuals/images/fig_3.jpg)

# 2. Introducing NeurHal

![](visuals/images/fig_4.jpg)

![](visuals/images/fig_5.jpg)

We predict correspondence maps on extended field-of-views

![](visuals/images/fig_6.jpg)

Training is done on both covisible and non-covisible samples

![](visuals/images/fig_7.jpg)

We resort to a Transformer-based image processing backbone

# 3. Application to absolute camera pose estimation

![](visuals/images/fig_8.jpg)  
We provide quantitative analysis of NeurHal's ability to hallucinate

![](visuals/images/fig_9.jpg)  
NeurHal on validation image pair (novel scene)

![](visuals/images/fig_10.jpg)  
NeurHal achieves sota on absolute pose estimation for low-overlap image pairs

![](visuals/images/fig_11.jpg)  
More results in our paper !

![](visuals/images/fig_12.jpg)  
Source

![](visuals/images/fig_13.jpg)  
Target

![](visuals/images/fig_14.jpg)  
Predicted NRE Map