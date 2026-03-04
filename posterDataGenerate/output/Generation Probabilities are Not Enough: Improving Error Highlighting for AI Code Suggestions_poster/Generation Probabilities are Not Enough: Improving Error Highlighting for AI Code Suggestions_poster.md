# Generation Probabilities are Not Enough: Improving Error Highlighting in Al Code Suggestions

Helena Vasconcelos,Gagan Bansal,Adam Fourney,

Vera Liao, Jennifer Wortman Vaughan

![](visuals/images/fig_1.jpg)

Research

Programmers increasingly use Al generated code (e.g., from CoPilot) in IDEs!

However,generated code may be erroneous! We need to help programmers double-check Al code and identify when and where it may be incorrect.

We explore two options to highlight uncertain, potentially erroneous regions:

Use generation probabilities or "confidence scores" to show where the model is uncertain   
Learn an edit model to show where programmersare most likely to make edits

Mixed-methods, within-subjects study with 30 programmers showed that edit model leads to:

-Significantly faster task completion time

![](visuals/images/fig_2.jpg)

-Significantly more localized edits

![](visuals/images/fig_3.jpg)

-Stronger preference

![](visuals/images/fig_4.jpg)

compared to the generation probability and no-highlights