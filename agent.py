import llamaAPI as LLM_API

class Agent:
    def __init__(self, persona, topic, restrictions, confirmation_bias, memory, is_fake=False, fake_message=''):
        self.topic = topic
        self.persona = persona
        self.restrictions = restrictions
        self.confirmation_bias = confirmation_bias
        self.memory = memory
        self.opinion_trajectory = [self.generate_initial_opinion() if not is_fake else []]
        self.is_fake = is_fake
        self.fake_message = fake_message
    
    def __str__(self):
        result = f"Topic: {self.topic}\n"
        result += f"Persona: {self.persona}\n"
        result += f"Restrictions: {self.restrictions}\n"
        result += f"Confirmation bias: {self.confirmation_bias}\n"
        result += f"Memory: self.memory\n"
        result += str(self.opinion_trajectory)
        return result

    def update_memory(self, type_of_interraction, written_message, reaction):
        if type_of_interraction == 'write':
            self.memory = f"My {len(self.opinion_trajectory)} message: [" + written_message + "]\n" + self.memory
        elif type_of_interraction == 'review':
            self.memory = f"My {len(self.opinion_trajectory)} reaction: [" + reaction + "] on message [" + written_message + "]\n" + self.memory
        else:
            raise Exception("Unknown type of interraction")
        
    def Write_message(self):
        if self.is_fake:
            return self.fake_message
        system_prompt = f"Your persona: {self.persona}\nRestrictions: {self.restrictions}\nYour confirmation bias: {self.confirmation_bias}\nThat's what you remember during the discussion: `{self.memory}`\n"
        user_prompt = f"Text public message about your opinion on the topic: {self.topic}"
        message = LLM_API.callLLM(system_prompt, user_prompt)
        self.update_memory("write", message, "")
        return message
    
    def React_on_message(self, message):
        system_prompt = f"Your persona: {self.persona}\nRestrictions: {self.restrictions}\nYour confirmation bias: {self.confirmation_bias}\nThat's what you remember during the discussion: `{self.memory}`\n"
        user_prompt = f"How your opinion on the topic `{self.topic}` has changed after receiving this message: `{message}`?"
        reaction = LLM_API.callLLM(system_prompt, user_prompt)
        self.update_memory("review", message, reaction)
        self.opinion_trajectory.append(self.generate_opinion(reaction))
        return reaction
    
    def classify_opinion_numerically(self, opinion):
        system_prompt = f"RETURN ONLY ONE NUMBER from the list: [-2, -1, 0, 1, 2]! Classify verbal report about the topic `{self.topic}` into a numeric opinion scale (-2, -1, 0, 1, 2) where -2 mean that you completely disagree with the question and 2 that you completely agree."
        user_prompt = f"Classify opinion: `{opinion}`"
        result = LLM_API.callLLM(system_prompt, user_prompt)
        for ch in result:
            if str.isdigit(ch):
                return int(ch)
        return "UNDEFINED"
    
    def generate_initial_opinion(self):
        system_prompt = f"Your persona: {self.persona}\nRestrictions: {self.restrictions}\nYour confirmation bias: {self.confirmation_bias}"
        user_prompt = f"Express your opinion on the topic: {self.topic}"
        initial_opinion = LLM_API.callLLM(system_prompt, user_prompt)
        return (initial_opinion, self.classify_opinion_numerically(initial_opinion))

    def generate_opinion(self, last_reaction):
        system_prompt = f"Your persona: {self.persona}\nRestrictions: {self.restrictions}\nYour confirmation bias: {self.confirmation_bias}\nYour thoughts records: \n {self.memory}"
        user_prompt = f"Express your opinion on the topic `{self.topic}`"
        opinion = LLM_API.callLLM(system_prompt, user_prompt)
        return (opinion, self.classify_opinion_numerically(opinion))