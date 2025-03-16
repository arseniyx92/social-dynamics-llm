import agent

if __name__ == "__main__":
    LLM_agent = agent.Agent(
        persona = "Name: Alice\nInitial belief: You strongly think global warning is a government conspiracy.\nGender: Female",
        topic = "Is climate change a government conspiracy?",
        restrictions = "Remember, throughout the interactions, you are alone in your room without any access to the Internet. Few people will exchange their opinion with you. So your opinion may change only within these interactions.",
        confirmation_bias="Remember, you are role-playing as a real person. You may change your opinion whenever you like.",
        # confirmation_bias = "Remember, you are role-playing as a real person. Like humans, you have confirmation bias. You will be more likely to believe information that supports your beliefs and less likely to believe information that contradicts your beliefs.",
        memory = ""
    )
    john_agent = agent.Agent(
        persona="",
        topic="",
        restrictions="",
        confirmation_bias="",
        memory="",
        is_fake=True,
        fake_message="I'm John and I would like to share my opinion about the climate change. I think it's not fake."
    )
    mary_agent = agent.Agent(
        persona="",
        topic="",
        restrictions="",
        confirmation_bias="",
        memory="",
        is_fake=True,
        fake_message="My name is Mary. I don't know what kinda fake news everyone's eatin', I've seen my grandpa's snowflake pictures from the 60s and they're still out there, folks! Climate change is real, it's just us burnin' too much gas and pollutin' the air, can't deny science, gotta take action."
    )
    LLM_agent.React_on_message(john_agent.Write_message())
    LLM_agent.React_on_message(mary_agent.Write_message())
    print(LLM_agent)