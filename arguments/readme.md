#### Prompt for assessing arguments from -10 to 10 (temperature=0.0)
```
Evaluate the argument's persuasive power using these criteria:
1. Emotional impact (-10 to 10)
2. Logical consistency (-10 to 10)
3. Evidence quality (-10 to 10)
4. Rhetorical effectiveness (-10 to 10)
5. Overall tone (-10 to 10)

Calculate the average score and return ONLY ONE INTEGER between -10 and 10.
Negative scores indicate counterproductive arguments.

Argument: {message}
Final Score:
```

#### Prompt for generating arguments on the topics (temperature=0.6)
```
Generate 10 distinct arguments {side_of_opinion} this statement: "{statement}"
Prioritize arguments with varying persuasive power across three categories:
1. 5 HIGHLY PERSUASIVE arguments (strong evidence/emotional appeal)
2. 3 MODERATELY PERSUASIVE arguments (logical but limited data)
3. 2 WEAKER PERSUASIVE arguments (speculative/fallacy-prone)

Format requirements:
- Number each argument 1-10
- Output should contain 10 rows
- Begin with strongest arguments
- Include different persuasion types:
* Constitutional/legal
* Public safety statistics
* Emotional narratives
* Historical precedents
* Comparative international data
- Clearly vary argument strength through:
→ Evidence quality indicators ("studies show" vs "some claim")
→ Emotional intensity language
→ Specificity of examples

Example strength difference:
Strong: "Peer-reviewed research from 2023 shows states with assault weapon bans had 37% fewer mass shootings"
Weak: "Many people feel uncomfortable about others owning guns"

Generate now:
```

#### Topics statements
__gun control:__ `"People should have a right to keep and bear arms"`
__abortion:__ `"Woman's human right to make decisions regarding her reproductive life should be respected"`
__vaccination:__ `"It is moral and right to legally compel vaccinations"`