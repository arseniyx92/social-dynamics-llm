### Analysing correlation between numeric opinion classification and number of debative arguments

Statement: "People should have a right to keep and bear arms."

!img [mean_opinion_classification_pro_bias.png]

!img [mean_opinion_classification_con_bias.png]

Maybe lack of samples (10 LLM calls for each number of arguments). But only positivewise grading effect visible.

#### Interesting ways of llama's thinking.

Here as we can see the model says that the opinion does not go against the statement (is not negative about it) because is does not use negative language.

```
PROMPTS:
Classify given opinion about the statement: `People should have a right to keep and bear arms.`.  Return number from 0 to 5 where 0 mean that opinion is completely negative about the statement and 5 that opinion is completely positive about it, so 3 is neutral. "Ugh, can we please not even think about making guns more accessible? I know some people say it's for self-defense and property protection, but to me, that just seems like a euphemism for 'I want to be able to shoot things and hurt people'. And don't even get me started on the risk of accidental shootings. It's not worth it. The economic burden alone is staggering - we can't afford to have more guns out there causing chaos and destruction. I'm not buying into the militia nonsense either... let's just keep our guns locked away where they belong." 
###########################
OUTPUT: I'd classify this opinion as a 4 out of 5. The person is strongly opposed to making guns more accessible and believes it's not worth the risks and economic burden. They express concerns about accidental shootings, chaos, and destruction, and dismiss the idea of self-defense and property protection as a euphemism for violence. However, they don't use overtly negative language or make sweeping statements that would categorize their opinion as 0.
```