# CW-ERM: Improving Autonomous Driving Planning with Closed-loop Weighted Empirical Risk Minimization

EeshaKumar1\*,Yiming Zhang²,Stefano Pini1,Simon Stent1, AnaSofia Rufino Ferreira²,SergeyZagoruyko1,ChristianS.Perone1\*

IWovenPlanet UnitedKingdomLimited2Woven PlanetNorthAmerica,Inc.\*Equal contribution Contact:{firstname}.{lastname}@woven-planet.global

# Main ldeas and Motivation

·Behavior Cloning (BC)algorithms for training selfdrivingvehiclesvia pure Empirical Risk Minimization (ERM) biasespolicy towards matching open-loop behavior

·We debias the policy network by identifying important samples via aclosed-loop evaluator ·Training in threephases ·Open-loop identification phase ·Error set construction and evaluation phase ·Upsampling training phase

# Our Contributions

$\bullet$ Motivate and proposea technique that leverages closed-loop evaluationmetricsacquired from policy rollouts inasimulator to debias thepolicy network and reduce the distributional differences between training (open-loop) and inference time (closed-loop);

·Evaluate CW-ERM on achallenging urban driving dataset in a closed-loop fashion to show that our method,although simple to implement,yieldssignificant improvements inclosed-loop performancewithout requiringcomplexand computationally expensive closed-loop trainingmethods;

·Showan importantconnection of ourmethod toafamilyofmethods thataddresses covariate shift through density ratio estimation.

Traditional open-loop ERM training Closed-loop Weighted Empirical Risk Minimization (CW-ERM) 。 。 。 000.0 O..00 。。 。 ·00·。 Training Identification Closed-loop Errorset Upsampled Final Scenes Policy Simulation construction Training Scenes Policy TERM ERERM πCW-ERM Front Collisions Side Collisions Rear Collisions Dist.to ref.traj. Baseline(ERwstcw) SideCollisions(CW-ERM) 三三 Dist.toref.traj.(CW-ERM) Front $^ +$ SideCollisions(CW-ERM)   
Front $^ +$ Side $^ +$ RearCollisions(CW-ERM)   
Front $^ +$ Side $^ +$ Dist.toref.traj.(CW-ERM) 5 10 15 20 40 50 60 70 2030 40 50 20 30 40 50

# Methodology

# Stage 1 (ldentification Policy)

·Train policy network via BC in open-loop using ERM, get $\hat { \pi } _ { E R M }$

# Collision Avoidance Examples

# Stage 2 (Closed-Loop Simulation)

·Perform rollouts using $\hat { \pi } _ { E R M }$ in closed-loop simulator

·Collect closed-loop metricsand identify the error set

$$
E _ { \hat { \pi } _ { E R M } } = \{ ( s _ { i } . a _ { i } ) \mathrm { ~ s . t . ~ } C ( s _ { i } , a _ { i } ) > 0 \} ,
$$

where $C ( s _ { i } , a _ { i } )$ is acost (e.g.collisions) incurred during the closed-loop rollouts.

![](/data/huangyc/Document2All/posterDataOutput_vlm/CW-ERM: Improving Autonomous Driving Planning with Closed-loop Weighted Empirical Risk Minimization_poster/auto/images/images/fig_1.jpg)  
Front collisions

![](/data/huangyc/Document2All/posterDataOutput_vlm/CW-ERM: Improving Autonomous Driving Planning with Closed-loop Weighted Empirical Risk Minimization_poster/auto/images/images/fig_2.jpg)  
Side collisions

# References

# Stage 3 (Final Policy)

·Train new policy where scenes belonging to $E _ { \hat { \pi } _ { E R M } }$ areunweighted bya factor $w ( \cdot )$

$$
\arg \operatorname* { m i n } _ { \pi \in \Pi } \mathbb { E } _ { s \sim d _ { \pi ^ { * } } , a \sim \pi ^ { * } ( s ) } [ w ( E _ { \hat { \pi } _ { E R M } } , s ) \ell ( s , a , \pi ) ]
$$

1.Liuet al. (2021).Just Train Twice: Improving Group Robustness without TrainingGroupInformation.InternationalConferenceonMachineLearning. 2.Vitelietal.(2022).Safetynet:Safeplanning forreal-world self-drivingvehicles usingmachine-learnedpolicies.InternationalConferenceonRoboticsand Automation (ICRA). 3.Scheel etal.(2022).Urbandriver:Learning todrive fromreal-world demonstrationsusingpolicy gradients.Conferenceon Robot Learning.