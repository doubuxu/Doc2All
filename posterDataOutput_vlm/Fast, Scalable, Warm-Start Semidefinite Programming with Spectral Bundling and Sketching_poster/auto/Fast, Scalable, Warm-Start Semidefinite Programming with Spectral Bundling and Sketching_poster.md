# Fast,Scalable,Warm-StartSemidefinite Programming with Spectral Bundlingand Sketching

Rico Angell1 and Andrew McCallum1 1University of Massachusetts Amherst

# Motivation

· Semidefinite programming (SDP) is an important tool for many applications

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_1.jpg)

# Unified Spectral Bundling

·Many existing methods for solving or approximately solving SDPs ·Need for a method that is fast, scalable,and provably correct for massive SDPs · Need a method where hyperparameters can modulate memory, accuracy, speed,and scalability of solving general SDPs

# Problem Setup

max (C,x) X0 s.t. $\boldsymbol { \mathcal { A } } _ { \mathcal { T ^ { \prime } } } \boldsymbol { X } = \boldsymbol { b _ { \mathbb { Z ^ { \prime } } } }$ AX≤b $A : \mathbb { S } ^ { n }  \mathbb { R } ^ { \acute { m } }$ linear operator

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_2.jpg)

· Want to solve general SDPs with both equality and inequality constraints · Want to have theoretical guarantees about convergence to optimal solution $\bullet$ Assume cost matrix $C$ is sparse and a upper bound $\alpha \geq \mathrm { t r } ( X _ { \star } )$ exists ·Assume the number of constraints is small compared to the problem size · Want to be able to solve ${ \tt S D P s }$ where $X$ will not fit in memory ·Want solvertobeabletotakeadvantage ofawarm-start initialization

·Reformulated SDPas a the following penalized dual objective:

$$
\begin{array} { r } { f ( y ) : = \alpha \left[ \lambda _ { \operatorname* { m a x } } ( C - \mathcal { A } ^ { * } y ) \right] _ { + } + \langle b , y \rangle + \iota _ { \mathcal { V } } ( y ) ^ { \sim } } \\ { = \underset { ( X , \nu ) \in \mathcal { X } \times \mathrm { N } } { \operatorname* { s u p } } \langle C - \mathcal { A } ^ { * } y , X \rangle + \langle b - \nu , y \rangle } \end{array}
$$

· Solve the SDP by minimizing $f$ using a proximal bundle method:

$$
\tilde { y } _ { t + 1 }  \underset { y \in \mathbb { R } ^ { m } } { \arg \operatorname* { m i n } } \hat { f } _ { t } ( y ) + \frac { \rho } { 2 } \Vert y - y _ { t } \Vert ^ { 2 }
$$

where the model $\hat { f } _ { t }$ is parameterized by the low dimensional subspace of $\mathcal { X }$ ：

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_3.jpg)

· The size of $V$ determines the rank $k$ of each update, specified by the user

, Only update $y _ { t + 1 } \gets \tilde { y } _ { t + 1 }$ if $\beta ( f ( y _ { t } ) - \hat { f } _ { t } ( \tilde { y } _ { t + 1 } ) ) \leq f ( y _ { t } ) - f ( \tilde { y } _ { t + 1 } )$

·Always use $\tilde { y } _ { t + 1 }$ to create $\hat { \mathcal { X } } _ { t + 1 } , V _ { t + 1 }$ is the top- $k$ eigenvectors of $C - A ^ { * } \tilde { y } _ { t + 1 }$

· Analytical solution to the proximal bundle method lead to the folowing updates

$$
\begin{array} { c } { \displaystyle \ddot { y } _ { t + 1 } = y _ { t } - \frac { 1 } { \rho } ( b - \nu _ { t + 1 } - A X _ { t + 1 } ) } \\ { \displaystyle ( X _ { t + 1 } , \nu _ { t + 1 } ) \in \operatorname * { a r g m a x } _ { ( X , \nu ) \in \dot { \mathcal X } _ { t } \times \mathrm { N } } \langle C , X \rangle + \langle b - \nu - A X , y _ { t } \rangle - \frac { 1 } { 2 \rho } \| b - \nu - A X \| ^ { 2 } } \end{array}
$$

$f ( y _ { t } ) - \operatorname* { i n f } f \leq \varepsilon$ after $t \geq O ( 1 / \varepsilon )$ iterations, $O ( \cdot )$ suppresses dependence on $n , m$

# Scaling with Matrix Sketching

·Only need to keep track of projections of $X$ such as $\langle C , X \rangle$ and $_ { A X }$ ·All of the memoization can be done eficiently due to linearity of operations ·Apply low-rank matrix sketching techniques to enable scaling to problems where $X$ cannot fit in memory—track projection $P$ instead of $X$

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_4.jpg)

# Results

# Max-Cut

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_5.jpg)  
>1013 decision variables

>2 billion decision variables tindicates thananε-approximate solution was notachieved in72 hours.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_6.jpg)  
Traveling Salesman Problem

USBSeffectivelytakingadvantage ofwarm-start initialization

![](/data/huangyc/Document2All/posterDataOutput_vlm/Fast, Scalable, Warm-Start Semidefinite Programming with Spectral Bundling and Sketching_poster/auto/images/images/fig_7.jpg)  
Clustering with -constraints   
Problem size increases

# UMassAmherst

Manning College of Information & Computer Sciences