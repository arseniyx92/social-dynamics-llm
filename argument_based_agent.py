import json
import llamaAPI as LLM_API
from utils import debug_print

class Agent:
    def __init__(self, user_id, pro_arguments, con_arguments, opinion, polarity):
        self.user_id = user_id
        self.pro_arguments = pro_arguments
        self.con_arguments = con_arguments
        self.opinion = opinion
        self.polarity = polarity

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "pro_arguments": self.pro_arguments,
            "con_arguments": self.con_arguments,
            "opinion": self.opinion
        }
    
    def write_message(self, statement, expression_by_polarity):
        expr = expression_by_polarity[str(self.polarity)]
        debug_print("#########MESSAGE GENERATION#########")
        self.opinion = LLM_API.callLLM(f"Pro-arguments (you won't use them if you are completely against): {self.pro_arguments}\nCon-arguments (you won't use them if you are in favor): {self.con_arguments}. You may use some of them internally but only to make up an opinion to express.", f"Generate opinion about the statement: {statement} using pros and cons and maybe coming up with some new ones. {expr}, behave more personal, like a human - your opinion may change.")
        debug_print("#########POLARITY GENERATION#########")
        self.polarity = classify_opinion_numerically(statement, self.opinion, expression_by_polarity)
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
        self.pro_arguments = LLM_API.directly_callLLM(f"""List only argumnets in favor of the statement: {statement}
        in this text:
        `{feedback}`
        """)
        self.con_arguments = LLM_API.directly_callLLM(f"""List only argumnets against the statement: {statement}
        in this text:
        `{feedback}`
        """)
        return feedback
        

def save_to_json(obj) -> str:
    return json.dumps(obj.to_dict(), indent=4)

def load_from_json(cls, data):
    return cls(**json.loads(data))

def classify_opinion_numerically(statement, opinion, expression_by_polarity):
        tries = 3
        while tries > 0:
            system_prompt = f""""Classify given opinion about the statement: `{statement}`.
            Return score number from 0 to 4 where 0 mean that opinion is completely agains of the statement and 4 that opinion is completely positive about it, so 2 is neutral.
            You can use this grading: {str(expression_by_polarity)}
            """
            user_prompt = f"Given opinion: {opinion}"
            result = LLM_API.callLLM(system_prompt, user_prompt, "llama3.2")
            for i in range(len(result)):
                if str.isdigit(result[i]):
                    num = int(result[i])
                    if i != 0 and result[i-1] == '-':
                        num *= -1
                    if num > 5:
                        num = 5
                    if num < 0:
                        num = 0
                    return num
            tries -= 1
        return -1