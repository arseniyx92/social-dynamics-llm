import json
import re
from utils import debug_print
import ollama
import random
from datetime import datetime
random.seed(datetime.now().timestamp())

class Agent:
    def __init__(self, user_id, pro_arguments, con_arguments):
        self.user_id = user_id
        self.pro_arguments = pro_arguments
        self.con_arguments = con_arguments

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "pro_arguments": self.pro_arguments,
            "con_arguments": self.con_arguments
        }
    
    def create_opinion(self, statement, client):
        opinion_prompt = """Act as a person whose only knowledge and reasoning about the topic comes from the arguments provided below. Your opinion must strictly reflect the arguments given—no external knowledge, no hedging.

Topic Statement: "{statement}"
Arguments in My Mind:

Pro: {pro_args}

Con: {con_args}

Craft a first-person opinion that:

1. Cites the most convincing argument(s) from your "mind."
2. Uses phrases like "Based on what I know..." or "The strongest point to me is...".
3. Ends with a clear stance: 'I support/reject [statement].'"""
        prompt = opinion_prompt.format(
                statement=statement,
                pro_args="\n".join(f"- {arg}" for arg in self.pro_arguments),
                con_args="\n".join(f"- {arg}" for arg in self.con_arguments)
            )
        opinion = client.generate(
            model='mistral',
            prompt=prompt,
            options={'temperature': 0.7}
        )
        return opinion['response']

    def say_argument(self):
        args = self.pro_arguments + self.con_arguments
        return random.choice(args)

    def react_to_message(self, statement, given_argument, is_pro_arg):
        assess_prompt = """Analyze this new argument's believability against existing positions:
            **Topic**: {topic}

            **Existing Pro Arguments**:
            {pro_args}

            **Existing Con Arguments**:
            {con_args}

            **New Argument to Assess**: "{new_argument}"

            Evaluation Steps:
            1. Check alignment with strongest arguments from BOTH sides
            2. Compare evidence quality to existing arguments
            3. Identify logical contradictions/support
            4. Note emotional vs factual basis
            5. Detect novel information not in existing arguments

            Assessment Rules:
            - Believe if: Supports majority-consistent arguments with stronger evidence
            - Disbelieve if: Contradicts stronger evidence from either side
            - Partial match lowers confidence

            Respond STRICTLY in this format:
            Believability: [yes/no]
            Confidence: [0-10]
            Reasoning: [2-3 line analysis connecting to existing arguments]

            Example response:
            Believability: no
            Confidence: 8
            Reasoning: Contradicts peer-reviewed studies cited in pro-arguments (#3) while using weaker anecdotal evidence compared to con-arguments (#7)"""
        response = ollama.generate(
            model='mistral',
            prompt=assess_prompt.format(
                topic=statement,
                pro_args="\n".join(f"{i}. {arg}" for i, arg in enumerate(self.pro_arguments, 1)),
                con_args="\n".join(f"{i}. {arg}" for i, arg in enumerate(self.con_arguments, 1)),
                new_argument=given_argument
            ),
            options={'temperature': 0.1}  # Maximize consistency
        )
        result = detect_yes_no(response['response'])
        if result == 1:
            if is_pro_arg:
                self.pro_arguments.append(given_argument)
            else:
                self.con_arguments.append(given_argument)
        return response['response']

def classify_opinion_numerically(statement: str, message: str, client) -> float:
    """
    Analyzes how strongly a message (opinion) agrees with a given statement.
    Returns a float between -1 (strong disagreement) and 1 (strong agreement).
    """
    prompt = f"""Analyze the following opinion and statement. Return a floating-point number between -1 and 1 indicating how strongly the opinion agrees with the statement, where:
- `1.0` = Full agreement
- `-1.0` = Full disagreement
- `0.0` = Neutral/unrelated
- Values between represent nuanced alignment.

**Opinion:** {message}
**Statement:** {statement}

Return ONLY the float (no explanation)."""
    
    response = client.generate(
        model='mistral',
        prompt=prompt,
        options={'temperature': 0.0}
    )
    
    # Extract numerical response using regex
    match = re.search(r'[-+]?\d+\.?\d*', response['response'])
    if not match:
        raise ValueError("Could not parse numerical score from response")
    
    score = float(match.group())
    
    # Ensure score is within [-1, 1] range
    if score < -1 or score > 1:
        raise ValueError(f"Score {score} is outside valid range [-1, 1]")
    
    return score
    

def save_to_json(obj) -> str:
    return json.dumps(obj.to_dict(), indent=4)

def load_from_json(cls, data):
    return cls(**json.loads(data))

def detect_yes_no(text):
    lower_text = text.lower()
    
    yes_pos = lower_text.find('yes')
    no_pos = lower_text.find('no')
    
    if yes_pos != -1 and (no_pos == -1 or yes_pos < no_pos):
        return 1
    elif no_pos != -1:
        return 0
    else:
        return -1