import argument_based_agent as agent
import llamaAPI as LLM_API
import utils

def get_argument_by_number(file_path, argument_number):
    with open(file_path, "r") as file:
        content = file.read()
    arguments = content.split("\n\n")
    if argument_number < 1 or argument_number > len(arguments):
        return "Invalid argument number. Please provide a number between 1 and 25."
    return arguments[argument_number - 1].strip()

statement = "People should have a right to keep and bear arm."

expression_by_polarity = {
    "0": "You are absolutely against the right to bear arm.",
    "1": "You are agains right to bear arm but you may be not so sure.",
    "2": "You are neutral about right to bear arm.",
    "3": "You like the idea of the right to bear arm, but you are not so sure.",
    "4": "You think that right to bear arm is essential. You are absolutely in favor of the right to bear arms.",
}

# It's not what I want. I want 0 to be agressively against, even not using any positive arguments

pro_arguments = " ".join([get_argument_by_number("pro_arguments.txt", i) for i in []])
con_arguments = " ".join([get_argument_by_number("con_arguments.txt", i) for i in [7, 5, 3, 2, 1, 4]])
agent_instance1 = agent.Agent(**{
    "user_id": 1,
    "pro_arguments": pro_arguments,
    "con_arguments": con_arguments,
    "opinion": "",
    "polarity": 0
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

HTML_REPRESENTATION_FILE = "view_dialog.html"

def generate_message(agent):
    msg = agent.write_message(statement, expression_by_polarity)
    print(f"Agent{agent.user_id}'s message: ", msg, '\n')
    print(f"Agent{agent.user_id}'s polarity: ", agent.polarity, '\n')
    utils.message_to_html(HTML_REPRESENTATION_FILE, f"""
<div class="agent-container">
    <span class="agent-id">Agent {agent.user_id}:</span>
    <span class="agent-text-{agent.polarity}">{msg}</span>
</div>
""")
    return msg

def react(agent_to, agent_from, message):
    reaction = agent_to.react_to_message(message, statement, agent_from.user_id)
    print(f"Agent{agent_to.user_id}'s arguments: ", agent_to.pro_arguments, '\n=====\n', agent_to.con_arguments, '\n')
    utils.message_to_html(HTML_REPRESENTATION_FILE, f"""
<div class="agent-container">
    <span class="agent-id">CURRENT ARGUMENTS of agent {agent_to.user_id}:</span>\n
    <span class="pro-args">{agent_to.pro_arguments}</span>\n
    <span class="con-args">{agent_to.con_arguments}</span>
</div>
""")
    return reaction

utils.create_html(HTML_REPRESENTATION_FILE)

msg1 = generate_message(agent_instance1)

msg2 = generate_message(agent_instance2)
react(agent_instance1, agent_instance2, msg2)

msg2 = generate_message(agent_instance2)
react(agent_instance1, agent_instance2, msg2)

msg1 = generate_message(agent_instance1)
react(agent_instance2, agent_instance1, msg1)

msg2 = generate_message(agent_instance2)
react(agent_instance1, agent_instance2, msg2)

msg1 = generate_message(agent_instance1)
react(agent_instance2, agent_instance1, msg1)

msg2 = generate_message(agent_instance2)
msg1 = generate_message(agent_instance1)

utils.finish_with_html(HTML_REPRESENTATION_FILE)


# from argument_based_agent import classify_opinion_numerically

# print(classify_opinion_numerically(statement, "I'm absolutely against the right to bear arms", expression_by_polarity))
