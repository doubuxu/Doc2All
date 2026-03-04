# On the convergence of mSGD and AdaGrad for stochastic optimization

# Algorithms:

$$
\mathbf {S G D}: \theta_ {n + 1} = \theta_ {n} - \epsilon_ {n} \nabla_ {\theta_ {n}} g \left(\theta_ {n}, \xi_ {n}\right)
$$

$$
\mathbf {m S G D}: v _ {n} = \alpha v _ {n - 1} + \epsilon_ {n} \nabla_ {\theta_ {n}} g \left(\theta_ {n}, \xi_ {n}\right), \theta_ {n + 1} = \theta_ {n} - v _ {n}
$$

$$
\text {A d a G r a d}: \quad \theta_ {n + 1} - \theta_ {n} - \frac {}{\sqrt {\sum_ {t = 1} ^ {n} \left\| \nabla_ {\theta_ {n}} g \left(\theta_ {n} , \xi_ {n}\right) \right\| ^ {2}}} \nabla_ {\theta_ {n}} g \left(\theta_ {n}, \xi_ {n}\right)
$$

# Contributions:

·We prove that the iterates of mSGD are asymptotically convergent to a connected set of stationary points for possibly non-convex loss function almost surely (i.e.,with probability one),which is more general than existing works on subsequence convergence.   
·We quantify the convergence rate of mSGD for the loss functions.Through this convergence rate we can geta theoretical explanation of why mSGDcanbe seen as an acceleration of SGD.Moreover,we provide the convergence rate of mean-square gradients and connect it to the convergence of time averages.   
·We prove the iterates of AdaGrad are asymptotically convergent to a connected set of stationary points almost surely for possible non-convex loss functions. The convergence result for the AdaGrad extends the subsequence convergence in the literature.

# Main assumptions:

Assumption1 Noise sequence $\left\{ \xi _ { n } \right\}$ aremutually independentand independentof $\theta _ { 1 }$ and $\nu _ { 0 }$ such that $\bar { g ( x ) } = \mathbb { E } _ { \xi _ { n } } \left( g ( x , \xi _ { n } ) \right)$ forany $\boldsymbol { x } \in \mathbb { R } ^ { N }$

Assumption2(Lossfunction assumption) Lossfunction $g ( \theta )$ satisfiesthefollowingconditions:

1) $g ( \theta )$ isanon-negativeand continuouslydifferentiable function.   
2)The setof stationarypoints of $\| \nabla _ { \theta } g ( \theta ) \|$ is notanempty set,thatis $J : = \{ \theta | \| \nabla _ { \theta } g ( \theta ) \| = 0 \} \neq \emptyset$   
3 $\nabla _ { \boldsymbol { \theta } } g ( \boldsymbol { \theta } )$ satisfiestheLipschitzcondition,i.e.,thereisascalar $c > 0 ,$ such that for any $x , y \in \mathbb { R } ^ { N }$ $\left\| \nabla _ { x } g ( x ) - \nabla _ { y } g ( y ) \right\| \leq c \| x - y \|$   
4) There is a scalar $M > 0$ such that for any $\boldsymbol \theta \in \mathbb { R } ^ { N }$ and positive integer n,

$$
\mathbb {E} _ {\xi_ {n}} \left(\left\| \nabla_ {\theta} g (\theta) - \nabla_ {\theta} g (\theta , \xi_ {n}) \right\| ^ {2}\right) \leq M (1 + g (\theta)). \tag {6}
$$

Assumption3 Momentumcoefficient $\alpha \in [ 0 , 1 )$ and the sequence of step sizeεnispositive,monotonicallyeceasingtrouch $\textstyle \sum _ { n = 1 } ^ { + \infty } \varepsilon _ { n } = + \infty$ and $\textstyle \sum _ { n = 1 } ^ { + \infty } \varepsilon _ { n } ^ { 2 } < + \infty$ P

Assumption4(Lossfunction assumption) Loss function $g ( \theta )$ satisfies the following conditions:

1）g(0)isanon-negativeand continuouslydifferentiable function.Thesetofits stationary points $J = \{ \theta | \| \nabla _ { \theta } g ( \theta ) \| = 0 \}$ isaboundedsetwhichhasonlyfiniteconnectedcomponents $J _ { 1 } , . . . , J _ { n } .$ Inaddition,treis $\varepsilon ^ { \prime } > 0 ,$ such that forany $i \in \{ 1 , 2 , \ldots , n \}$ and $0 < d ( \theta , J _ { i } ) < \varepsilon ^ { \prime }$ ,itholdsthat $\left| g ( \theta ) - g _ { i } \right| \neq 0 ,$ where $g _ { i } = \{ g ( \theta ) | \theta \in J _ { i } \}$ isaconstant.

2）Forany $i \in \{ 1 , 2 , \ldots , n \}$ ,itholdsthat

$$
\liminf_{d(\theta ,j_{i})\to 0}\frac{\| \nabla_{\theta}g(\theta)\|^{2}}{g(\theta) - g_{i}}\geq s > 0.
$$

Assumption5 Lossfunction $g ( \theta )$ inequation5satisfies thefollowingconditions:

1）g(0）isanon-negativeandcontinuously diffrentiable function.The setof itsstationary points $J = \{ \pmb { \theta } | \| \nabla _ { \pmb { \theta } } g ( \pmb { \theta } ) \| = 0 \}$ isaboundedsetwhichhas onlyfiniteconnectedcomponents $J _ { 1 } , . . . , J _ { n } .$ Inaddition,thereisε1>0,suchthat foranyiand $0 < d ( \theta , J _ { i } ) < \varepsilon _ { 1 }$ ,itholdsthat $\left| g ( \theta ) - g _ { i } \right| \neq 0 ,$ where $g _ { i } = \{ g ( \theta ) | \theta \in J _ { i } \}$ isaconstant.   
2)Thegradient $\nabla _ { \boldsymbol { \theta } } g ( \boldsymbol { \theta } )$ satisfies theLipschitzcondition,i.e.foranyx,y∈RN Vxg(x）-Vyg（y）/≤cx-yll   
3）There are two constants $M ^ { \prime } > 0$ and $a > 0$ such that forany $\theta \in \mathbb { R } ^ { N } a n d n \in \mathbb { N } _ { + }$

$$
E _ {\xi_ {n}} \left(\left\| \nabla_ {\theta} g (\theta , \xi_ {n}) \right\| ^ {2}\right) \leq M ^ {\prime} \left\| \nabla_ {\theta} g (\theta) \right\| ^ {2} + a. \tag {11}
$$

# Main results:

Theorem1 Consider themSGD in equation3.IfAssumptions1-3 hold,then for $\forall \boldsymbol { \theta } _ { 1 } \in \mathbb { R } ^ { N }$ and $\forall \nu _ { 0 } \in \mathbb { R } ^ { N }$ ,thereexistsaconnected set $J ^ { * } \subseteq J$ such that the iterate $\theta _ { n }$ isconvergent to the set $J ^ { * }$ almost surely,i.e.,

$$
\lim  _ {n \rightarrow \infty} d \left(\theta_ {n}, J ^ {*}\right) = 0, \quad a. s.
$$

where $d ( x , J ^ { * } ) = \operatorname* { i n f } _ { y } \{ \| x - y \| , y \in J ^ { * } \}$ denotes the distance between point xand set J*.

Theorem2 Consider themSGDin equation3with thenoise followingauniform samplingdistribution.IfAssumptions1-4hold,for $\forall \nu _ { 0 } \in \mathbb { R } ^ { N }$ and $\forall \theta _ { 1 } \in \mathbb { R } ^ { N }$ itholdsthat

$$
\mathbb {E} \left(\| \nabla_ {\theta_ {n}} g (\theta_ {n}) \| ^ {2}\right) = O \left(e ^ {- \sum_ {i = 1} ^ {n} \frac {s \varepsilon_ {i}}{p (1 - \alpha) ^ {2}}}\right), \tag {10}
$$

$p = \exp \left\{ \sum _ { k = 1 } ^ { \infty } M \varepsilon _ { k } ^ { 2 } \right\}$ dief

In Theorem2,let $\alpha = 0$ ,then we can obtain theconvergence rate of SGD,

$$
\mathbb {E} \left(\| \nabla_ {\theta_ {n}} g (\theta_ {n}) \| ^ {2}\right) = O \left(e ^ {- \sum_ {i = 1} ^ {n} \frac {s}{p} \varepsilon_ {i}}\right)
$$

Theorem3 Consider the AdaGrad in equation5.If Assumptions1and 5 hold,then for $\forall \theta _ { 1 } \in \mathbb { R } ^ { N }$ and $S _ { 0 } = 0$ thereexistsa connected component of the set $J ^ { * } \subseteq J ,$ suchthat the estimate $\theta _ { n }$ is convergent to the set $J ^ { * }$ almost surely,i.e.,

$$
\lim  _ {n \rightarrow \infty} d \left(\theta_ {n}, J ^ {*}\right) = 0. \quad a. s.
$$

# Proof outline for Theorems 1-2:

The proof is in light of the Lyapunov method.We aim to prove that $g ( \theta _ { n } )$ is convergent a.s.,and then toprove $\nabla _ { \theta _ { n } g } ( \theta _ { n } )  0 a . s$ With these two results,we are able to get $\theta _ { n }  J ^ { * } \thinspace a . s .$ Inthefollowing, weprovide the proof outline to show how to obtain the provided results of mSGD.

Step1:We prove mSGD is a stable algorithm,i.e., $\mathbb { E } ( g ( \theta _ { n } ) ) < K < + \infty , \forall n$ inLemma1.The idea is to prove that a weighted sum of the loss function value,i.e.,

$$
U _ {n} := \sum_ {t = 1} ^ {n} (1 / (2 - \alpha)) ^ {n - t} \mathbb {E} (1 + g (\theta_ {t + 1}))
$$

is bounded through a recursion formula (a rough form)

$$
U _ {n} - U _ {n - 1} \leq A \alpha^ {n} + \underbrace {B \sum_ {t = 1} ^ {n - 1} \left(1 / (2 - \alpha)\right) ^ {n - t} \varepsilon_ {t} ^ {2} \mathbb {E} \left\| \nabla_ {\theta_ {t}} g \left(\theta_ {t} , \xi_ {t}\right) \right\| ^ {2}} _ {I} (A, B a r e t w o c o n s t a n t s).
$$

Then we apply Assumption 24) to $I$ and then obtain

$$
U _ {n} - U _ {n - 1} \leq A \alpha^ {n} + \underbrace {B \sum_ {t = 1} ^ {n - 1} \left(1 / (2 - \alpha)\right) ^ {n - t} \varepsilon_ {t} ^ {2} \mathbb {E} \left(1 + g (\theta_ {t})\right)} _ {R} (A, B a r e t w o c o n s t a n t s).
$$

Combining $U _ { n - 1 }$ and $R$ leads to

$$
F _ {n} - F _ {n - 1} \leq A \alpha^ {n} + B ^ {\prime} \left(\frac {1}{2 - \alpha}\right) ^ {n} (A, B ^ {\prime} \text {a r e t w o c o n s t a n t s}),
$$

where

$$
F _ {n} := \sum_ {t = 1} ^ {n} \left(\frac {1}{2 - \alpha}\right) ^ {n - t} Z (t + 1) \mathbb {E} \left(e _ {t + 1} ^ {(n)} \left(1 + g \left(\theta_ {t + 1}\right)\right)\right)
$$

and

$$
Z (t) = \prod_ {k = t} ^ {+ \infty} \left(1 + M _ {0} \varepsilon_ {k} ^ {2}\right) = \left(1 + M _ {0} \varepsilon_ {t} ^ {2}\right) \prod_ {k = t + 1} ^ {+ \infty} \left(1 + M _ {0} \varepsilon_ {k} ^ {2}\right) = \left(1 + M _ {0} \varepsilon_ {t} ^ {2}\right) Z (t + 1).
$$

Thus, we are able to obtain $\begin{array} { r } { E \big ( g \big ( \theta _ { n } \big ) \big ) < F _ { n - 1 } \leq A \sum _ { t = 1 } ^ { + \infty } \alpha ^ { t } + B \sum _ { t = 1 } ^ { + \infty } \big ( 1 / ( 2 - \alpha ) \big ) ^ { t } < + \infty . } \end{array}$

Step 2: From Lemma 1 and the condition $\textstyle \sum _ { t = 1 } ^ { + \infty } \varepsilon _ { n } ^ { 2 } < + \infty$ ,we are able to prove that $\scriptstyle \sum _ { t = 1 } ^ { n } \| \nu _ { t } \| ^ { 2 }$ and $\Sigma \varepsilon _ { t } \| \nabla _ { \theta _ { t } } g ( \theta _ { t } ) \| ^ { 2 }$ are convergent a.s.respectively, as stated inLemma7and Lemma 8.

Step3:We divide $g ( \theta _ { n } )$ into three terms

$$
g \left(\theta_ {n}\right) = \sum_ {t = 1} ^ {n} A (n) \| v _ {t} \| ^ {2} + \sum_ {t = 1} ^ {n} B _ {n} \varepsilon_ {t} \| \nabla_ {\theta_ {n}} g \left(\theta_ {n}\right) \| ^ {2} + \sum_ {t = 1} ^ {n} C _ {n} ^ {T} \left(\nabla_ {\theta_ {n}} g \left(\theta_ {n}, \xi_ {n}\right) - \nabla_ {\theta_ {n}} g \left(\theta_ {n}\right)\right).
$$

From Lemma7and Lemma8,we are able to prove that $\begin{array} { r l } { \quad } & { { } \sum _ { t = 1 } ^ { n } A ( n ) \| \nu _ { t } \| ^ { 2 } + \sum _ { t = 1 } ^ { n } B _ { n } \varepsilon _ { t } \| \nabla _ { \theta _ { n } } g ( \theta _ { n } ) \| ^ { 2 } } \end{array}$ is convergenta.s..Fromtheconvergence theorem formartingale-difference sum(Lemma5),weprove that $\begin{array} { r l } { \sum _ { t = 1 } ^ { n } C _ { n } ^ { T } ( \nabla _ { \theta _ { n } } g ( \theta _ { n } , \xi _ { n } ) - \nabla _ { \theta _ { n } } g ( \theta _ { n } ) ) } & { { } } \end{array}$ isconvergenta.s.Thenweprove $g ( \theta _ { n } )$ is convergent a.s.

Step 4:By Lemma 9 and the convergence of $g ( \theta _ { n } )$ in Step 3,we get $\theta _ { n } \to J ^ { * }$ a.s..

Step5:After the proof of the convergence of mSGD,we analyze the iterates of $F _ { n }$ .Then under a new assumption $\begin{array} { r } { \operatorname* { l i m i n f } _ { d ( \theta , J _ { i } ) \to 0 } \| \nabla _ { \theta } g ( \theta ) \| ^ { 2 } / \big ( g ( \theta ) - g _ { i } \big ) \geq s > 0 } \end{array}$ ,weareable toobtain the convergent rate ofmSGD.