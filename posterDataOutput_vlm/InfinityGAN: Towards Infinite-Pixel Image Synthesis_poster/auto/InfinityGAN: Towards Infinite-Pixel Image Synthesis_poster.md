# InfinityGAN: Towards Infinite-Pixel Image Synthesis

Chieh Hubert Lin1Hsin-Ying Lee2Yen-Chi Cheng3Sergey Tulyakov2Ming-Hsuan Yang1,4,.5 1UC Merced2Snap Research3CMU4Google Research5Yonsei University

TL;DR We tackle the problem of synthesizing images at arbitrarily sizes, up to infinitely large.

# Synthesizing infinite-pixel images from finite-sized training data.

A $1 0 2 4 \times 2 0 4 8$ image composedof242 patches,independently synthesized by InfinityGAN with spatial fusion of two styles.The generatoris trained on101x101patches (e.g.,marked intop-left)sampledfrom197×197realimages.Note that training and inference (of any size) are performed ona single GTX TITAN X GPU.

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_1.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_2.jpg)

Without carefully taming the positional information in the generator, other frameworks cannot generalize to extended image sizes at testing.

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_3.jpg)

# We show that the two sets of latent variables learn different and diverse appearances.

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_4.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_5.jpg)  
InfinityGAN $^ +$ GAN-inversion (In&Out $\textcircled{4}$ CVPR’22) $=$ Seamless and arbitrarily-length image outpainting / inbetweening

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_6.jpg)

More samples from models trained at higherresolution settings.

A 256x10240 image ←←←←←

![](/data/huangyc/Document2All/posterDataOutput_vlm/InfinityGAN: Towards Infinite-Pixel Image Synthesis_poster/auto/images/images/fig_7.jpg)