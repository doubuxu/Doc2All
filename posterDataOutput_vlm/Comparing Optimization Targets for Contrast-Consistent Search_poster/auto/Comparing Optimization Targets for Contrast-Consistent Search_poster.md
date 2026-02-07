# Comparing Optimization Targets for Contrast-Consistent Search

Hugo Fry，Seamus Fallows,lan Fan, Jamie Wright, Nandi Schoots

TheAlSafetyHub

# Abstract

# Clarifying Ccs

# Introducing the MD loss function

Weinvestigate the optimization target of Contrast-Consistent Scarch (CCS),whichaims lo rccovcrthc inlcrnal rcprcscnlalions of truthofalargelanguagemodel.Wepresentanewloss function that wecalltheMidpoint-Displacerment(MD)lossfunction.Wedemonstrate that fora certain hyper-parametervalue this MD loss functionleads toaprober withvery similar weightsto CCS.Wefurther showthat thishyper-parameter isnot optimaland thatwithabetter hypcr-paramclcr lhc MD loss[unclion lcnlalivclyallainsa highcr testaccuracy than CCS.

# Introducing Ccs

Contrast-Consistent Search (CCS),developed by Burns et al.[1].is anunsupcrviscdmclhod forcxLractingknowlcdgcfrom lhc hiddcn statesof large languagemodels.Given only unlabelled model activations,CCSisable toaccuratelyclassify statementsaccordingto theirtruthvalue.Itdoes thisbyutilisingthenegationconsistency property of truth:astatement and its negation must have opposite truthvalues.Framedin terms of probabilities,given theprobability $\gamma$ thata propositionis truc,thcprobabilityitsncgation is trucis $1 - p ,$ CCSworks byfindinga direction in activation space that satisfies lhisconsislcncy constrainl.

Dataset. We takea dataset of contrast pairs $\{ ( \boldsymbol { x } ; t , \boldsymbol { x } ; t ) \} _ { i = 1 } ^ { n }$ consist ingof nalural languagc slalcmcnls $\boldsymbol { \cdot } \boldsymbol { \cdot } \boldsymbol { \cdot } \boldsymbol { \cdot }$ and Lhcir logical opposilcs $\boldsymbol { x } _ { i } ^ { - }$ Thepairsare formedbytakingaquestion ${ \dot { q } } _ { i }$ andappending withone of twomutuallyexclusive ariswers.Contrast pairsare fed toapre-trained languagemodel to obtainasetof representations $\{ ( \boldsymbol { \phi } _ { i } ^ { + } , \boldsymbol { \phi } _ { i } ^ { - } ) \} _ { i = 1 } ^ { 3 5 }$ where $\phi _ { i } ^ { \perp } : - \phi ( x _ { i } ^ { - } ) \in \mathbb { R } ^ { d }$ is theactivation vector of aparticular layer for the input $\cdot \cdot _ { i } ^ { - }$ .These representationsare then used to traina linearclassifieraccordingtoan objectivedesigned to enforce negation consistency on contrast pairs.

In order toavoid training the classifier to simplydetect thepresence ofthemutually exclusive answers,the sets $\{ \Leftrightarrow _ { i } ^ { + } \}$ and $\{ \phi _ { i } ^ { - } \}$ should beindependently normalized.Thenormalized representationsare given by

$$
\tilde { \phi } _ { i } ^ { - } : - \frac { \tilde { \phi } _ { i } ^ { - } - \mu ^ { - } } { \sigma ^ { \perp } } ,
$$

where $( \mu ^ { \perp } , \sigma ^ { - } )$ arethe meansand standard deviations of the respective sets.「or convenience,we will ormit the tildeand simply use ${ \boldsymbol { \phi } } _ { ; i } ^ { + }$ torepresent the normalized representations.

Loss Function.Alinear classifier $p _ { 0 , { \dot { \boldsymbol { \psi } } } } : \dot { \boldsymbol { \wp } }  \sigma ( \boldsymbol { \wp } ^ { T } \dot { \boldsymbol { \phi } } | \mathbf { \Sigma } b )$ is trained on thcnormalizcd activations,whcrc $\sigma$ isthc sigmoid function, $\theta$ isa vector of weights and $b$ is a bias.Theloss function is given by

$$
L _ { \mathrm { C C S } } ( \theta , b ) : - \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \big [ 1 - p _ { \theta , b } ( \phi _ { i } ^ { + } ) - p _ { \theta , b } ( \phi _ { i } ^ { - } ) \big ] ^ { 2 } + \operatorname* { m i n } \big \{ p _ { \theta , b } ( \phi _ { i } ^ { + } ) , p _ { \theta , b } ( \phi _ { i } ^ { - } ) \big \} ^ { 2 } .
$$

Thefirst term encourages the classifier to find features that are negation-consistent and the second term is included todisincentivise the degenerateassignment $p _ { \theta , \delta } ( \dot { \phi } _ { i } ^ { + } ) = p _ { \theta , \delta } ( \phi _ { i } ^ { - } ) = 0 . 5 ,$

Inference.To makeaprediction onan example $q _ { i }$ after training,the average

$$
\bar { p } _ { i } ( q _ { i } ) : - \frac { 1 } { 2 } ( p _ { 0 , b } ( \dot { \phi } _ { i } ^ { + } ) + ( 1 - p _ { 0 , b } ( \dot { \phi } _ { i } ^ { - } ) ) )
$$

is compared to0.5with $p _ { i } > 0 . 5$ correspondingtoeither theanswer "yes"or $" 1 7 0 ^ { \dag }$ based on whichever gives the maximumaccuracy on a givcn lcsl scl.

A natural guess for how CCs isable to accurately classify truth is thal lhc normalizcd modcl rcprcscnlalions arc approximalcly clusteredaccordingtotruthand that CCSisabletofinda hyperplane that separates these two clusters.However,this explanation is incorrect.

Recall thatafter training,anexample $q _ { i }$ is classified according to $\smash { p ( q _ { i } ) \geq 0 . 5 }$ .Usingcquation 3,this condlition rcduccs to

$$
\begin{array} { c } { { \sigma ( \theta ^ { T } \phi _ { i } ^ { - } + b ) > \sigma ( \theta ^ { T } \phi _ { i } ^ { - } - b ) } } \\ { { > 0 ^ { T } ( \phi _ { i } ^ { + } - \phi _ { i } ^ { - } ) > 0 . } } \end{array}
$$

We see that CCS is classifying only according to the displacement vectors $\{ \phi _ { i } ^ { - } - \phi _ { i } ^ { - } \}$ .Since these are translation invariant,CCS does notrequire the contrast pairs to be separable bya hyperplane. Figure1 shows an example in which CCS is nol findinga separaling hyperplane even when it gains a high test accuracy.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Comparing Optimization Targets for Contrast-Consistent Search_poster/auto/images/images/fig_1.jpg)  
Figure1.We ccnsideractivatiors of theT5-base mode on the BoolQ train dataset.On tc:x-ax’s wc plot thc projcctions of thc activation5 $\dot { \mathcal { O } _ { i } }$ ortothc first princicle cornponent and on the $y ^ { * }$ axisweolol the dalapoints $\phi _ { i }$ projected onto $\hat { \theta }$ We colour the datepcints $\vec { \mathbf { \nabla } } \cdot \vec { \mathbf { \nabla } } \cdot \vec { \mathbf { \nabla } }$ əy tnc (grourd-truth) truth-labcls'truc'(red)anc'fa sc'(bluc) $0 ^ { \circ }$ thc datapoints $x _ { i } .$ Thc hor'zontal linedicates the inputs fo‘which CCs outputs 0.5.

Additionally, the original paper:1] presents CCS as learning prob abilitiesfor the truth values of contrast pairs. We suggest abandoning this probabilities framing. Figure2 shows that CCS can still performwelleven when the probabilitiesare strongly clustered around 0.5.

![](/data/huangyc/Document2All/posterDataOutput_vlm/Comparing Optimization Targets for Contrast-Consistent Search_poster/auto/images/images/fig_2.jpg)  
Figure2.(a) Histograrrd'splaying the CCSorober otputs evaluuted o1 te lzst hidden state of tre ercoder cf UnfiedQA T5-Large for the Bco Q datasct.(b) H'stogram d'splaying thc CCS orobcr ot tputs cvaluated $_ { \textmd { O } ^ { \star } }$ thc lesthiddenstate of te decoderof UifedQAT5-Large for the BoolQdtatset. Dcspite the cncodcravi-ga higher confidence in thc prober outəuts,the encoder nasa lower leslaccuracy (O.523)than the decocer (0.978).   
Table2.We compare test accurac'es of diferent lossfunctiorsaveraged overfve datasets,using thezctivatio5 of a nubercfmodcls.Focachrowwc havecrboldcnedthclossfurcticn that obtaincc thchighcstavcrage tcstaccuracy notincluding the supervisedloss.Te(L)anc (D) abelsreler lo the encoderand decoderlayers cl the UQAmode.

Usingthenormalized weightvectorθwedefine thefollowingquan-Lilics:

$$
\begin{array} { r } { \displaystyle \mathcal { U } _ { i } : = \phi _ { i } ^ { + } - \phi _ { i } ^ { - } , \mathrm { ~ a n c } } \\ { \displaystyle \sigma _ { i i } ^ { 2 } : - \frac { 1 } { n } \sum _ { i } ( \hat { \theta } ^ { T } \boldsymbol { u } _ { i } ) ^ { 2 } . } \end{array}
$$

Hcrc $u _ { i }$ isthcdisplaccmcnt bctwccn thc activations ofa contrast pairand $\sigma _ { \it 2 } ^ { 2 }$ isthemean square separation of the activations of the contrast pairsalongthe direction $\theta$ .

Furthermore,we analogously define

$$
\begin{array} { r } { v _ { i } : = \phi _ { i } ^ { + } + \phi _ { i } ^ { - } , \mathsf { a n c } } \\ { \sigma _ { m } ^ { 2 } : = \displaystyle \frac { 1 } { n } \sum _ { i } ( \hat { \theta } ^ { T } v _ { i } ) ^ { 2 } . } \end{array}
$$

Here $\frac { v _ { i } } { 2 }$ is themidpintoftectiatisoftrast $\frac { \sigma _ { m } ^ { 2 } } { 4 }$ isthe mean square value of the midpoint of the activations of the contrast pairsalong thcdircction $\theta$ .

We propose a new loss functionand demonstrate that this new loss funclion isa good proxy oplimisalion largcl for CCs.Thc ncwloss function is given by

$$
\begin{array} { r l } { L _ { \mathsf { M E } } - ( \lambda - 1 ) \sigma _ { d } ^ { 2 } } & { { } \lambda \cdot \sigma _ { m } ^ { 2 } , } \end{array}
$$

where $\lambda \in \left[ 0 , 1 \right]$ isahyperparameter controlling therelative trade ofrbetwcen $\sigma _ { d } ^ { 2 }$ and $\sigma _ { m } ^ { 2 } ,$ and Lhewcight vcclor $\theta$ is conslraincd lo satisfy $| \theta | = 1$ .

Tounderstand whywe use this loss function,first that the CCS loss functionincentivisesincreasing theseparation of theprober outputs of conlrasl pairs $| p ( \phi _ { i } ^ { \ : | } ) - p ( \phi _ { i } ^ { - } ) |$ Considera ${ \mathsf { C } } { \mathsf { C } } { \mathsf { S } }$ prober $p ( \phi ) -$ $\sigma \langle \theta ^ { T } \phi + \bar { \theta } \rangle$ in which $\theta$ is constrained toafixed norm $\vert \theta \vert = c$

Inorder for CCSto increase thedifference between proberoutputs,onemight expect that CCSfindsadirection that increases the difference of the prober inputs (since sigmoid isamonotonically increasing function).That is tosay,onemight expect CCSwill finda direction that maximises $\sigma _ { \mathcal { I } } ^ { 2 }$

However,if $\sigma _ { m } ^ { 2 }$ ismuch larger than $\sigma _ { \it ( l } ^ { 2 }$ then the input to thesigmoid foreach contrast pair(i.e. $\theta ^ { T } { \Theta } _ { i } ^ { + } + b \operatorname { a n d } { \theta } ^ { T } { \phi } _ { i } ^ { - } + b )$ will be pushed int.o thesamesaturation regime of the sigmoid.Thisresults ina lower difference in prober outputs of contrast pairs,which in turn results ina lrade of between maximising $\textstyle ( \mathcal { T } _ { \vec { d } } ^ { 2 }$ while minimising $\sigma _ { m } ^ { 2 }$

It should be stressed that thistrade off between $\sigma _ { \mathcal { I } } ^ { 2 }$ and $\sigma _ { m } ^ { 2 }$ is purely anartifact of the double saturation of sigmoid usedin the CCS prober.Since this trade off shouldoccurnomatterwhat $| \theta | = c$ isconstrained to,we propose that the unconstrained CCS prober is ingncraloptisingorcbalatn $\sigma _ { \it d } ^ { 2 }$ and $\sigma _ { m } ^ { 2 }$

# Results

structure as the CCS probers, $p ( \boldsymbol { \phi } ) = \sigma ( \boldsymbol { \theta } ^ { T } \boldsymbol { \phi } + b ) ,$

# Similarity

# Accuracy

In Table 1 we find that the average cosine similarity between the weight vector of the CCS prober and the weight vector of the prober trained using our new MD method isabout O.63.For reference,the probability of two uniformlysampled1O24-dimensional unit vectorshavingacosine similarity $\tt O f O . 6 3$ or higher isapproximately $1 0 ^ { - 2 3 7 }$ Note that Lhe CCS probers had anaverage cosine similarily with themselves of only O.78.This suggests that the MD-CCS lossfunction isa good proxy optimization target for CCS.

<table><tr><td rowspan="2">Model</td><td colspan="5">Loss Function</td></tr><tr><td>CCS MD-CCS</td><td>MD-Acc MA SMR</td><td>PCA</td><td>Rand.</td><td>Superv.</td></tr><tr><td>UQA(E)</td><td>0.8359 0.7034</td><td>0.2995 0.1448</td><td>0.1991 0.2406</td><td>0.0222</td><td>0.2583</td></tr><tr><td>UQA(D)</td><td>0.8787 0.7269</td><td>0.5303 0.1687 0.2432</td><td>0.1792</td><td>0.0228</td><td>0.6014</td></tr><tr><td>DcBERTa</td><td>0.8643 0.6209</td><td>0.2786 0.2309 0.2024</td><td>0.0741</td><td>0.0202</td><td>0.4617</td></tr><tr><td>GPT-Neo</td><td>0.5277 0.4830</td><td>0.4164 0.0226 0.0485</td><td>0.1901</td><td>0.0245</td><td>0.1347</td></tr><tr><td>Average</td><td>0.7767 0.6336</td><td>0.3812 0.1418 0.1733</td><td>0.1710</td><td>0.0224</td><td>0.3640</td></tr></table>

Table1.Wccomputc theaverage cosine similar'tics of tncdirecticns foundusingdifercntloss functicns to the direcionsof2OCCSprobers.Weaverageoverfivedatasetsusing theactivationsofourdiferentmodels.Foreachrow webaveenboderedthelossfunctionthat obtaedthehighestaveregecosinesinilaitywithCCS,notincluding te CCS lcss furcticn.Notc that the (E)and(D)rcfer to trcccodeand decoder laycrs of thc UQA modcl.

In Table 2 we show the test accuracies of probers trained using the MD loss function on various datasetsandmodels.We tentatively find that theaccuracies of thenew probersare similar to those achieved byCCS,and often out-perform CCS.Note that MD-Acc probers geta higher test accuracy Lhanbolh lhe MD-CCSand CCS probers for three oul of fourmodels,foranaverage difference of around4%.

<table><tr><td rowspan=2 colspan=1>Model</td><td rowspan=2 colspan=8>Loss FunclionCCS MD-CCSMD-AccMA   SMR  PCA  Rand.Superv.</td></tr><tr><td rowspan=1 colspan=1>MD-CCS</td><td rowspan=1 colspan=1>MD-Acc</td><td rowspan=1 colspan=1>MA</td><td rowspan=1 colspan=1>SMR</td><td rowspan=1 colspan=1>PCA</td><td rowspan=1 colspan=1>Rand.</td><td rowspan=1 colspan=1>Superv.</td></tr><tr><td rowspan=1 colspan=1>UQA(E)</td><td rowspan=1 colspan=1>0.6863</td><td rowspan=1 colspan=1>0.6902</td><td rowspan=1 colspan=1>0.7414</td><td rowspan=1 colspan=1>0.7399</td><td rowspan=1 colspan=1>0.7419</td><td rowspan=1 colspan=1>0.7383</td><td rowspan=1 colspan=1>0.6363</td><td rowspan=1 colspan=1>0.8839</td></tr><tr><td rowspan=1 colspan=1>UQA(D)</td><td rowspan=1 colspan=1>0.8305</td><td rowspan=1 colspan=1>0.8200</td><td rowspan=1 colspan=1>0.8180</td><td rowspan=1 colspan=1>0.7550</td><td rowspan=1 colspan=1>0.7460</td><td rowspan=1 colspan=1>0.7525</td><td rowspan=1 colspan=1>0.6286</td><td rowspan=1 colspan=1>0.9140</td></tr><tr><td rowspan=1 colspan=1>DeBFRTa</td><td rowspan=1 colspan=1>0.7740</td><td rowspan=1 colspan=1>0.7855</td><td rowspan=1 colspan=1>0.8735</td><td rowspan=1 colspan=1>0.8650</td><td rowspan=1 colspan=1>0.8585</td><td rowspan=1 colspan=1>0.8605</td><td rowspan=1 colspan=1>0.7288</td><td rowspan=1 colspan=1>0.9135</td></tr><tr><td rowspan=1 colspan=1>CPT-Neo</td><td rowspan=1 colspan=1>0.5510</td><td rowspan=1 colspan=1>0.5755</td><td rowspan=1 colspan=1>0.5898</td><td rowspan=1 colspan=1>0.5820</td><td rowspan=1 colspan=1>0.5555</td><td rowspan=1 colspan=1>0.5737</td><td rowspan=1 colspan=1>0.5603</td><td rowspan=1 colspan=1>0.7580</td></tr><tr><td rowspan=1 colspan=1>Average</td><td rowspan=1 colspan=1>0.7105</td><td rowspan=1 colspan=1>0.7178</td><td rowspan=1 colspan=1>0.7557</td><td rowspan=1 colspan=1>0.7355</td><td rowspan=1 colspan=1>0.7255</td><td rowspan=1 colspan=1>0.7313</td><td rowspan=1 colspan=1>0.6385</td><td rowspan=1 colspan=1>0.8674</td></tr></table>

# References