# Generation Probabilities are Not Enough: Improving Error Highlighting in Al Code Suggestions

Helena Vasconcelos,GaganBansal,AdamFourney, Vera Liao, Jennifer Wortman Vaughan

Programmers increasingly use Al generated code (e.g., from CoPilot) in IDEs!

However,generated code may be erroneous!We need to help programmers double-check Al code and identify whenand where it may be incorrect.

We explore two options to highlight uncertain, potentially erroneous regions:

Use generation probabilities or “confidence scores"toshowwherethemodel isuncertain Learn an edit model to show where programmers are most likely to make edits

Mixed-methods, within-subjects study with 30 programmers showed that edit model leads to:

-Significantly faster task completion time

![](/data/huangyc/Document2All/posterDataOutput_vlm/Generation Probabilities are Not Enough: Improving Error Highlighting for AI Code Suggestions_poster/auto/images/images/fig_1.jpg)  
Significantly more localized edits

![](/data/huangyc/Document2All/posterDataOutput_vlm/Generation Probabilities are Not Enough: Improving Error Highlighting for AI Code Suggestions_poster/auto/images/images/fig_2.jpg)

# Stronger preference

![](/data/huangyc/Document2All/posterDataOutput_vlm/Generation Probabilities are Not Enough: Improving Error Highlighting for AI Code Suggestions_poster/auto/images/images/fig_3.jpg)

compared to the generation probability and no-highlights