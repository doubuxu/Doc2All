# MOCCASIN: Efficient Tensor Rematerialization for Neural Networks

BurakBartan1/HaomingLi²/Harris Teague1/ ChristopherLott1/Bistra Dilkina²

1QualcommAl Research,2Universityof Southern California

bbartan@qti.qualcomm.com

# 1. Introduction

# 2.Motivation and problem statement

# 3.Prior work

·Thedeploymentandtrainingof neuralnetworks onedge computingdevicesposemanychallenges. ·Thelowmemory nature of edgedevices is often one of thebiggest limitingfactorsencounteredinthedeploymentof largeneural networkmodels. ·Tensorrematerializationor recomputeisawaytoaddress high memoryrequirementsforneuralnetworktrainingandinference. ·In this paperwe consider the problem of execution time minimizationof computegraphssubjecttoamemorybudget. ·Inparticular,we developa newconstraint programming formulationcalledMoccasinwith onlyO(n) integervariables, where $n$ isthenumberof nodes inthe compute graph(asopposed topriorwork formulationswith $O ( n ^ { 2 } )$ variables).

![](/data/huangyc/Document2All/posterDataOutput_vlm/Moccasin: Efficient Tensor Rematerialization for Neural Networks_poster/auto/images/images/fig_1.jpg)

![](/data/huangyc/Document2All/posterDataOutput_vlm/Moccasin: Efficient Tensor Rematerialization for Neural Networks_poster/auto/images/images/fig_2.jpg)

Considerthe example10-node computation graphabove,and assume:

<table><tr><td>MEMORY-CONSTRAINED COMPUTATION GRAPH SEQUENCINGWITHREMATERIALIZATION minimize total executionduration seq(G)</td></tr></table>

1.Output sizes are 50 for nodes on the left,and1for the ones on the right.

2.Durationis1forall nodes.

Considerexecution of the nodes in the order

# 0,1,2,3,4,5,6,7,8,9

Rematerialization:Discard outputof node1after node2is computed and recomputeitlater:

Weneed to keep the output of node1in memory until we execute node8 (similarlyfor2&7)

0,1,2,3,4,5,6,7,8,9   
discard1recompute1

Torecomputenode1:We need to recomputeO or have itavailablein memory-anotherdecisionthatneedstobemade bythealgorithm

Theworkof[1]developsamixed integerlinear programming(MILP) formulation to solve thisproblem.

·Introduces Boolean matrices $R , S , F$ forrecompute, storage,memorydeallocation $ O ( n ^ { 2 } + n m )$ Boolean decision variables(n:#nodes,m:#edges) ·Poorscalabilitytolarge computation graphs

Wehave developeda newoptimization problem formulationkeepingscalabilityinmind,which greatly simplifiestheproblem.

Keyassumption:Don't rematerializeany node more than C times.

[1]Checkmate:Breaking theMemoryWall with Optimal Tensor Rematerialization,Proceedingsof Machine Learningand Systems2(MLSys 2020).ParasJain,AjayJain,AniruddhaNrusimha，AmirGholami,Pieter Abbeel,JosephGonzalez,KurtKeutzer,lonStoica

# 4. Solution

# 5. Formal specification

# 6. Numerical results

minimize M wa (1) -Totalamountofcomputation   
s,e, Ui   
subjecto s≤e,v,i （2) Startof an interval comes before end e≤s²+1，Vv,i＜C (3） Orderingamong theintervals ofanode M ma≤M,t∈D （4) Memoryusecannotexceed M vi:st≤e $\forall ( u , v ) \in E$ , $\forall i \in \{ i : a _ { v } ^ { i } = 1 \}$ ,j such that $a _ { u } ^ { j } = 1 , s _ { u } ^ { j } + 1 \leq s _ { v } ^ { i } \leq e _ { u } ^ { j }$ (5) Precedence constraints s≠su，∀U,u∈{U,u:U≠u}，i,j (6) Intervalstarttimesarealldifferent a=1,u （7) -There is at least one active interval per node s，e∈D,a²∈{0,1}，U,i. （8） →Variabledomains   
10 Checkmate Moccasin $( C = 2 )$   
8   
6   
4   
0 500100015002000 Solve time(sec) Figure:Percentage of   
total duration increase against solve time in   
seconds forour   
proposed method   
(Moccasin)and   
Checkmate[1]onarealworld graph with n=442 nodesandm=1247   
edges.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Moccasin: Efficient Tensor Rematerialization for Neural Networks_poster/auto/images/images/fig_3.jpg)

Oursolution isanoptimizationproblemformulationwhere

·Themainbuildingblockistheconceptofoutputretentionintervalswhich simplifiestheproblemformulationgreatly   
·Outputretention intervalsare used tomodel howlongtheoutputofa nodeisretainedinmemory   
·We define $C$ retentionintervalsforeach node where each intervalrepresentsa rematerialization (i.e.recompute)of thatnode   
·The starting $s _ { v } ^ { i }$ and end $e _ { v } ^ { i }$ timesof theintervalsaremodeledasthedecisionvariablesof theoptimizationproblem   
·We then define the precedenceand memory constraints using these decision variables   
·Theresultingproblemcouldbeposedasaconstraintprogramming(CP)problem,whichwecoulduseanygenericCP solverto solvenumerically

<table><tr><td colspan="3"></td><td colspan="3">CHECKMATEMILP</td><td colspan="3">CHECKMATE LP+Rounding</td><td colspan="3">MOCCASIN</td></tr><tr><td>Graph</td><td>(n,m)</td><td>M</td><td>TDI%</td><td>Peakmem</td><td>Time (s)</td><td>TDI%</td><td>Peakmem</td><td>Time (s)</td><td>TDI%</td><td>Peakmem</td><td>Time (s)</td></tr><tr><td rowspan="2">RLG2</td><td rowspan="2">(250,944)</td><td>132,156</td><td>0.9</td><td>132,130</td><td>685.1</td><td>93.0</td><td>178,200</td><td>401.7</td><td>0.9</td><td>131,831</td><td>55.0</td></tr><tr><td>117,472</td><td>=</td><td></td><td>-</td><td>328.6</td><td>181,200</td><td>696.9</td><td>4.9</td><td>117,400</td><td>639.5</td></tr><tr><td rowspan="2">RLG4</td><td rowspan="2">(1000,5875)</td><td>547,757</td><td>=</td><td></td><td>=</td><td>-</td><td>=</td><td>=</td><td>0.7</td><td>547,660</td><td>3612.9</td></tr><tr><td>486,895</td><td>-</td><td></td><td>-</td><td>-</td><td>-</td><td>-</td><td>3.4</td><td>486,880</td><td>3611.8</td></tr><tr><td rowspan="2">RW1</td><td rowspan="2">(358,947)</td><td>20,227,276</td><td>2.3</td><td>20,226.048</td><td>1340.0</td><td>-</td><td></td><td>=</td><td>2.3</td><td>20,226.048</td><td>123.5</td></tr><tr><td>17,979,801</td><td>4.5</td><td>17,977,344</td><td>1605.4</td><td>=</td><td></td><td>=</td><td>4.5</td><td>17,977,344</td><td>122.0</td></tr><tr><td rowspan="2">RW2</td><td rowspan="2">(442,1247)</td><td>10,817,740</td><td>1.4</td><td>10,811,392</td><td>1856.7</td><td>=</td><td></td><td>-</td><td>1.4</td><td>10,813,440</td><td>1201.3</td></tr><tr><td>9,615,769</td><td>2.8</td><td>9,615,360</td><td>2242.9</td><td>=</td><td></td><td>=</td><td>2.8</td><td>9,613,312</td><td>303.9</td></tr><tr><td rowspan="2">RW3</td><td rowspan="2">(574,1304)</td><td>10,539,417</td><td>-</td><td></td><td>-</td><td>=</td><td></td><td>=</td><td>0.8</td><td>10,539,008</td><td>1802.4</td></tr><tr><td>9,368,371</td><td>-</td><td></td><td>-</td><td>-</td><td></td><td>-</td><td>1.6</td><td>9,367,552</td><td>1802.8</td></tr><tr><td rowspan="2">CM1</td><td rowspan="2">(73,149)</td><td>11.3GB</td><td>0.0</td><td>11.1GB</td><td>6.3</td><td>0.0</td><td>11.4GB</td><td>6.8</td><td>0.0</td><td>11.1 GB</td><td>3.1</td></tr><tr><td>10.0GB</td><td>0.1</td><td>9.65GB</td><td>5.6</td><td>0.1</td><td>10.8GB</td><td>6.7</td><td>0.1</td><td>9.9GB</td><td>3.1</td></tr><tr><td rowspan="2">CM2</td><td rowspan="2">(353,751)</td><td>31.9GB</td><td>0.1</td><td>31.6GB</td><td>434.1</td><td>0.1</td><td>31.5GB</td><td>505.2</td><td>0.2</td><td>31.9GB</td><td>65.2</td></tr><tr><td>28.4GB</td><td>0.3</td><td>28.3GB</td><td>485.3</td><td>0.5</td><td>27.8GB</td><td>1065.4</td><td>0.3</td><td>28.4GB</td><td>69.3</td></tr></table>

Table:Performance comparison across differentgraph families under different memory budgets.