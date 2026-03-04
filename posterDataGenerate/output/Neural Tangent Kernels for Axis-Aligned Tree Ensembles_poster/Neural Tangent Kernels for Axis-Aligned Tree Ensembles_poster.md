# Contribution

We formulate the Neural Tangent Kernel (NTK) induced by infinitely

# Differentiable Decision Tree

By employing a sigmoid-like function, we can relax the splitting into a continuous form,which allows the use of gradient descent.

![](visuals/images/fig_1.jpg)

# Neural Tangent Kernel for Tree Ensembles

The NTK emerges in the context of functional gradient descent.

# Functional Gradient Descent

![](visuals/images/fig_2.jpg)

○It does not change during training when considering infinitely wide neural networks.   
○Then,functional behavior becomesanalytically tractable.

By handling the number of trees like the width of neural networks, we can apply NTK theory to differentiable tree ensembles.   
Proved in our previous work: Kanoh & Sugiyama (ICLR 2022)   
• In this work,we extend the NTK concept for axis-aligned trees.

# Axis-Aligned Constraint

We consider two axis-aligned cases: AAA and AAl.   
${ \pmb w } _ { m , n }$ is in one-hot representation,spliting isaxis-aligned.

![](visuals/images/fig_3.jpg)

![](visuals/images/fig_4.jpg)

![](visuals/images/fig_5.jpg)

![](visuals/images/fig_6.jpg)

# Closed-form NTK formula for Axis-Aligned Trees

# NTK for Infinite Ensembles of Axis-Aligned Trees

![](visuals/images/fig_7.jpg)

•Training behavior is now analytically tractable using our formula.

![](visuals/images/fig_8.jpg)  
Output dynamics for test data points.Each line color corresponds to each data point.

# Ensembles of Various Trees

The NTK induced by an ensemble of various tree architectures is equal to the sum of the NTKs induced by each architecture.

Op is the proportion of the corresponding tree architecture within the ensemble.

# NTK Property forMixed Trees

Mixed $( \pmb { x } _ { i } , \pmb { x } _ { j } ) = \rho _ { 1 } \Theta ^ { \tt A }$

# Insight on Oblivious Trees

Any non-oblivious trees can be transformed into oblivious trees that induce exactly the same limiting NTK.   
There is no need to consider combinations of complex trees,and it is sufficient to consider only combinations of oblivious trees.

![](visuals/images/fig_9.jpg)

# Multiple Kernel Learning (MKL) as Architecture Search ---

MKL enables tree architecture search based on convex optimization.

○Suitable features for AAA and AAl can be different.

![](visuals/images/fig_10.jpg)  
MKL weights obtained bythe tic-tac-toe endgame dataset

![](visuals/images/fig_11.jpg)  
Classification accuracy on tic-tac-toe endgame dataset   
Hardness ofthe sigmoidused inasplitting

![](visuals/images/fig_12.jpg)  
Interactions for tic-tac-toe endgame