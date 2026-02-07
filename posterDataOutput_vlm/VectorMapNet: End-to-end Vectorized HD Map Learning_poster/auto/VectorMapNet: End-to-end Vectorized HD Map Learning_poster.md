# IIli VectorMapNet: End-to-end Vectorized HD Map Learning i: IC

Yicheng Liu, Tianyuan Yuan, Yue Wang, Yilun Wang, Hang Zhao

# Motivations

# VectorMapNet

# Qualitative Results

Autonomous driving systems require an understanding of map elements on the road,including lanes,pedestrian crossing,and traffic signs,to navigate around the world.

LIDAR Pairwise $\textcircled{8}$ Involves a complex pipeline   
scans alignment Globallyonsistentpointcloud Static HD map   
IMU $\textcircled{2}$ Costly and labor intensive Manual Annotation $\textcircled{8}$ Needs timely update   
odometry

In contrast, we focus on using onboard sensors, including LiDARs and cameras,to estimate map elementson-the-fly.

# Contributions

·VectorMapNet isanend-to-end mappingapproach.   
·We utilize polyline to accommodate the heterogeneous nature of map elements. Our method achieves promising performance in online semantic HD map learning tasks.

![](/data/huangyc/Document2All/posterDataOutput_vlm/VectorMapNet: End-to-end Vectorized HD Map Learning_poster/auto/images/images/fig_1.jpg)  
VectorMapNetdtndodel,issigndtoepresentmapithsparsesetofpolylinestufulatingtetasrset detection problem.In our approach,we divide the task into three distinct components

![](/data/huangyc/Document2All/posterDataOutput_vlm/VectorMapNet: End-to-end Vectorized HD Map Learning_poster/auto/images/images/fig_2.jpg)  
ABEVFeature Extractor(Avariantof IPM)thatlifts various sensormodality inputs intoacanonicalfeature space (BEV space).

(2)Amapelementdetector(DETR-likeTransformerdecoder)tatlocatesandclasifesallmapelementsbypredictingelementeypintsAi and their class labels $l _ { i }$

(3)APolylineGenerator(Vanilaransformerdecoder)thatproducesasequenceoforderedpolylineverticeshichdescribes thelocal geometry of each detected map element $A _ { i } , l _ { i }$

![](/data/huangyc/Document2All/posterDataOutput_vlm/VectorMapNet: End-to-end Vectorized HD Map Learning_poster/auto/images/images/fig_3.jpg)  
Using polylines as primitives has brought us two benefits compared with baselines:

·Polylines effectivelyencode the detailed mapgeometries,e.g.,the cornersof boundaries (red elipses).

Polyline representations prevent Modelfrom generating ambiguous results,as it consistently encodes direction information.Incontrast,Rasterized methodsare prone to falsely generating loopy curves (blue ellipses ).

# Problem Formulation

# Quantitative Results

# Centerline Generation

Similarto HDMapNet,our task is to generate vectorized mapelements usingdata from onboard sensors of autonomous vehicle,such as RGB cameras and/or LiDARs.These map elements include:

·Lane dividers:boundaries dividing lanes on the road,usuallystraight lines.   
Road boundaries:boundaries of roads separating roads and sidewalks,typically irregularly-shaped curves of arbitrary lengths. Pedestrian crossings:regions with white markings indicating legal pedestrian crossing points, typically represented aspolygons.   
Centerlines:line segments that commonly used for driving direction,vehicle positioning,and navigation.

# Why use polyline to represent maps?

Using polylines to represent map elements has three main advantages:

·Polylinesarea flexible primitive that can represent complex geometric elements in HD maps.   
·The order of polyline vertices isa natural way to encode the direction of map elements.   
·The polyline representation has been widely used by downstream tasks,such as motion forecasting.

Top-right Middle Start . Top-most Right-most Bottom-left End Lett.ostBottom-most Polyline Bounding Box SME Extreme Points

Three different keypoint representationsare proposed here.

# VectorMapNet for Motion Forecasting

Toevaluate the capacity of our method and to investigate its usefulness in downstream tasks,we put our predicted HD map to the test within a motion forecasting task.

Wereporttheaverage precision thatuses Chamferdistanceand Fréchet Distanceas the threshold.

Motion Forecasting heavily relies on precise map information for accurate prediction of future motion.

□ Results on nuScenes   

<table><tr><td>Methods</td><td>APped</td><td>APdivider</td><td>APboundary</td><td>mAP</td></tr><tr><td>STSU(Can et al., 2021)</td><td>7.0</td><td>11.6</td><td>16.5</td><td>11.7</td></tr><tr><td>HDMapNet (Camera)(Lietal.,2021)</td><td>14.4</td><td>21.7</td><td>33.0</td><td>23.0</td></tr><tr><td>HDMapNet (LiDAR) (Lietal.,2021)</td><td>10.4</td><td>24.1</td><td>37.9</td><td>24.1</td></tr><tr><td>HDMapNet (Fusion) (Li et al.,2021)</td><td>16.3</td><td>29.6</td><td>46.7</td><td>31.0</td></tr><tr><td>VectorMapNet(Camera)</td><td>36.1</td><td>47.3</td><td>39.3</td><td>40.9</td></tr><tr><td>VectorMapNet (Camera)+fine-tune</td><td>42.5</td><td>51.4</td><td>44.1</td><td>46.0</td></tr><tr><td>VectorMapNet(LiDAR)</td><td>25.7</td><td>37.6</td><td>38.6</td><td>34.0</td></tr><tr><td>VectorMapNet(Fusion)</td><td>37.6</td><td>50.5</td><td>47.5</td><td>45.2</td></tr><tr><td>VectorMapNet (Fusion) + fine-tune</td><td>48.2</td><td>60.1</td><td>53.0</td><td>53.7</td></tr></table>

□Results on Argoverse2   

<table><tr><td rowspan="2"></td><td colspan="5">Frechet Distance</td><td colspan="4">Chamfer Distance</td></tr><tr><td>#dim</td><td>APped</td><td>APdivider</td><td>APboundary</td><td>mAP</td><td>APped</td><td>APdivider</td><td>APboundary</td><td>mAP</td></tr><tr><td>Keypoint Representaion HDMapNet (Camera) (Li etal.,2021)</td><td>2</td><td>-</td><td>：</td><td>：</td><td>·</td><td>13.1</td><td>5.7</td><td>37.6</td><td>18.8</td></tr><tr><td>VectorMapNet (Camera)</td><td>2</td><td>43.2</td><td>45.5</td><td>52.0</td><td>46.9</td><td>38.3</td><td>36.1</td><td>39.2</td><td>37.9</td></tr><tr><td>VectorMapNet (Camera)</td><td>3</td><td>41.7</td><td>42.3</td><td>49.9</td><td>44.6</td><td>36.5</td><td>35.0</td><td>36.2</td><td>35.8</td></tr></table>

To demonstrate the flexibility of polyline,we expand VectorMapNettopredictcenterlines.

<table><tr><td>Model Inputs</td><td>minADE↓</td><td>minFDE↓</td><td>MR@2m↓</td></tr><tr><td>Traj.</td><td>0.909</td><td>1.577</td><td>19.6</td></tr><tr><td>Traj.+G.T.Map</td><td>0.779</td><td>1.390</td><td>18.0</td></tr><tr><td>Traj.+Pred.Map</td><td>0.826</td><td>1.477</td><td>18.2</td></tr></table>

![](/data/huangyc/Document2All/posterDataOutput_vlm/VectorMapNet: End-to-end Vectorized HD Map Learning_poster/auto/images/images/fig_4.jpg)

# A benefit of of posingmap learningasa detectionproblem:

![](/data/huangyc/Document2All/posterDataOutput_vlm/VectorMapNet: End-to-end Vectorized HD Map Learning_poster/auto/images/images/fig_5.jpg)

The model can identify pedestrian crossings at intersections thataremissed in theannotationsof the HD map provided by the dataset.

# Reference

HDMapNet:An Online HDMap Constructionand Evaluation Framework,Li etal.,ICRA2022   
Structured bird's-eye-view traffic sceneunderstanding from onboard images,Can etal.,ICCV2021