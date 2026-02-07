# How Do Nonlinear Transformers Acquire Generalization-Guaranteed CoT Ability?

Hongkang ${ \mathsf { L } } { \mathsf { i } } ^ { 1 }$ ，MengWang1,SongtaoLu²，XiaodongCui²，Pin-Yu Chen2 1:Rensselaer Polytechnic Institute;2:IBM Research

# Overview

# Theoretical results

$\spadesuit$ Theoretically characterize how training Transformers can enable chain-of thought (CoT). $\spadesuit$ Quantitative analysis of how context examples affect CoT performance. Theoretical study of why CoT outperforms ICL.

# Background and motivation

Standard Prompting Chain-of-Thought Prompting Model input Model Input   
Q:Rogerhas5tennis balls.He buys2more cansof Q:Roger has5 tennis balls.He buys2 more cans of   
tennis balls.Eachcan has3tennisballs.Howmany tennis balls.Eachcanhas3tennis ball.Howmany   
tennis balls does he have now? tennis balls does he have now?   
A:The answer is 11. A:Roger started with5 balls.2cans of3tennis balls eachis6tennis balls.5+6=11.The answer is11.   
Q:Thecafeteria had23apples.If they used 20 to   
makelunchand bought6more,howmanyapples Q:The cafeteria had23apples.If theyused20to   
do they have？ make lunchand bought6more,howmany apples do they have？ Model Output Model Output   
A:The answeris27. A:The cafeteria had 23 apples originall. They used 20 tomakelunch.Sothey had23-20=3.They bought6moreapples,sothey have3+6=9.The answeris9.

CoTaugments $K$ -step reasoningexamplesto the query for generation,i.e.,an extension of incontext learning (ICL) by multi-step examples.

Existing works [1,2,3]: the expressive power. The problem of why a Transformer can be trained to conduct CoT is less investigated.

# Problem formulation

Study learning $K$ -step reasoning tasks. Each task $f$ is a composition of $\left\{ f _ { i } \right\} _ { \mathrm { { i } } = 1 } ^ { K } { } _ { \mathrm { { i } } = 1 }$ and outputs $\left\{ { z _ { i } } \right\} ^ { K } _ { \mathrm { i } = 1 }$ for the input $z _ { 0 } = x _ { q u e r y }$ ,where $z _ { k } = f _ { k } ( z _ { k - 1 } )$

Learning model: one-layer Transformer $F ( P ) =$ $\begin{array} { r } { \sum _ { i } W _ { V } \widetilde { p _ { i } } s o f t m a x \left( ( W _ { K } \widetilde { p _ { i } } ) ^ { \top } W _ { Q } \widetilde { p } _ { q u e r y } \right) } \end{array}$ ,where $P$ is the input prompt, $\tilde { p } _ { i }$ is $p _ { i }$ with positional encoding.

Training: Following theoretical works [4,5] for $1 C L$ we aim to solve an empirical risk minimization by stochastic gradient descent with squared loss. Each Training prompt consists of context examples and a query. Each example $P = \left( { \begin{array} { l } { x _ { 1 } \ y _ { i , 1 } \dots y _ { i , K - 1 } } \\ { y _ { i , 1 } y _ { i , 2 } \dots y _ { i , K } } \end{array} } \right)$ has $K$ steps,where $y _ { i , s } = f _ { k } ( y _ { i , s - 1 } )$ .The query contains the first $k \in [ K ]$ steps of the reasoning.

CoT Inference: The testing prompt consists of examples and a query.The query contains one step. CoT repeats the two steps below for $K$ steps.

$\triangleright$ Greedy decoding to generate the next step.   
$\triangleright$ Add the generation to the end of the prompt.

CoT generalization error: average O-1 error of $K$ steps.

ICL Inference: The testing examples only contain the input and the final-step output.The generalization erroristheaverage O-1error.

[1]Lietal.Dissecting Chain-of-Thought: Compositionality through In-Context Filtering and Learning.   
Neurips 2023.   
[2] Fengetal.Towards Revealing the Mystery behind Chain of Thought:ATheoretical Perspective.   
Neurips2023 [3] Lietal.Chain of Thought Empowers Transformers to Solve Inherently Serial Problem.ICLR2024.   
[4] Huang et al.In-context convergence of transformers.ICML2024.   
[5]Zhang et al.Trained transformers learn linear models in-context.JMLR 2024.

Data&Tasks:The training and testing data are formulated by training/testing-relevant (TTR/TSR) patterns $\{ \mu _ { i } \} _ { i = 1 } ^ { M }$ and $\{ \mu _ { i } ^ { \prime } \} _ { i = 1 } ^ { M \prime }$ $\mathsf { T S R } \in$ span{TRR}. Consider erroneous testing prompts: reasoningin someexamplescontains incorrect steps.For task $f$ ，

$\alpha$ (or $\alpha ^ { \prime }$ ): the fraction of contexts with inputs thatshare the same TRR (or TSR) patterns as the query. $\tau ^ { f }$ : the fraction of accurate context examples. $\rho ^ { f }$ : the normalized gap of accurate over the most likely inaccurate reasoning steps.

Theorem1(Convergence):With the numberof context examples and iterations linear in $\Omega ( \alpha ^ { - 1 } )$ the population risk is $\le { \cal O } ( \epsilon )$

Theorem 2 (CoT Generalization):To achieve a zero CoT error,the number of context examples for task $f$ is proportional to $\left( \alpha ^ { \prime } \tau ^ { f } \rho ^ { f } \right) ^ { - 2 }$ .The CoT performance is improved with

More accurate reasoning examples, More similar examples to the query.

Theorem 3 (Comparison with ICL):The success of ICL requires a dominant fraction of correct input-label examples in the testing prompt (Condition 1), but CoT does not.

# The mechanism of CoT

Proposition 1: The attention weights is concentrated on prompt columns with the same TSR pattern and the step index as the query step.This leads to a correct prediction in each reasoning step.

Transformers Provably Implement CoT by Attending to the Most Similar Examples Every Step.

largest fraction greedy decoding same TSR,same step diff.TSR diff.step 4   
Attn:0.3 0.3 0.3 0.02 0.02 ↑ ↑ WK WQ   
step:12 12 12 12 12 H1 μ1μ2μ3 μ1H4μ5 μ1μ2μ3 K5μ1μ6 μ query Context examples of 2-steps reasoning labels:μ1.μ2

# Numerical experiments

Condition 1 is crucial for the success of ICL but not for CoT. Training dynamics of CoT: same TSR & step matter.

100 10-1 10-2 CoTw.o.Condition1 ICL w.Condition1 ICL w.o.Condition 1 020406080100 #of context examples

1.0 0.8 0.6 same TSR,same step same TSR,diff.step 0.4 0.2 0.0 0 2004006008001000 Iterations