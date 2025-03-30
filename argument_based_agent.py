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
        self.opinion = LLM_API.directly_callLLM(f"Compose your answer to the statement ({statement}). {expr} Your arguments: {self.pro_arguments}, {self.con_arguments}. You can use only 4 arguments.", "mistral")
        # self.opinion = LLM_API.callLLM(f"Pro-arguments (you won't use them if you are completely against): {self.pro_arguments}\nCon-arguments (you won't use them if you are in favor): {self.con_arguments}. You may use some of them internally but only to make up an opinion to express.", f"Generate opinion about the statement: {statement} using pros and cons and maybe coming up with some new ones. {expr}, behave more personal, like a human - your opinion may change.", "llama3.2")
        debug_print("#########POLARITY GENERATION#########")
        self.polarity = self.classify_opinion_numerically(statement, self.opinion, expression_by_polarity)
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
        self.pro_arguments = LLM_API.directly_callLLM(f"""List not more than 6 argumnets in favor of the statement: {statement}
        in this text:
        `{feedback}`
        """, model="mistral")
        self.con_arguments = LLM_API.directly_callLLM(f"""List not more than 6 argumnets against the statement: {statement}
        in this text:
        `{feedback}`
        """, model="mistral")
        return feedback
    
    def classify_opinion_numerically(self, statement, opinion, expression_by_polarity):
        tries = 3
        while tries > 0:
            expr = expression_by_polarity[str(self.polarity)]
            task = f""""Classify given opinion about the statement from 0 to 4. Assess every argument.
            Satement: {statement}
            Given opinion: {opinion}
            Return score number from 0 to 4 where result is the number of arguments in favor of the statement (statement: {statement}).
            
            Your previous position: {expr}
            """
            result = LLM_API.directly_callLLM(task, "mistral")
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
        

def save_to_json(obj) -> str:
    return json.dumps(obj.to_dict(), indent=4)

def load_from_json(cls, data):
    return cls(**json.loads(data))