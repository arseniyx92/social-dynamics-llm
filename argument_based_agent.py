import json
import llamaAPI as LLM_API
from utils import debug_print
import ollama

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
    
    def create_opinion(self, statement):
        opinion_prompt = """Analyze the following debate structure and craft a nuanced personal opinion:
            **Topic Statement**: {statement}

            **Pro Arguments**:
            {pro_args}

            **Con Arguments**:
            {con_args}

            Create a first-person perspective opinion that:
            1. Acknowledges valid points from both sides
            2. Demonstrates which arguments carried more weight in the decision
            3. Shows emotional reasoning behind the stance
            4. Maintains logical coherence
            5. Reflects personal priorities/values revealed by chosen arguments

            Format the opinion to:
            - Be 2-3 paragraphs
            - Use conversational language
            - Include phrases like "While I understand..." or "What ultimately convinces me..."
            - Reveal whether the position leans pro, con, or neutral
            - Highlight which specific arguments were most persuasive

            Respond ONLY with the crafted opinion, no commentary."""
        opinion = ollama.generate(
            model='mistral',
            prompt=opinion_prompt.format(
                statement="Stricter gun legislation reduces firearm-related deaths",
                pro_args="\n".join(f"- {arg}" for arg in self.pro_arguments),
                con_args="\n".join(f"- {arg}" for arg in self.con_arguments)
            ),
            options={'temperature': 0.7}
        )
        return opinion


    def react_to_message(self, message, statement, msg_from_user):
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
                new_argument="Military-style weapons account for <5% of gun crimes"
            ),
            options={'temperature': 0.1}  # Maximize consistency
        )
        print(response)

def classify_opinion_numerically(statement: str, message: str) -> int:
    prompt = f"""
        Given the statement: "{statement}", analyze the following message's agreement. 
        Rate numerically from -10 (completely against the statement) to 10 (completely in favor). 
        Consider both direct and implied meanings. Respond ONLY with the integer.

        Message: {message}
        Answer: """
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        options={'temperature': 0.0}  # Minimize randomness for deterministic output
    )
    
    # Extract and validate numeric score
    match = re.search(r'-?\d+', response['response'])
    if match:
        score = int(match.group())
        return max(-10, min(10, score))  # Enforce bounds
    else:
        raise ValueError(f"Failed to parse score from: {response['response']}")
    

def save_to_json(obj) -> str:
    return json.dumps(obj.to_dict(), indent=4)

def load_from_json(cls, data):
    return cls(**json.loads(data))