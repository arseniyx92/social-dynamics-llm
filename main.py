import argument_based_agent as agent
import llamaAPI as LLM_API

def get_argument_by_number(file_path, argument_number):
    with open(file_path, "r") as file:
        content = file.read()
    arguments = content.split("\n\n")
    if argument_number < 1 or argument_number > len(arguments):
        return "Invalid argument number. Please provide a number between 1 and 25."
    return arguments[argument_number - 1].strip()

statement = "People should have a right to keep and bear arms."

expression_by_polarity = {
    "0": "You hate the probability that people may bear arms. You are absolutely negative about this statement.",
    "1": "You are agains right to bear arms but you may be not so sure.",
    "2": "You are neutral about right to bear arms.",
    "3": "You like the idea of the right to bear arms, but you are not so sure.",
    "4": "You think that right to bear arms is essential. You are fully into allowing people to bear arms.",
}

# It's not what I want. I want 0 to be agressively against, even not using any positive arguments

pro_arguments = " ".join([get_argument_by_number("pro_arguments.txt", i) for i in [1, 4, 6]])
con_arguments = " ".join([get_argument_by_number("con_arguments.txt", i) for i in [7, 5, 3, 2]])
agent_instance1 = agent.Agent(**{
    "user_id": 1,
    "pro_arguments": pro_arguments,
    "con_arguments": con_arguments,
    "opinion": "",
    "polarity": 1
})

pro_arguments = " ".join([get_argument_by_number("pro_arguments.txt", i) for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]])
con_arguments = " ".join([get_argument_by_number("con_arguments.txt", i) for i in []])
agent_instance2 = agent.Agent(**{
    "user_id": 2,
    "pro_arguments": pro_arguments,
    "con_arguments": con_arguments,
    "opinion": "",
    "polarity": 4
})

msg1 = agent_instance1.write_message(statement, expression_by_polarity)
print("Agent1's message: ", msg1, '\n')
print("Agent1's polarity: ", agent_instance1.polarity, '\n')

msg2 = agent_instance2.write_message(statement, expression_by_polarity)
print("Agent2's message: ", msg2, '\n')
print("Agent2's polarity: ", agent_instance2.polarity, '\n')

reaction = agent_instance1.react_to_message(msg2, statement)
print("Agent1's arguments: ", agent_instance1.pro_arguments, '\n=====\n', agent_instance1.con_arguments, '\n')

msg2 = agent_instance2.write_message(statement, expression_by_polarity)
print("Agent2's message: ", msg2, '\n')
print("Agent2's polarity: ", agent_instance2.polarity, '\n')

reaction = agent_instance1.react_to_message(msg2, statement)
print("Agent1's arguments: ", agent_instance1.pro_arguments, '\n=====\n', agent_instance1.con_arguments, '\n')

msg11 = agent_instance1.write_message(statement, expression_by_polarity)
print("Agent1's message: ", msg11, '\n')
print("Agent1's polarity: ", agent_instance1.polarity, '\n')