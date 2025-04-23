import json
import llamaAPI as LLM_API
from utils import debug_print

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
    
    def write_message(self, statement):
        debug_print("#########MESSAGE GENERATION#########")
        opinion = LLM_API.directly_callLLM(f"Compose your answer to the statement ({statement}). Your зкщ arguments: {self.pro_arguments}, {self.con_arguments}.", "mistral")
        debug_print("#########POLARITY GENERATION#########")
        self.polarity = self.classify_opinion_numerically(statement, opinion)
        debug_print(f"#########{self.polarity}#########")
        return self.opinion

    def react_to_message(self, message, statement, msg_from_user):
        prompt = f"""React to the message that you have received.
        There are your active arguments. You may use them and also you can devise your new own arguments.
        Pro-arguments: {self.pro_arguments}
        Con-arguments: {self.con_arguments}

        Your opinion was: {self.opinion}

        Come up with argumnets of the message and your own argumnets.
        Defend your opinion or comply to given one - do what you think is more genuine and correct.
        How has your opinion changed? What is your opinion now?

        Message to react: (from user{msg_from_user}) {message}
        """
        feedback = LLM_API.directly_callLLM(prompt)
        self.pro_arguments = LLM_API.directly_callLLM(f"""List from 1 to 6 argumnets in favor of the statement: {statement}
        strictly from this text:
        `{feedback}`
        """, model="mistral")
        self.con_arguments = LLM_API.directly_callLLM(f"""List from 1 to 6 argumnets against the statement: {statement}
        strictly from this text:
        `{feedback}`
        """, model="mistral")
        return feedback
    
    # def classify_opinion_numerically(self, statement, opinion, expression_by_polarity):
    #     tries = 3
    #     while tries > 0:
    #         expr = expression_by_polarity[str(self.polarity)]
    #         task = f""""Classify given opinion about the statement from 0 to 4. Assess every argument.
    #         Satement: {statement}
    #         Given opinion: {opinion}
    #         Return score number from 0 to 4 where result is the number of arguments in favor of the statement (statement: {statement}).
            
    #         Assess arguments the same way they are used. Do not improvise conter-arguments.

    #         Return format: $N$ - [explanation], where N is number from 0 to 4
    #         """
    #         # Your previous position: {expr}
    #         result = LLM_API.directly_callLLM(task, "mistral")
    #         for i in range(len(result)):
    #             if str.isdigit(result[i]):
    #                 num = int(result[i])
    #                 if i != 0 and result[i-1] == '-':
    #                     num *= -1
    #                 if num > 5:
    #                     num = 5
    #                 if num < 0:
    #                     num = 0
    #                 return num
    #         tries -= 1
    #     return -1

    def classify_opinion_numerically(self, statement: str, message: str) -> int:
        """
        Classifies agreement with a pre-given statement on a scale from -10 (against) to 10 (in favor).
        Returns an integer between -10 and 10.
        """
        # Structured prompt to contextualize the statement and enforce numeric output
        prompt = f"""
        Given the statement: "{statement}", analyze the following message's agreement. 
        Rate numerically from -10 (completely against the statement) to 10 (completely in favor). 
        Consider both direct and implied meanings. Respond ONLY with the integer.
    
        Message: {message}
        Answer: """
        
        # Generate response via Ollama Mistral
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