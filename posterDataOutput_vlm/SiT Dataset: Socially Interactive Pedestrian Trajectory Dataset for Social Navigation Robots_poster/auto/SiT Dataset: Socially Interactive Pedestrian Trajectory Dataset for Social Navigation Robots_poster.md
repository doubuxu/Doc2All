# SiT Dataset : Socially Interactive Pedestrian Trajectory Dataset for Social Navigation Robots

Jongwook Bae Jungho Kim Junyong Yun ChangwonKang Jeongseon Choi KimChanhyeok Junho Lee Jun Won Choi\* SPA Laboratory,epartmentof rtificial Intelligence,Hanyang Unversityeoul, Republicof Koea

# Contributions

# Robot Setup

# Tasks and Benchmark

# √Static collection

■ Many pedestrian trajectory datasets were collected from fixed positions, limiting variability.

# √ Missing ego motion

■ Many existing robot datasets lack ego-motion information.

# Vehicle-centric bias

■ Most autonomous datasets were collected from vehicles, exhibiting a gap from realistic robot-pedestrian interaction behavior.

\*+: Multi - layered map   

<table><tr><td>Dataset</td><td>Platform</td><td>Task</td><td>Sync.</td><td>Map</td><td>E2E</td><td>Location</td></tr><tr><td>UCY</td><td>Fixed</td><td>Tracking,Prediction</td><td>-</td><td></td><td></td><td>Outdoor</td></tr><tr><td>ETH</td><td>Fixed</td><td>Tracking, Prediction</td><td>-</td><td></td><td></td><td>Outdoor</td></tr><tr><td>SDD</td><td>Fixed</td><td>Tracking, Prediction</td><td>-</td><td></td><td></td><td>Outdoor</td></tr><tr><td>CITR-DUT</td><td>Fixed</td><td>Tracking,Prediction</td><td>-</td><td></td><td></td><td>Outdoor</td></tr><tr><td>nuScenes</td><td>Vehicle</td><td>Detection,Tracking,Prediction</td><td>=</td><td>羊</td><td></td><td>Outdoor</td></tr><tr><td>Waymo Open</td><td>Vehicle</td><td>Detection,Tracking,Prediction</td><td></td><td></td><td></td><td>Outdoor</td></tr><tr><td>Argoverse</td><td>Vehicle</td><td>Detection,Tracking,Prediction</td><td></td><td></td><td>√</td><td>Outdoor</td></tr><tr><td>JRDB</td><td>Robot</td><td>Detection, Tracking</td><td></td><td></td><td></td><td>Indoor&amp;Outdoor</td></tr><tr><td>STCrowd</td><td>Fixed</td><td>Detection,Tracking,Prediction</td><td>√</td><td></td><td></td><td>Outdoor</td></tr><tr><td>SiT(Ours)</td><td>Robot</td><td>Detection, Tracking, Prediction</td><td>√</td><td>&lt;+</td><td>√</td><td>Indoor &amp; Outdoor</td></tr></table>

# Overview

# Real-world context

■ Collected data from dense areas like campuses and public roads /Comprehensive data ■Sequential raw data from various sensors ■ 60 scenes with 6OK images and 12K point cloud frames at $1 0 \mathsf { H z }$ ■2D and 3D bounding boxes for 6 classes

# √Unique features

■Emphasis on Human-Robot Interactions (HRl) Precise multi-sensor synchronization ■ Multi-layered indoor & outdoor semantic maps from SLAM ■ Cover tasks from 3D detection to motion forecasting (end-to-end)

# √Multi-sensors equipped on UGV

■ 1 x Husky UGV platform ■ 2 x Velodyne VLP-16 5x Basler a2A1920-51gc cameras ■1xMTi-680G IMU& RTK ■ 1 x VectorNav VN-100 IMU

![](/data/huangyc/Document2All/posterDataOutput_vlm/SiT Dataset: Socially Interactive Pedestrian Trajectory Dataset for Social Navigation Robots_poster/auto/images/images/fig_1.jpg)

# Details of SiT Dataset

![](/data/huangyc/Document2All/posterDataOutput_vlm/SiT Dataset: Socially Interactive Pedestrian Trajectory Dataset for Social Navigation Robots_poster/auto/images/images/fig_2.jpg)

# √Comparison with other datasets

# Benchmark

# √Perception tasks

■ 3D Object Detection based on image or point clouds   
3D Multi-Object Tracking Trajectory Prediction   
End-to-End 3D Detection to Motion Forecasting

■ Plan to release benchmarks and pre-trained models. ■ Challenges open on Eval.Al (Feb.2024)

# Samples of dataset

√Real-world captures   
■Candid shots from diverse urban environments   
√3D visualization   
■ Dynamic representations of objects and trajectories   
√Semantic maps   
■ 12 Color-coded layouts detailing regions

![](/data/huangyc/Document2All/posterDataOutput_vlm/SiT Dataset: Socially Interactive Pedestrian Trajectory Dataset for Social Navigation Robots_poster/auto/images/images/fig_3.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/SiT Dataset: Socially Interactive Pedestrian Trajectory Dataset for Social Navigation Robots_poster/auto/images/images/fig_4.jpg)