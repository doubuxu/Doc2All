# On the convergence of mSGD and AdaGrad for stochastic optimization

# Algorithms:

SGD: $\theta _ { n + 1 } = \theta _ { n } - \epsilon _ { n } \nabla _ { \theta _ { n } } g ( \theta _ { n } , \xi _ { n } )$

mSGD: $\boldsymbol { v } _ { n } = \alpha \boldsymbol { v } _ { n - 1 } + \epsilon _ { n } \nabla _ { \boldsymbol { \theta } _ { n } } g ( \boldsymbol { \theta } _ { n } , \boldsymbol { \xi } _ { n } ) , \ \boldsymbol { \theta } _ { n + 1 } = \boldsymbol { \theta } _ { n } - \boldsymbol { v } _ { n }$

AdaGrad:0n+1-0n- $\theta _ { n + 1 } - \theta _ { n } - { \frac { 1 } { \sqrt { \sum _ { t = 1 } ^ { n } \| \nabla _ { \theta _ { n } } g ( \theta _ { n } , \xi _ { n } ) \| ^ { 2 } } } } \nabla _ { \theta _ { n } } g ( \theta _ { n } , \xi _ { n } )$

# Contributions:

·We prove that the iterates of mSGDare asymptotically convergent toa connected set of stationary points for possibly non-convex loss function almost surely (i.e.,with probability one),which is more general than existing works on subsequence convergence. ·We quantify the convergence rate of mSGD for the loss functions. Through this convergence rate we can get a theoretical explanation of why mSGDcan be seen as an acceleration of SGD.Moreover,we provide the convergence rate of mean-square gradientsand connect it to the convergence of time averages. We prove the iterates of AdaGrad are asymptotically convergent to a connected set of stationary points almost surely for possible non-convex loss functions.The convergence result for the AdaGrad extends the subsequence convergence in the literature.

$$
\begin{array} { r } { \mathbb { E } \left( \| \nabla _ { \theta _ { n } } g ( \theta _ { n } ) \| ^ { 2 } \right) = O \left( e ^ { - \sum _ { i = 1 } ^ { n } \frac { s } { p } \varepsilon _ { i } } \right) . } \end{array}
$$

# Main assumptions:

Assumption1 Noise sequence $\left\{ \xi _ { n } \right\}$ are mutually independent and independent of $\theta _ { 1 }$ and $\nu _ { 0 }$ such that $\bar { g ( x ) } = \mathbb { E } _ { \xi _ { n } } \left( g ( x , \xi _ { n } ) \right)$ for any $\boldsymbol { x } \in \mathbb { R } ^ { N }$

Assumption2(Loss function assumption)Loss function $g ( \theta )$ satisfies thefollowing conditions:

1 $g ( \theta )$ isanon-negative and continuously differentiable function.

2）The set of stationary points of $\| \nabla _ { \theta } g ( \theta ) \|$ is not an empty set,thatis

$$
J : = \{ \theta | \| \nabla _ { \theta } g ( \theta ) \| = 0 \} \neq \emptyset
$$

3） $\nabla _ { \boldsymbol { \theta } } g ( \boldsymbol { \theta } )$ satisfestheipschitcondition,e,ereislr $c > 0 ,$ such that for any $x , y \in \mathbb { R } ^ { N }$

4) There is a scalar $M > 0$ such that for any $\boldsymbol \theta \in \mathbb { R } ^ { N }$ and positive integer n,

$$
\mathbb { E } _ { \xi _ { n } } \left( \left\| \nabla _ { \theta } g ( \theta ) - \nabla _ { \theta } g ( \theta , \xi _ { n } ) \right\| ^ { 2 } \right) \leq M \big ( 1 + g ( \theta ) \big ) .
$$

Assumption3 Momentumcoefficient $\alpha \in [ 0 , 1 )$ and the sequence ofstep sizeεn is positive,monotonicallydeeigt $\begin{array} { r } { \sum _ { n = 1 } ^ { + \infty } \varepsilon _ { n } = + \infty a n d \sum _ { n = 1 } ^ { + \infty } \varepsilon _ { n } ^ { 2 } < + \infty } \end{array}$

Assumption 4 (Loss function assumption) Lossfunction $g ( \theta )$ satisfies thefollowing conditions:

1 $g ( \theta )$ isanon-negativeandcontinuouslydifferentiable function.The setofitsstationarypoints $J = \{ \theta | \| \nabla _ { \theta } g ( \theta ) \| = 0 \}$ isaboundedsetwhichhasonlyfiniteconnectedcomponents $J _ { 1 } , \ldots , J _ { n } .$ , In addition,hreis $\varepsilon ^ { \prime } > 0 ,$ such that for any $i \in \{ 1 , 2 , \ldots , n \}$ and $0 < d ( \theta , J _ { i } ) < \varepsilon ^ { \prime }$ ,itholdsthat $\left| g ( \theta ) - g _ { i } \right| \neq 0 ,$ where $g _ { i } = \{ g ( \theta ) | \theta \in J _ { i } \}$ isaconstant.

2）For any $i \in \{ 1 , 2 , \ldots , n \}$ ,itholdsthat

$$
\operatorname* { l i m } _ { d ( \theta , J _ { i } ) \to 0 } \frac { | | \nabla _ { \theta } g ( \theta ) | | ^ { 2 } } { g ( \theta ) - g _ { i } } \ge s > 0 .
$$

Assumption5 Loss function $g ( \theta )$ inequation5satisfies thefollowingconditions:

$I )$ $g ( \theta )$ isanon-negativeand continuously differentiablefunction.The setof itsstationary points $J = \{ \pmb { \theta } | \| \nabla _ { \pmb { \theta } } g ( \pmb { \theta } ) \| = 0 \}$ isabounded setwhich hasonlyfiniteconnectedcomponents $J _ { 1 } , . . . , J _ { n } .$ In addition,thereisε $> 0 ,$ such that foranyiand $0 < d ( \theta , J _ { i } ) < \varepsilon _ { 1 }$ ,itholdsthat $\left| g ( \theta ) - g _ { i } \right| \neq 0 ,$ where $g _ { i } = \{ g ( \theta ) | \theta \in J _ { i } \}$ isaconstant.

2）The gradient $\nabla _ { \boldsymbol { \theta } } g ( \boldsymbol { \theta } )$ satisfiestheLipschitzcondition,i.e.foranyx,yRN,

$$
\left\| \nabla _ { x } g ( x ) - \nabla _ { y } g ( y ) \right\| \leq c \| x - y \|
$$

3）There are two constants $M ^ { \prime } > 0$ and $a > 0$ such that for any0∈RNandn∈N,

$$
E _ { \xi _ { n } } \Big ( \big \| \nabla _ { \theta } g ( \theta , \xi _ { n } ) \big \| ^ { 2 } \Big ) \leq M ^ { \prime } \big \| \nabla _ { \theta } g ( \theta ) \big \| ^ { 2 } + a .
$$

# Main results:

Theorem1 Consider themSGDinequation3. If Assumptions $_ { I - 3 }$ hold,thenfor $\forall \boldsymbol { \theta } _ { 1 } \in \mathbb { R } ^ { N }$ and $\forall \nu _ { 0 } \in \mathbb { R } ^ { N }$ ,thereexistsa connected set $J ^ { * } \subseteq J$ such that the iterate $\theta _ { n }$ is convergent to the set $J ^ { * }$ almost surely,i.e.,

$$
\operatorname* { l i m } _ { n  \infty } d ( \theta _ { n } , J ^ { * } ) = 0 , \qquad a . s .
$$

where $d ( x , J ^ { * } ) = \operatorname* { i n f } _ { y } \{ \| x - y \| , y \in J ^ { * } \}$ denotes the distance between point x and set $J ^ { * }$

Theorem2 Consider the mSGD in equation3with thenoise following auniform sampling distribution.If Assumptions $_ { I - 4 }$ hold,for $\forall \nu _ { 0 } \in \mathbb { R } ^ { N }$ and $\forall \theta _ { 1 } \in \mathbb { R } ^ { N }$ ,itholdsthat

$$
\mathbb { E } \left( \Vert \nabla _ { \theta _ { n } } g ( \theta _ { n } ) \Vert ^ { 2 } \right) = O \left( e ^ { - \sum _ { i = 1 } ^ { n } \frac { s \varepsilon _ { i } } { p ( 1 - \alpha ) ^ { 2 } } } \right) ,
$$

where $p = \exp \left\{ \sum _ { k = 1 } ^ { \infty } M \varepsilon _ { k } ^ { 2 } \right\}$ and M seind in codin $^ { 4 ) }$ of suprio

In Theorem2,let $\alpha = 0$ ,then we can obtain the convergence rate of SGD,

Theorem3 Consider the AdaGrad in equation5.If Assumptions $I$ and5hold,then for $\forall \theta _ { 1 } \in \mathbb { R } ^ { N }$ and $S _ { 0 } = 0$ thereexists $a$ connected component of the set $J ^ { * } \subseteq J ,$ suchthat the estimate $\theta _ { n }$ is convergent to the set $J ^ { * }$ almost surely,i.e.,

$$
\operatorname* { l i m } _ { n  \infty } d ( \theta _ { n } , J ^ { * } ) = 0 . \qquad a . s .
$$

Xingkang He, University of Notre Dame

# Proof outline for Theorems 1-2:

The proof is inlight of theLyapunov method.We aimto prove that $g ( \theta _ { n } )$ is convergent a.s.,and then toprove $\nabla _ { \theta _ { n } g } ( \theta _ { n } )  0 a . s$ With these two results,we are able to get $\theta _ { n }  J ^ { * } \thinspace a . s .$ In the following, weprovide the proof outline to show how to obtain the provided results of mSGD.

Step1:We prove mSGD is a stable algorithm,i.e., $\mathbb { E } ( g ( \theta _ { n } ) ) < K < + \infty , \forall n$ inLemma1.The idea is to prove that a weighted sum of the loss function value,i.e.,

$$
U _ { n } : = \sum _ { t = 1 } ^ { n } \left( 1 / ( 2 - \alpha ) \right) ^ { n - t } \mathbb { E } \left( 1 + g ( \theta _ { t + 1 } ) \right)
$$

is bounded through a recursion formula (a rough form)

$$
U _ { n } - U _ { n - 1 } \leq A \alpha ^ { n } + \underbrace { B \sum _ { t = 1 } ^ { n - 1 } \left( 1 / ( 2 - \alpha ) \right) ^ { n - t } \varepsilon _ { t } ^ { 2 } \mathbb { E } \left\| \nabla _ { \theta _ { t } } g ( \theta _ { t } , \xi _ { t } ) \right\| ^ { 2 } } _ { I } ( A , B a r e t w o c o n s t a n t s ) .
$$

Then we apply Assumption 24) to $I$ and then obtain

$$
U _ { n } - U _ { n - 1 } \leq A \alpha ^ { n } + B \underset { t = 1 } { \underbrace { \sum _ { t = 1 } ^ { n - 1 } \left( 1 / ( 2 - \alpha ) \right) ^ { n - t } \varepsilon _ { t } ^ { 2 } \mathbb { E } \left( 1 + g ( \theta _ { t } ) \right) } } \left( A , B a r e t w o c o n s t a n t s \right) .
$$

Combining $U _ { n - 1 }$ and $R$ leads to

$$
F _ { n } - F _ { n - 1 } \leq A \alpha ^ { n } + B ^ { \prime } \left( { \frac { 1 } { 2 - \alpha } } \right) ^ { n } ( A , B ^ { \prime } a r e t w o c o n s t a n t s ) ,
$$

where

$$
F _ { n } : = \sum _ { t = 1 } ^ { n } \left( \frac { 1 } { 2 - \alpha } \right) ^ { n - t } Z ( t + 1 ) \mathbb { E } \left( e _ { t + 1 } ^ { ( n ) } \big ( 1 + g \big ( \theta _ { t + 1 } \big ) \big ) \right)
$$

and

$$
Z ( t ) = \prod _ { k = i } ^ { + \infty } ( 1 + M _ { 0 } \varepsilon _ { k } ^ { 2 } ) = ( 1 + M _ { 0 } \varepsilon _ { t } ^ { 2 } ) \prod _ { k = t + 1 } ^ { + \infty } ( 1 + M _ { 0 } \varepsilon _ { k } ^ { 2 } ) = ( 1 + M _ { 0 } \varepsilon _ { t } ^ { 2 } ) Z ( t + 1 ) .
$$

Thus,we are able to obtain $\begin{array} { r } { E \big ( g \big ( \theta _ { n } \big ) \big ) < F _ { n - 1 } \leq A \sum _ { t = 1 } ^ { + \infty } \alpha ^ { t } + B \sum _ { t = 1 } ^ { + \infty } \big ( 1 / ( 2 - \alpha ) \big ) ^ { t } < + \infty . } \end{array}$

Step 2:FromLemmalandthecondition $\textstyle \sum _ { t = 1 } ^ { + \infty } \varepsilon _ { n } ^ { 2 } < + \infty$ ,we are able to prove that $\scriptstyle \sum _ { t = 1 } ^ { n } \| \nu _ { t } \| ^ { 2 }$ and $\Sigma \varepsilon _ { t } \| \nabla _ { \theta _ { t } } g ( \theta _ { t } ) \| ^ { 2 }$ are convergent a.s.respectively,as stated inLemma 7and Lemma 8.

Step3:We divide $g ( \theta _ { n } )$ into three terms

$$
g ( \theta _ { n } ) = \sum _ { t = 1 } ^ { n } A ( n ) \| \nu _ { t } \| ^ { 2 } + \sum _ { t = 1 } ^ { n } B _ { n } \varepsilon _ { t } \| \nabla _ { \theta _ { n } } g ( \theta _ { n } ) \| ^ { 2 } + \sum _ { t = 1 } ^ { n } C _ { n } ^ { T } ( \nabla _ { \theta _ { n } } g ( \theta _ { n } , \xi _ { n } ) - \nabla _ { \theta _ { n } } g ( \theta _ { n } ) ) .
$$

From Lemma7and Lemma 8,we are able to prove that $\begin{array} { r l } { \quad } & { { } \sum _ { t = 1 } ^ { n } A ( n ) \| \nu _ { t } \| ^ { 2 } + \sum _ { t = 1 } ^ { n } B _ { n } \varepsilon _ { t } \| \nabla _ { \theta _ { n } } g ( \theta _ { n } ) \| ^ { 2 } } \end{array}$ is convergenta.s.Fromtheconvergence theoremformartingale-difference sum(Lemma5),weprove that $\begin{array} { r l } { \sum _ { t = 1 } ^ { n } C _ { n } ^ { T } ( \nabla _ { \theta _ { n } } g ( \theta _ { n } , \xi _ { n } ) - \nabla _ { \theta _ { n } } g ( \theta _ { n } ) ) } & { { } } \end{array}$ is convergent a.s.Then we prove $g ( \theta _ { n } )$ is convergent a.s.

Step 4:ByLemma 9and the convergence of $g ( \theta _ { n } )$ in Step3,we get $\theta _ { n } \to J ^ { * }$ a.s..

Step5:After the proof of the convergence of mSGD,we analyze the iterates of $F _ { n }$ .Then under a new assumption $\begin{array} { r } { \operatorname* { l i m i n f } _ { d ( \theta , J _ { i } ) \to 0 } | | \nabla _ { \theta } g ( \theta ) | | ^ { 2 } / \left( g ( \theta ) - g _ { i } \right) \geq s > 0 } \end{array}$ ,we are able toobtain the convergent rate ofmSGD.