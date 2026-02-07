# All in a Row: Compressed Convolution Networks for Graphs

Junshu Sun1.2Shuhui Wang1.3Xinzhe Han1.2Zhe Xue4Qingming Huang1,2,3

1:b e Computer Science, Beijing University of Posts and Telecommunications, China

# Motivation

# Method

# Main Results

Compared to Euclidean convolution,existing graph convolution methods generally fail to learn diverse convolution operators under limited parameter scalesand depend on additional treatments of multi-scale feature extraction. In this paper,we want to bridge the gap between Euclidean space and graph space，and therefore generalize Euclidean convolution to graphs.

Generalizing Euclidean convolution to graphs faces challenges from two aspects. From the graph perspective,they generally have irregular local structures,diferent from the grid data in Euclidean space.

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_1.jpg)  
Regular Local Structure

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_2.jpg)  
Irregular Local Structure

From the Euclidean convolution perspective,it is sensitive to the local spatial order,while GNNs should preserve permutation invariance,i.e., produce the same node representations regardless of the order of the nodes.

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_3.jpg)  
Permutation Invariance/Equivariance

# Notations

<table><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>n</td></tr><tr><td rowspan=1 colspan=1>NodeFeat.</td><td rowspan=1 colspan=1>Adjacency Mx.</td><td rowspan=1 colspan=1>DegreeMx.</td><td rowspan=1 colspan=1>DAD</td><td rowspan=1 colspan=1>All-one Vec.</td><td rowspan=1 colspan=1>NodeNum</td></tr></table>

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_4.jpg)

# Regularization on Graphs

We propose to regularize graph-structured data through learnable permutations for end-to-end GNNs.

Position Regression: Nodes with similar features or short paths in between will get closer position prediction.

Weuse the sigmoid function to approximate the sign function in backpropagation.

# Compressed Convolution Network

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_5.jpg)

Learnable permutations decouple the input order and the follow-up module,therefore we can apply either permutation-sensitive or permutationinvariant operators on graphs.

$$
\mathbf { r } _ { A } = \tilde { \mathbf { A } } ^ { t } \mathrm { M L P } ( \mathbf { X } ) , \quad \mathbf { r } = \mathrm { s g n } \left( \mathbf { r } _ { A } \mathbf { 1 } ^ { \top } - \mathbf { 1 } \mathbf { r } _ { A } ^ { \top } \right) \mathbf { 1 } .
$$

Permutation Matrix Generation:We resort to the cyclic shift to generate permutation matrices. The differentiable cyclic shift can be implemented through element-wise addition and modulus.

「he Compressed Convolution Network (CoCN) can be highlighted as:

where $\mathbf { m } \in \mathbb { R } ^ { n }$ denotes the indicator,initialized as $\pmb { \mathsf { m } } _ { j } = j$ ， $\tau$ denotes the relaxation factor.

$$
\hat { \mathsf { \bf P } } = \mathsf { e x p } \left\{ - \tau \left[ \left( \mathbf { m 1 } ^ { \top } - \mathbf { 1 r } ^ { \top } + n \right) \quad \left( \mathsf { m o d } n \right) \right] \right\} ,
$$

Diagonal convolution learns both node features and structure features explicitly.   
Diagonal convolution performs diagonal sliding on structure features to adapt to the scale of graphs.   
CoCNs directly apply hierarchical feature learning on graphs.   
The computational units of CoCNs are nodes/node sets.   
CoCNs use anti-diagonal compression to update structure features.

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_6.jpg)

# Comparison with State-of-the-Arts

Table I.Graph Classification Results (measured by accuracy:%).   

<table><tr><td></td><td>MUTAG</td><td>PROTEINS</td><td>NCI1</td><td>IMDB-B</td><td>IMDB-M</td><td>COLLAB</td></tr><tr><td>GRAPHS</td><td>188</td><td>1,113</td><td>4,110</td><td>1,000</td><td>1,500</td><td>5,000</td></tr><tr><td>AVGNODES</td><td>17.93</td><td>39.06</td><td>29.87</td><td>19.77</td><td>13</td><td>74.5</td></tr><tr><td>AVG EDGES</td><td>39.6</td><td>145.6</td><td>64.6</td><td>193.1</td><td>131.87</td><td>4,914.4</td></tr><tr><td>NODE FEATURES</td><td>7</td><td>3</td><td>37</td><td>0</td><td>0</td><td>0</td></tr><tr><td>PATCHY-SAN</td><td>88.95±4.21</td><td>75.00±2.51</td><td>78.60±1.90</td><td>71.00±2.29</td><td>45.23±2.84</td><td>72.60±2.15</td></tr><tr><td>GCN</td><td>69.50±1.78</td><td>73.24±0.73</td><td>76.29±1.79</td><td>73.26±0.46</td><td>50.39±0.41</td><td>80.59±0.27</td></tr><tr><td>GIN</td><td>81.39±1.53</td><td>71.46±1.66</td><td>80.00±1.40</td><td>72.78±0.86</td><td>48.13±1.36</td><td>78.19±0.63</td></tr><tr><td>GRAPHSAGE</td><td>83.60±9.60</td><td>73.00±4.50</td><td>76.00±1.80</td><td>68.80±4.50</td><td>47.60±3.50</td><td>73.90±1.70</td></tr><tr><td>PG-GNN</td><td></td><td>76.80±3.80</td><td>82.80±1.30</td><td>76.80±2.60</td><td>53.20±3.60</td><td>80.90±0.80</td></tr><tr><td>TOPKPOOL</td><td>67.61±3.36</td><td>70.48±1.01</td><td>67.02±2.25</td><td>71.58±0.95</td><td>48.59±0.72</td><td>77.58±0.85</td></tr><tr><td>SAGPOOL</td><td>73.67±4.28</td><td>71.56±1.49</td><td>67.45±1.11</td><td>72.55±1.28</td><td>50.23±0.44</td><td>78.03±0.31</td></tr><tr><td>ASAP</td><td>77.83±1.49</td><td>73.92±0.63</td><td>71.48±0.42</td><td>72.81±0.50</td><td>50.78±0.75</td><td>78.64±0.50</td></tr><tr><td>DIFFPOOL</td><td>79.22±1.02</td><td>76.25±1.00</td><td>62.32±1.90</td><td>73.14±0.70</td><td>51.31±0.72</td><td>82.13±0.43</td></tr><tr><td>MINCUTPOOL</td><td>79.17±1.64</td><td>74.72±0.48</td><td>74.25±0.86</td><td>72.65±0.75</td><td>51.04±0.70</td><td>80.87±0.34</td></tr><tr><td>STRUCTPOOL</td><td>79.50±0.75</td><td>75.16±0.86</td><td>78.64±1.53</td><td>72.06±0.64</td><td>50.23±0.53</td><td>77.27±0.51</td></tr><tr><td>EDGEPOOL</td><td>74.17±1.82</td><td>75.12±0.76</td><td></td><td>72.46±0.74</td><td>50.79±0.59</td><td></td></tr><tr><td>SEP</td><td>85.56±1.09</td><td>76.42±0.39</td><td>79.35±0.33</td><td>74.12±0.56</td><td>51.53±0.65</td><td>81.28±0.15</td></tr><tr><td>GMT</td><td>83.44±1.33</td><td>75.09±0.59</td><td>76.35±2.62</td><td>73.48±0.76</td><td>50.66±0.82</td><td>80.74±0.54</td></tr><tr><td>CoCN(OURS)</td><td>87.08±0.17</td><td>76.86±0.13</td><td>82.89±0.19</td><td>77.26±0.27</td><td>56.32±0.18</td><td>86.15±0.10</td></tr></table>

Table2.Node Classification Results (measured by accuracy:%).   

<table><tr><td></td><td>CHAMELEON</td><td>SQUIRREL</td><td>CORNELL</td><td>TEXAS</td><td>WISCONSIN</td><td>ACTOR</td><td rowspan="3"></td></tr><tr><td>NODES</td><td>2,277</td><td>5,201</td><td>198</td><td>183</td><td>251</td><td>7,600</td></tr><tr><td>EDGES</td><td>36,101</td><td>198,493</td><td>295</td><td>309</td><td>499</td><td>33544</td></tr><tr><td>FEATURES</td><td>2.325</td><td>2.089</td><td>1,703</td><td>1,703</td><td>1,703</td><td>932</td><td>AVGRANK</td></tr><tr><td>GCN</td><td>59.82±2.58</td><td>36.89±1.34</td><td>57.03±4.67</td><td>59.46±5.25</td><td>59.80±6.99</td><td>30.26±0.79</td><td>11.17</td></tr><tr><td>CHEBYNET</td><td>55.24±2.76</td><td>43.86±1.64</td><td>74.30±7.46</td><td>77.30±4.07</td><td>79.41±4.46</td><td>34.11±1.09</td><td>8.17</td></tr><tr><td>GEOM-GCN</td><td>60.00±2.81</td><td>38.15±0.92</td><td>60.54±3.67</td><td>66.76±2.72</td><td>64.51±3.66</td><td>31.59±1.15</td><td>10.17</td></tr><tr><td>GRAPHSAGE</td><td>49.06±1.88</td><td>36.73±1.21</td><td>80.08±2.96</td><td>82.03±2.77</td><td>81.36±3.91</td><td>35.07±0.15</td><td>7.00</td></tr><tr><td>FAGCN</td><td>46.07±2.11</td><td>30.83±0.69</td><td>76.76±5.87</td><td>76.49±2.87</td><td>79.61±1.58</td><td>34.82±1.35</td><td>9.17</td></tr><tr><td>APPNP</td><td>40.44±2.02</td><td>29.20±1.45</td><td>56.76±4.58</td><td>55.10±6.23</td><td>54.59±6.13</td><td>30.02±0.89</td><td>13.00</td></tr><tr><td>MIXHOP</td><td>60.50±2.53</td><td>43.80±1.48</td><td>73.51±6.34</td><td>77.84±7.73</td><td>75.88±4.90</td><td>32.22±2.34</td><td>8.33</td></tr><tr><td>LINKX</td><td>68.42±1.38</td><td>61.81±1.80</td><td>77.84±5.81</td><td>74.60±8.37</td><td>75.49±5.72</td><td>36.10±1.55</td><td>6.33</td></tr><tr><td>GGCN</td><td>71.14±1.84</td><td>55.17±1.58</td><td>85.68±6.63</td><td>84.86±4.55</td><td>86.86±3.29</td><td>37.54±1.56</td><td>2.50</td></tr><tr><td>ACMII-GCN</td><td>68.46±1.70</td><td>51.80±1.50</td><td>85.95±5.64</td><td>86.76±4.75</td><td>87.45±3.74</td><td>36.43±1.20</td><td>2.33</td></tr><tr><td>GPRGCN</td><td>62.59±2.04</td><td>46.31±2.46</td><td>78.11±6.55</td><td>81.35±5.32</td><td>82.55±6.23</td><td>35.16±0.90</td><td>5.17</td></tr><tr><td>GCNII</td><td>63.86±3.04</td><td>38.47±1.58</td><td>77.86±3.79</td><td>80.39±3.83</td><td>77.57±3.40</td><td>37.44±1.30</td><td>5.83</td></tr><tr><td>CoCN(OURS)</td><td>79.17±0.17</td><td>72.95±0.23</td><td>86.22±0.49</td><td>85.21±0.49</td><td>86.88±0.45</td><td>36.35±0.12</td><td>1.83</td></tr></table>

# Partial Model Study Results and Key Conclusions

Ablation studies on the number of permutations (left)，and output similarityamong different permutation heads during training (right).

![](/data/huangyc/Document2All/posterDataOutput_vlm/All in a Row: Compressed Convolution Networks for Graphs_poster/auto/images/images/fig_7.jpg)

# Takeaways:

Permutation module can permute input nodes with little information loss.The largertherelaxation factor $\tau$ becomes,the less the information loss is.   
CoCNs learn complementary feature representations under different permutations and require multiple permutations (around 8-16) for suffcient feature learning. CoCNs achieve better performance as the receptive field size increases (bounded by the number of input nodes).   
Both node features and structure features generally contribute to the model prediction.