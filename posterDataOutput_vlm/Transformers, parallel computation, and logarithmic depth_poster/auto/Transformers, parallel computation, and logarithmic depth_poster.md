# Transformers, Parallel Computation,and Logarithmic Depth

Clayton Sanforda,Daniel Hsu²,Matus Telgarskyb

a Columbia University，bNew York University

# Spotlight Paper

# Motivation

Motivating question: How can transformers be understood as models of parallel computation (e.g. MPC)?

1. Representational powers of depth? 2.Multi-step reasoning capabilities? 3.Comparisons with other models (state-space models, sub-quadratic attention transformers,GNNs)?

# Transformer Architecture

Self-attention unit: $\begin{array} { r } { f ( X ) = \operatorname { s o f t m a x } ( X Q K ^ { T } X ^ { T } ) X V } \end{array}$   
for input $\boldsymbol { X } \in \mathbb { R } ^ { N \times d }$ and model parameters   
$Q , K$ ， $V \in \mathbb { R } ^ { d \times m }$   
Multi-headed attention: $\begin{array} { r } { L ( X ) = X + \sum _ { h = 1 } ^ { H } f _ { h } ( X ) } \end{array}$   
Arbitrary element-wise encoding $( M L P + \mu$ bositional   
encoding): $\varphi ( X ) = ( \varphi ( x _ { 1 } , 1 ) , \dots , \varphi ( x _ { N } , N ) )$   
Full transformer: $T ( X ) = ( \varphi _ { D } \circ L _ { D } \circ \cdots \circ L _ { 1 } \circ \varphi _ { 0 } ) ( X )$   
Key assumptions: $m , H , L \ll N$ ；fixed precision;arbitrary $\varphi$

# Massively Paralel Computation (MPC)

Theoreticalmodel of MapReduce byKarloff,etal $^ { \prime } 1 0$ .

1. $N$ -bit input divided among $q$ machines with local memory s.   
2.For round $r = 1 , \dots R$ ： 2.1 Each machine performs some computation on its input state. 2.2Each machine simultaneously sendsand receives messages of size $\leq s$   
$( \gamma , \delta )$ -MPC protocols have local memory $s = O ( N ^ { \delta } )$ and   
global memory $q s = O ( N ^ { 1 + \gamma } )$ .

# Conjecture (1-cyclevs 2-cycle; Ghaffari, etal '19)

Any $( \gamma , \delta )$ -MPC protocol with $\delta \in ( 0 , 1 )$ that distinguishes one length- $N$ cycle from two length $\cdot \frac { N } { 2 }$ cycles uses $R = \Omega ( \log N )$ rounds.

# k-Hop Induction Heads

Induction Heads: Toy task to complete bigram via previous occurrence:IH(baebcabebdea) $= 6$

Occurs naturally in trained transformers;useful primitive for mechanistic interpretability research [Anthropic blog post]. Two-step logical reasoning task with natural two-layer transformer construction [Bietti,et al '23]. Negative result from communication complexity: Single-layer transformers cannot solve IH.

$k$ -Hop Induction Heads: Iterated variant of IH to capture $k$ -step reasoning. $\mathrm { h o p } _ { k } ( \dots \cdot \dots \partial _ { k } a _ { k + 1 } \dots \cdot \dots a _ { k - 1 } a _ { k } \dots a _ { 1 } a _ { 2 } \dots a _ { 1 } ) = a _ { k + 1 }$ baebcabebdea.

# Theory Result #1: Near-equivalence of Transformers & MPC

# Theorem (Transformers simulate MPC)

Any R-round $( \gamma , \delta )$ -MPCprotocol(with $\delta > \gamma ,$ ）canbe simulated bya transformerof depth $L = O ( R )$ and width $m = \tilde { O } ( N ^ { 4 \delta } )$

Implications: $O ( \log ( N ) )$ -depth solutions to graph connectivity，min-spanning forest,cycle check,formula evaluation,etc. Proof ldea:Simulate each machine's computations in ${ \mathsf { M L P s } } \varphi$ simulate communication with self-attention units. Subsequent improvement:Width dependence improved to $m = { O } ( N ^ { \delta + \varepsilon } )$ for any fixed $\varepsilon$ by $[ S F H + 2 4 ]$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_1.jpg)

# Theorem (MPC simulates Transformers)

Any transformer of depth $L$ and width mcan be simulated by an $( 1 + \delta , \delta )$ -MPC protocol with $R = O ( L )$ rounds, $s = O ( m )$ local memory，and $q = O ( N ^ { 2 } )$ machines.

Implications: Under 1-cycle vs 2-cycle conjecture, $L = \Omega ( \log N )$ depth is necessary to solve graph connectivity.   
Proof Idea: $O ( N )$ "token machines”compute $Q / K / V$ embeddings; $O ( N ^ { 2 } )$ “inner product   
machines"compute all $Q / K$ inner products.   
Limitation:Not exactly bidirectional relationship between theorems due to $q = O ( N ^ { 2 } )$ machine   
requirement.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_2.jpg)

# TheoryResult #2:Eficient Multi-Step ReasoningRepresentations

Construction:Transformers of depth $L = \left\lfloor \log _ { 2 } k \right\rfloor + 2$ and width $m = O ( 1 )$ can solve $k .$ -IH.

$\blacktriangleright$ First two layers solve induction heads for each input.   
$\blacktriangleright$ Subsequent layers employ“pointer doubling"to chain together solutions.   
Optimality: All transformers of width $m = { O } ( N ^ { 1 - \varepsilon } )$ that solve $k$ -IHhavedepth $L = \Omega ( \log k )$ (conditional on 1-cyclevs 2-cycle conjecture).   
$\blacktriangleright$ Reduction to MPC simulation of transformers.

# Theory Result #3:Sub-optimality of Other Architectures

Graph Neural Networks: Solving graph connectivity requires $L \sqrt { m } = \tilde { \Omega } ( N ^ { 1 / 4 } )$ [CONGEST reduction; Loukas ‘19]. State-Space Models:RNN,LSTM,Mamba solutions to $k { - } | \mathsf { H }$ requiresdepth $L \geq k$ orwidth $m = \Omega ( N / k ^ { 6 } )$ [Pointer chasing reduction； Assadi,N'21]. Sub-Quadratic Attention Transformers: Every kernel-based (e.g.Performer) or masking-based (e.g. Longformer) transformer variant that solves $k$ -IHhaseither depth $L \geq k$ or near-quadratic attention computations [Pointer chasing].

# Empirical Result #1:Log-depth k-Hop Induction Heads

Task:Multi-task $k { - } 1 \mathsf { H }$ for   
$k = 0 , 1 , \ldots , 1 6$ sequence length   
$N = 1 0 0$ .   
Models: GPT-2 transformers with embed. dim. $m = 1 2 8$ depth $L = 2 , \ldots , 6$   
Result: Low error when $L \leq \lfloor \log _ { 2 } k \rfloor$ ,as predicted by theory.

# Empirical Result #2: Interpretability of Learned Models

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_3.jpg)  
Layer 2,1-IH

16-1H attention matrices softmax $( X Q K ^ { \tau } X ^ { \tau } )$ ，with colored partial solutions

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_4.jpg)  
Layer4,2-IH

Key question: Do the   
trained transformers solve   
$k .$ -IHwith the same“pointer doubling"approachof the   
theoretical construction?   
Yes.Close correspondence between self-attention   
matrices and partial solutions to $k$ -IH.   
At least one head in the lth attention layer implements $2 ^ { \ell - 2 } \mathfrak { - } | \mathsf { H }$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_5.jpg)

# Paper Links

Layer 6,8-IH

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_6.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_7.jpg)  
(Emp.attn.matrix,theoretical $j { \mathrm { - } } 1 \mathsf { H \ m a p }$ >

Prior communication compl. $^ +$ attention paper. [SHT23], NeurlPS '23.

This paper. [SHT24].

![](/data/huangyc/Document2All/posterDataOutput_vlm/Transformers, parallel computation, and logarithmic depth_poster/auto/images/images/fig_9.jpg)  
Subsequent application to graphalgorithms. $[ S F H + 2 4 ]$