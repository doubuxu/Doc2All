# Color Equivariant Convolutional Networks

Color isacrucial visualcue for object recognition,but CNNs fail to generalize if there is data imbalance between colorvariations.Color invariance addresses this issue by removing allcolor information.We introduce Color Equivariant Convolutions (CEConvs): a novel deep learning building block that shares shape features across the color spectrumwhile retaining important colorinformation.

# Authors

AttilaLengyel,mbrettaStrafforello,obert-JanBruintjes,AexanderGielisse,JanvnGemert

Affiliations Delft UniversityofTechnology

![](/data/huangyc/Document2All/posterDataOutput_vlm/Color Equivariant Convolutional Networks_poster/auto/images/images/fig_1.jpg)  
Figure1.Color is oftena discriminative feature in object recognition. However,intra-classcolorvariationscanconfuseaclassification model.Ontheotherhand,removingcolormakes flowers lessdistinct fromtheir background and thus harder to classify.

# Preliminaries

# Contributions

# Color Equivariant Convolutions

ACNN isequivarianttoatransformationTif transforming the input $x$ by $T$ results inanequally transformed featuremap:

$$
f \bigl ( T ( x ) \bigr ) = T ^ { \prime } ( f ( x ) )
$$

Equivariance allows parameter sharing,resulting in better data efficiency and $o o D$ generalization.

Transformation information isstoredinextra FM dimension-invarianceachieved by avg pooling.

1.We show that CNNs benefit from color information and at the same time are not robust to color shifts.   
2.We introduce Color Equivariant Convolutions (CEConvs),which allows feature sharing between colors.   
3.We demonstrate that CEConvs improve robustnessto train-test color shifts in the input.   
·CEConvs implementequivariance to hue shifts.   
Hue shiftsaremodeled as3D rotations around [1,1,1] diagonal,parameterizedasa $_ { 3 \times 3 }$ rotationmatrix $H .$   
CEConv input layer isdefined as: ${ \big [ } f \star \psi ^ { i } { \big ] } ( x , k ) = \sum _ { y \in { \mathbf Z } ^ { 2 } } \sum _ { c = 1 } ^ { c ^ { l } } f _ { c } ( y ) \cdot H _ { n } ( k ) \psi _ { c } ^ { i } ( y - x )$   
·Hidden layers:cyclic permutations in color dimension.   
·Hybrid CECNNsuse CEConvs in part of network.

# When is color equivariance useful?

Synthetic toy settings:

2.Colorvariations:simulated by biased ColorMN/sT,a10-class clasification problem where each class $c$ has its own characteristic hue $\theta _ { c }$ defined indegrees,distributed uniformlyonthe huecircle.The exact colorof each digit $x$ issampled according to $\theta _ { x } \sim N ( \theta _ { c } , \sigma )$ .

![](/data/huangyc/Document2All/posterDataOutput_vlm/Color Equivariant Convolutional Networks_poster/auto/images/images/fig_2.jpg)  
G3G7B1B7B2R7B4B9G1G9R2R8G6G0B3B0R9R3R1R5G4G5G2R6R4B6B5G8B8RO Class

LeftLong-tailed ColorMNIST-CECNN(91.35 $\pm$ 0.40%)performs significantlybetter than Z2CNN $( 7 . 5 9 \pm 0 . 6 1 \% )$ .Performancemostly increasesforclasseswithfewsamples,indicatingthatCEConvs areindeedmoredataefficient.Z2cNN(grayscale）andCECNN (coset pool) withanaverageaccuracy of 24.19±0.53%and 29.43± 0.46%,respectively，areunabletodiscriminatebetweencolors.

Right>Biased ColorMNiST-Testaccuraciesfordifferent standard deviations(σ).CECNN outperforms Z2CNN acrossall σ.CECNN (coset pool) outperformsCECNN forg248-above thisvaluecolor isno longer informativeandactsas noise.Z2cNN (grayscale)is omittedas it performssignificantlyworse,ranging between 89.89% $( \sigma = 0 )$ and79.94 $( \sigma = 1 0 ^ { 6 } )$ .

![](/data/huangyc/Document2All/posterDataOutput_vlm/Color Equivariant Convolutional Networks_poster/auto/images/images/fig_3.jpg)

# Robustness to color shifts

# Conclusions

![](/data/huangyc/Document2All/posterDataOutput_vlm/Color Equivariant Convolutional Networks_poster/auto/images/images/fig_4.jpg)  
Robustnessto test-time hue shifts-Flowers-102

# Related Literature

LeftTest accuracies under gradual testtimehue shift.Huevariations degradethe performanceofCNNs (ResNet-18).Grayscale imagesandcolorjitterare invariantand thus robust,butalsofail tocaptureusefulcolor features.Ourcolor equivariant network (CE-ResNet-18-1)enablesfeature sharingacross colorsand generalizesto discrete hue shifts. Equivarianceiscomplementarytocolorjitter asthecombinationperformsbest.

Right>Neuron Feature visualizations of filters atdifferent depths in the network.Rows representthe colordimensionandencode thesame shapein different colors.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Color Equivariant Convolutional Networks_poster/auto/images/images/fig_5.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Color Equivariant Convolutional Networks_poster/auto/images/images/fig_6.jpg)

Color Equivariantconvolutionsenable feature   
sharing across colors and,unlike invariance,can still use color information.   
CECNNsoutperform regularCNNs inacolor   
imbalanced or biased setting.   
CEConvs are computationally more expensive than regular convolutions.Hybrid CECNNsprovide early equivariancewith only limited compute increase. CEConvs are only approximately equivariant due to clipping errors.   
Future work: combine color and geometric   
transformations in equivariant convolutions.