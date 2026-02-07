# Matrix Compression via Randomized Low Rank and Low Precision Factorization

Rajarshi Saha,Varun Srivastava,Mert Pilanci (Stanford University)

# Motivation

# OurAlgorithm: Low-Precision and Low Rank

·Matrices are ubiquitous -- can involve billions of elements making their storage and processing quite demanding in terms of computational resources and memory usage. Eg.: Vector databases, Kernel matrices, LLM weight matrices, etc.

·Question: How to compress matrices via dimensionality reduction and quantization?

·Several real-world matrices exhibit approximately low-rank structure due to inherent redundancy or patterns.

Algorithm 1: LPLR: Randomized Low-Precision Low-Rank factorization

Input:Matrix $\mathbf { A } \in \mathbb { R } ^ { n \times d }$ ,sketch size $_ m$ ,Quantizers Q, $\mathrm { \Delta Q ^ { \prime } }$ with dynamic ranges $\mathrm { R _ { Q } }$ , $\mathrm { R } _ { \mathrm { Q ^ { \prime } } }$ and bit-budgets B, $\mathrm { B ^ { \prime } }$ respectively.   
Output:Factorization:LR where $\mathbf { L } \doteq \mathbb { R } ^ { n \times m }$ , $\mathbf { R } \in \mathbb { R } ^ { m \times d }$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Matrix Compression via Randomized Low Rank and Low Precision Factorization_poster/auto/images/images/fig_1.jpg)

1 Sample a Gaussian sketching matrix $\mathbf { S } \in \mathbb { R } ^ { d \times m }$ with entries $S _ { i j } \sim { \mathcal { N } } \left( 0 , { \frac { 1 } { m } } \right)$   
2 Compute an approximate basis of column space of A by forming the sketch:AS.   
3 Quantize the approximate basis with $\mathrm { Q }$ to get Q(AS).   
4Find $\mathbf { W } ^ { * } = \arg \operatorname* { m i n } _ { \mathbf { W } }$ $\| \mathbf { Q } ( \mathbf { A S } ) \mathbf { W } - \mathbf { A } \| _ { \mathbf { F } } ^ { 2 } = \mathbf { Q } ( \mathbf { A S } ) ^ { \dagger } \mathbf { A }$   
5Quantize $\mathbf { W } ^ { * }$ using quantizer $\mathrm { \bf Q ^ { \prime } }$ to get $\mathbf { { Q } ^ { \prime } } ( \mathbf { { W } ^ { * } } )$   
6return Low-rank and low-precision approximation LR where $\mathbf { L } = \mathbf { Q } ( \mathbf { A } \mathbf { S } )$ , $\mathbf { R } = \mathbf { Q } ^ { \prime } ( \mathbf { W } ^ { * } )$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Matrix Compression via Randomized Low Rank and Low Precision Factorization_poster/auto/images/images/fig_2.jpg)

·We factorize, $\mathbf { A } \approx \mathbf { L R }$ , where the entries of $\mathbf { L }$ and $\mathbf { R }$ are quantized with $\mathbf { B }$ and $\mathbf { B ^ { \prime } }$ bits per entry respectively.   
·Compression ratio with respect to naive quantization (uniformly allocate ${ \bf { B _ { n q } } }$ bits per entry) is $\frac { m n \mathrm { B } + m d \mathrm { B } ^ { \prime } } { n d \mathrm { B } _ { \mathrm { n q } } }$   
·By tuning sketch-size we can ensure compression ratio $\leq 1$ for $\mathtt { B } _ { \mathtt { n q } } = 1$ , while letting B and $\mathsf { B } ^ { \prime }$ to take values allowed by current hardware-primitives, e.g.,4-- bits,8--bits,etc.   
·Low-precision computations are faster: Computing $\mathbf { A x }$ versus $\mathbf { L } ( \mathbf { R x } )$

Leverage the approximate low-rank structure while quantizing matrices

# Randomized Embeddings

# Data compression and Nearest Neighbors

# Compression of Large Language Models

![](/data/huangyc/Document2All/posterDataOutput_vlm/Matrix Compression via Randomized Low Rank and Low Precision Factorization_poster/auto/images/images/fig_3.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Matrix Compression via Randomized Low Rank and Low Precision Factorization_poster/auto/images/images/fig_4.jpg)

$$
( 1 - \epsilon ) \| { \mathbf z } \| _ { 2 } \le \| { \mathbf S } { \mathbf z } \| _ { 2 } \le ( 1 + \epsilon ) \| { \mathbf z } \| _ { 2 } \ \forall { \mathbf z } \in \mathcal { V }
$$

<table><tr><td colspan="3">B=B&#x27;=8bits,Bnq=4bits</td></tr><tr><td>Metric</td><td>LPLR</td><td>LPLR-SVD</td><td>Naive Quant.</td></tr><tr><td>Mean</td><td>0.672</td><td>0.537</td><td>0.836</td></tr><tr><td>Std Dev</td><td>0.080</td><td>0.079</td><td>0.470</td></tr></table>

Compressinga brain MRI. $\mathrm { B } = 4$ ， $\mathrm { B } ^ { \prime } = 8$ ， $\mathrm { B _ { n q } } = 1$ , $m = 1 2 4$ ， $n = 1 5 3 4 d = 1 4 3 3$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Matrix Compression via Randomized Low Rank and Low Precision Factorization_poster/auto/images/images/fig_5.jpg)

Compressing the weight matrices of LlaMa.We consistently observe better Frobeniusnormerror, except for specific layers.

Subspace embeddings: Norm of vectors in therange space is approximately preserved with high probability when $m \gtrsim \epsilon ^ { - 2 } \mathrm { r a n k } ( \mathbf { A } )$ Critical dimension, $_ m$ does not depend on original dimension, $_ n$

DSVD: Computes the best rank-kapproximation and quantize the factors independently.   
LSVD: Variant of LPLR that computes exact SVD instead of randomized SVD.

· For a given data matrix $\mathbf { A } \in \mathbb { R } ^ { n \times d }$ and a query $\mathbf { x } \in \mathbb { R } ^ { d }$ ,retrieve

$$
i ^ { * } = \mathrm { a r g m a x } _ { i \in [ n ] } ( \mathbf { A } \mathbf { x } ) _ { i } \ \approx \ \mathrm { a r g m a x } _ { i \in [ n ] } ( \mathbf { L } \mathbf { R } \mathbf { x } ) _ { i }
$$

# Approximation Error Guarantees

Applications: Semantic search over vector databases (music recommendation), In-context learning for LLMs,etc.

Table 1: Comparison with baselines (row-norm bound is constant,i.e., $\| \mathbf { a } ^ { ( i ) } \| = \mathsf { O } ( 1 ) )$ $k , m \ll \operatorname* { m i n } \{ d , n \}$ $\boldsymbol { n } .$ no. of rows, $d \mathbf { \cdot }$ no. of columns, $_ m$ ：sketch size,e:error tolerance, $\delta = k / ( m - k - 1 )$ .The expressions for bit-budget (per entry) ignores constant multiplicative factors inside the $\log _ { 2 } ( \cdot )$ .We assume $n \geq d$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Matrix Compression via Randomized Low Rank and Low Precision Factorization_poster/auto/images/images/fig_6.jpg)

Table 5:CIFAR100 embeddings generated by MobileNetV3 with anunquantized accuracyand F1 score $7 6 \%$ :Results on LPLR and LPLR-SVD with $\mathrm { B } = \mathrm { B } ^ { \prime } = 8$ bits   

<table><tr><td></td><td colspan="4">Frobenius Norm Error</td><td colspan="4">Accuracy (%)</td><td colspan="4">Weighted F1 Score (%)</td></tr><tr><td>Bnq</td><td>LPLR</td><td>LSVD</td><td>DSVD</td><td>NQ</td><td>LPLR</td><td>LSVD</td><td>DSVD</td><td>NQ</td><td>LPLR</td><td>LSVD</td><td>DSVD</td><td>NQ</td></tr><tr><td></td><td>1.04</td><td>1.08</td><td>1.09</td><td>6.75</td><td>79</td><td>82</td><td>82</td><td>1</td><td>79</td><td>82</td><td>82</td><td>0</td></tr><tr><td>124</td><td>1.08</td><td>1.1</td><td>1.12</td><td>2.18</td><td>80</td><td>80</td><td>80</td><td>1.7</td><td>80</td><td>80</td><td>80</td><td>1.3</td></tr><tr><td></td><td>1.11</td><td>1.12</td><td>1.14</td><td>1.17</td><td>79</td><td>78</td><td>77</td><td>75</td><td>79</td><td>78</td><td>78</td><td>75</td></tr></table>

<table><tr><td>Algorithms</td><td>Approximation error</td><td>Bit-budget (per entry)</td><td>Computation</td></tr><tr><td>Naive uniform</td><td>E</td><td>log (nd)</td><td>O(nd)</td></tr><tr><td>Direct-SVD</td><td>|Ak-A²+∈</td><td>（²nd) 10g2 E</td><td>O(nd²)</td></tr><tr><td>LPLR (ours)</td><td>(1+δ)|A-Al²+∈</td><td>K(AK)Knm 1og2 /log mn2 E a E</td><td>O(ndm)</td></tr></table>

Random Embeddings (e.g., Gaussian) also help in quantization by reducing the dynamic range.

Table 6: IMDB embeddings generated by BERT with anunquantized accuracy and F1 score $7 5 \%$ and $7 4 \%$ respectively:Resultson LPLRandLPLR-SVD with $\mathrm { B } = \bar { \mathrm { B ^ { \prime } } } = 8$ bits   

<table><tr><td></td><td colspan="4">Frobenius Norm Error</td><td colspan="4">Accuracy (%)</td><td colspan="4">WeightedF1 Score (%)</td></tr><tr><td>Bnq</td><td>LPLR</td><td>LSVD</td><td>DSVD</td><td>NQ</td><td>LPLR</td><td>LSVD</td><td>DSVD</td><td>NQ</td><td>LPLR</td><td>LSVD</td><td>DSVD</td><td>NQ</td></tr><tr><td>1</td><td>0.313</td><td>0.241</td><td>0.229</td><td>6.63</td><td>73</td><td>74</td><td>75</td><td>50</td><td>74</td><td>74</td><td>75</td><td>33</td></tr><tr><td></td><td>0.235</td><td>0.178</td><td>0.161</td><td>1.016</td><td>74</td><td>74</td><td>74</td><td>50</td><td>74</td><td>74</td><td>74</td><td>50</td></tr><tr><td>4</td><td>0.148</td><td>0.122</td><td>0.098</td><td>0.417</td><td>75</td><td>74</td><td>75</td><td>73</td><td>74</td><td>74</td><td>75</td><td>73</td></tr></table>

R．Saha，V.Srivastava，M.Pilanci，"Matrix Compression via Randomized Low Rank and Low Precision Factorization",37th Conference on Neural Information Processing Systems (NeurlPS),2023.

$\| \mathbf { S } \mathbf { x } \| _ { \infty } \leq  { \operatorname { O } \left( \frac { \| \mathbf { x } \| _ { 2 } } { \sqrt { d } } \right) }$