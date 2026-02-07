# UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining

Hyung Won Chung,Xavier Garcia,Adam Roberts,YiTay,Orhan Firat,Sharan Narang, Noah Constant h.w.chung27@gmail.com,{nconstant, xgarcia}@google.com

50 r=1   
T=3.33   
25 UniMax (1×budget) UniMax(1/8budget)   
4   
2   
00 50 100 Languagerank

![](/data/huangyc/Document2All/posterDataOutput_vlm/UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining_poster/auto/images/images/fig_1.jpg)  
(b)Pretraining samplingdistribution.Temperature samplingresultsinpoorlybalanced distributions, whereasUNIMAX providesmore uniform distributions without excessive upsampling.

![](/data/huangyc/Document2All/posterDataOutput_vlm/UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining_poster/auto/images/images/fig_2.jpg)  
(a)Number of training epochs for each language. Temperature samplingresults inalargenumberof datarepeats for low-resource languages,whereas UNIMAX explicitly caps repeats.

![](/data/huangyc/Document2All/posterDataOutput_vlm/UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining_poster/auto/images/images/fig_3.jpg)  
Figure2:Pretraining cross-entropy loss on the held-out data over the training steps.With too-low temperature,low-resourcelanguagesaresampled too litle,andtheirlosses arerelatively high.With higher temperature,overfitting becomes more severe with increasingmodel size.

$$
p _ { l } = \frac { n _ { l } } { \sum _ { l ^ { \prime } \in L } n _ { l ^ { \prime } } } \quad q _ { l } = \frac { p _ { l } ^ { 1 / \tau } } { \sum _ { l ^ { \prime } \in L } p _ { l ^ { \prime } } ^ { 1 / \tau } }
$$

![](/data/huangyc/Document2All/posterDataOutput_vlm/UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining_poster/auto/images/images/fig_4.jpg)  
Figure4:Average TyDiQA GoldP performanceacross three model sizes.Overall,UNIMAX outperforms both baselines at all model sizes considered.Breakdowns on higher-resource (top-5)and lower-resource (bottom-4) languages show UNIMAX outperforms $\tau = 3 . 3 3$ on both high-and lowresource,and onlyunderperforms $\tau = 1$ onhigh-resource at largemodel scales.

Algorithm1:UNIMAX   

<table><tr><td></td><td>Temperature(T)</td></tr><tr><td>mBERT(Devlin et al.,2019)</td><td>1.43</td></tr><tr><td>XLM(Conneau&amp;Lample,2019)</td><td>2.00</td></tr><tr><td>XLM-R(Conneau et al.,2020)</td><td>3.33</td></tr><tr><td>mT5(Xueetal.,2021)</td><td>3.33</td></tr><tr><td>XLM-E(Chi etal.,2022)</td><td>1.43</td></tr></table>

![](/data/huangyc/Document2All/posterDataOutput_vlm/UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining_poster/auto/images/images/fig_5.jpg)  
Figure3:Pretraining cross-entropy loss on the held-out data over1Mtraining steps.With the sequence length of 512,this correspondsto $1 / 2$ character budget.Theoverfittingbehavior emerges onlyafter sufficient number of training steps for $\tau = 3 . 3 3$

Inputs:Character count $c _ { l }$ of each language $l$ in all the languages $L$ of the training corpus Total characterbudget $C$ Thenumber of epochs per language $N$   
Output: Sampling distribution $p _ { l }$ of each language

Table3:Comparison to mT5. XNLI and PAWS-X show average per-language accuracy; the rest showaverage per-language EM/F1.We usethe translate-train setting except forTyDiQA,which uses“in-language”.We omit results for theLarge configuration due to instabilities in training.   

<table><tr><td></td><td colspan="2">XNLI</td><td colspan="2">PAWS-X</td><td colspan="2">XQuAD</td><td colspan="2">MLQA</td><td colspan="2">TyDiQA</td></tr><tr><td>Model</td><td>mT5</td><td>umT5</td><td>mT5</td><td>umT5</td><td>mT5</td><td>umT5</td><td>mT5</td><td>umT5</td><td>mT5</td><td>umT5</td></tr><tr><td>Small</td><td>72.0</td><td>76.2</td><td>79.9</td><td>87.2</td><td>49.4/64.5</td><td>60.5/74.0</td><td>38.8/56.6</td><td>41.8/60.7</td><td>62.7/74.0</td><td>56.6/70.0</td></tr><tr><td>Base</td><td>79.8</td><td>80.8</td><td>89.3</td><td>90.4</td><td>59.7/75.3</td><td>67.3/79.8</td><td>48.5/67.6</td><td>51.6/70.5</td><td>68.4/79.7</td><td>68.4/81.0</td></tr><tr><td>XL</td><td>85.3</td><td>86.5</td><td>91.0</td><td>90.7</td><td>56.6/75.1</td><td>75.0/86.1</td><td>54.5/73.5</td><td>58.3/76.8</td><td>78.4/87.6</td><td>74.1/85.2</td></tr><tr><td>XXL</td><td>87.1</td><td>87.8</td><td>91.5</td><td>91.2</td><td>71.3/85.2</td><td>77.9/88.2</td><td>57.4/76.0</td><td>70.5/78.6</td><td>79.5/88.7</td><td>81.2/89.7</td></tr></table>

# Resources

mC43.1.0,availablevia HuggingFace . umT5checkpoints,availablevia T5X repo

end for   
p←normalize $( U )$   
return p