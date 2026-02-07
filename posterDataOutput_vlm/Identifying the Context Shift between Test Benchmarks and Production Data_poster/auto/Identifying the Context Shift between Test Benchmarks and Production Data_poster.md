# ldentifying the Context Shift between Test Benchmarks and Production Data

MatGroh, MIT Media Lab

# Will your model work in production?

![](/data/huangyc/Document2All/posterDataOutput_vlm/Identifying the Context Shift between Test Benchmarks and Production Data_poster/auto/images/images/fig_1.jpg)

Exampleerrorson out-of-distributiondata

![](/data/huangyc/Document2All/posterDataOutput_vlm/Identifying the Context Shift between Test Benchmarks and Production Data_poster/auto/images/images/fig_2.jpg)

# Consider the Data Generating Process

Distribution Shift Perspective

# Context Shift Perspective

Covariate Shift: $P _ { t e s t } ( x ) \neq P _ { t r a i n } ( x )$ and $P _ { t e s t } ( y | x ) = P _ { t r a i n } ( y | x )$

Prior Probability Shift: $P _ { t e s t } ( y ) \neq P _ { t r a i n } ( y )$ and $P _ { t e s t } ( y | x ) = P _ { t r a i n } ( y | x )$

Concept Shift: $P _ { t e s t } ( x ) = P _ { t r a i n } ( x )$ and $P _ { t e s t } ( y | x ) \neq P _ { t r a i n } ( y | x )$

Sample Selection Bias:when the data distribution is missing relevant examples or dimensions

Other Distribution Shift: $P _ { t e s t } ( x , y ) \neq P _ { t r a i n } ( x , y )$

Non-stationarity:when the data distribution changes over time or environment

Adversarial Perturbations:when the distribution of data isaltered in a way that does not affect human task performance

# Contextual Dimensions in Human Centered ML Applications

ee

Who is represented in the data? Who is annotating the data? When and where is data collected? Howdo social,geographical,temporal,esthetic,financial,andther iiosyncrasies infuence tedatc

# Data Generation Process Desiderata for Dynamic Benchmarks

1.Prediction Task: What are the input features and output labels? e.g.Dynabench13   
2.TestSize:Whatis the minimum test size forreducing within data sampling eror toan acceptably smallrate?   
3.GroudTruthAnnotationArbitration:Whohastheauthoritytoannotatethedata?Howshoulddisagreementberepresented?   
4.DataInclusionandExclusionCriteria:Whataretheposibledatasources?Howisdatacurated?Whatarethequalityconstraints?

# Case Study of Implicit Assumptions in Facial Expression Recognition

ExamplePerformance EvaluationofFERfromMollahosseinietal2016   

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Proposed Architecture</td><td rowspan=1 colspan=1>AlexNet</td></tr><tr><td rowspan=1 colspan=1>MultiPie</td><td rowspan=1 colspan=1>94.7</td><td rowspan=1 colspan=1>94.8</td></tr><tr><td rowspan=1 colspan=1>MMI</td><td rowspan=1 colspan=1>77.9</td><td rowspan=1 colspan=1>56.0</td></tr><tr><td rowspan=1 colspan=1>DISFA</td><td rowspan=1 colspan=1>55.0</td><td rowspan=1 colspan=1>56.1</td></tr><tr><td rowspan=1 colspan=1>FERA</td><td rowspan=1 colspan=1>76.7</td><td rowspan=1 colspan=1>77.4</td></tr><tr><td rowspan=1 colspan=1>SFEW</td><td rowspan=1 colspan=1>47.7</td><td rowspan=1 colspan=1>48.6</td></tr><tr><td rowspan=1 colspan=1>CK+</td><td rowspan=1 colspan=1>93.2</td><td rowspan=1 colspan=1>92.2</td></tr><tr><td rowspan=1 colspan=1>FER2013</td><td rowspan=1 colspan=1>66.4</td><td rowspan=1 colspan=1>61.1</td></tr></table>

# HowShould Facial Expressionsbe Represented?

![](/data/huangyc/Document2All/posterDataOutput_vlm/Identifying the Context Shift between Test Benchmarks and Production Data_poster/auto/images/images/fig_3.jpg)

Asthe following"basicemotioncategories:" Neutral,Hapiness,dness,nger,ea, Disgust,Surprise?Orastheemotionsonthe right from Cowen et al 2020?Or somethingelse?

Toomanydegreesoffreedom $^ { + }$ toomanyassumptions Whatdatacan serveas ground truth: posedphotographswithobservers'labels, framesfromavideowithobservers'labeled peakexpressions,self reports,mappingsof facialactionunitstocategories？When shouldwe expect themodel to generalize? What limits should beexpress?

SIGNALS Dashboard camera Pressure   
Spedometer Electrodermal activity SteeringWheel Skin temperature Faceexpression Chair 三Speed   
1 Acceleration Webcam Heartrate Keyboard reathg ate ITyping patten   
1 Camera Poture Microphone 自 Physica gestures Smartwatch speech 4四

# References

1.paperswitodecom/sota/imageclassficationon-cifar-10andpaperwihcode.com/sotaimageclsificatononigene   
2.Recht,et al.Do ImageNet ClasifiersGeneralize to ImageNet.2019.   
3.BuolamwiniandGebru.Gender Shades:IntersectionalAcuracy DiparitiesinCommercialGender Clasfication.2018   
4.Eykholt K,et al.Physicial-WorldAttackson Deep Learning Visual Clasification.2018   
5.Groh et al.EvaluatingDeep Neural Networks Trained on...2021   
6.Daneshjou et al.Disparities in Dermatology Al..2022   
7.Kosti et al.Context Based Emotion Recognition using...2019   
8.Groh et al.Deepfake Detection by Crowds,Machines,and...2022   
9.Obermeyer et al.Dissecting Racial Bias in an Algorithm...2019   
10.Winkleret al.Association Between Surgical SkinMarkings in Dermoscopic..2019   
11.Oakden-Rayner et al. Hidden Stratification Causes Clinically Meaninful...2020   
12.Pierson etal.AnAlgorithmicApproach to Reducing Unexplained...2021   
13.Kiela et al.Dynabench:Rethinking Benchmarking in NLP.2021   
14.Mollahosseini et al.Going Deeping in Facial Expression Recognition...2016   
15.Cowen et al.Sixteen Facial Expressions Occur in Similar Contexts...2020