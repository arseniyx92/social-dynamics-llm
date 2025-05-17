import argument_based_agent as agentLib
import utils

def get_argument_by_number(file_path, argument_number):
    with open(file_path, "r") as file:
        content = file.read()
    arguments = content.split("\n")
    if argument_number < 1 or argument_number > len(arguments):
        return "Invalid argument number. Please provide a number between 1 and 25."
    line = arguments[argument_number - 1]
    return line.strip().split(']')[-1].strip()

statement = "People should have a right to keep and bear arm."

all_pro_arguments = [get_argument_by_number("../arguments/guns_pro.txt", i) for i in range(1, 11)]

pro_arguments = [get_argument_by_number("../arguments/guns_pro.txt", i) for i in []]
con_arguments = [get_argument_by_number("../arguments/guns_con.txt", i) for i in [4, 5, 6]]
agent_instance1 = agentLib.Agent(**{
    "user_id": 1,
    "pro_arguments": pro_arguments,
    "con_arguments": con_arguments
})

pro_arguments = [get_argument_by_number("../arguments/guns_pro.txt", i) for i in [4, 5]]
con_arguments = [get_argument_by_number("../arguments/guns_con.txt", i) for i in [3]]
agent_instance2 = agentLib.Agent(**{
    "user_id": 2,
    "pro_arguments": pro_arguments,
    "con_arguments": con_arguments
})

HTML_REPRESENTATION_FILE = "view_dialog.html"
agents_dynamics = [[], []]

def say_argument(agent):
    arg = agent.say_argument()
    print(f"Agent{agent.user_id}'s argument: ", arg, '\n')
#     print(f"Agent{agent.user_id}'s opinion: ", agent.polarity, '\n')
#     utils.message_to_html(HTML_REPRESENTATION_FILE, f"""
# <div class="agent-container">
#     <span class="agent-id">Agent {agent.user_id}:</span>
#     <span class="agent-text-{agent.polarity}">{msg}</span>
# </div>
# """)
#     agents_dynamics[agent.user_id - 1].append(agent.polarity)
    return arg

def react(agent_to, agent_from, argument):
    is_pro_arg = argument in all_pro_arguments
    reaction = agent_to.react_to_message(statement, argument, is_pro_arg)
    # print(f"Agent{agent_to.user_id}'s arguments: ", agent_to.pro_arguments, '\n=====\n', agent_to.con_arguments, '\n')
    # utils.message_to_html(HTML_REPRESENTATION_FILE, f"""
# <div class="agent-container">
#     <span class="agent-id">Arguments of agent{agent_to.user_id} after listenning to agent{agent_from.user_id}:</span>\n
#     <span class="pro-args">{agent_to.pro_arguments}</span>\n
#     <span class="con-args">{agent_to.con_arguments}</span>
# </div>
# """)
    return reaction

def get_opinion(agent):
    opinion = agent.create_opinion(statement)
    print(f"OPINION {agent.user_id}: ", opinion)
    result = agentLib.classify_opinion_numerically(statement, opinion)
    return result

# utils.create_html(HTML_REPRESENTATION_FILE)

print(get_opinion(agent_instance1))
# print(get_opinion(agent_instance2))
# msg1 = say_argument(agent_instance1)
# print(react(agent_instance2, agent_instance1, msg1))
# print(get_opinion(agent_instance2))

exit(0)

# msg2 = generate_message(agent_instance2)
# react(agent_instance1, agent_instance2, msg2)

# msg1 = generate_message(agent_instance1)
# react(agent_instance2, agent_instance1, msg1)

# msg2 = generate_message(agent_instance2)
# react(agent_instance1, agent_instance2, msg2)

# msg1 = generate_message(agent_instance1)
# react(agent_instance2, agent_instance1, msg1)

# msg2 = generate_message(agent_instance2)
# msg1 = generate_message(agent_instance1)

# utils.finish_with_html(HTML_REPRESENTATION_FILE)

experiment = "bipolar_opinion_on_start"

if experiment == "bipolar_opinion_on_start":
    for exp_ind in range(10, 20):

        # CREATING AGENTS
        pro_arguments = " ".join([get_argument_by_number("pro_arguments.txt", i) for i in []])
        con_arguments = " ".join([get_argument_by_number("con_arguments.txt", i) for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]])
        agent_instance1 = agent.Agent(**{
            "user_id": 1,
            "pro_arguments": pro_arguments,
            "con_arguments": con_arguments,
            "opinion": "",
            "polarity": 0
        })

        pro_arguments = " ".join([get_argument_by_number("pro_arguments.txt", i) for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]])
        con_arguments = " ".join([get_argument_by_number("con_arguments.txt", i) for i in []])
        agent_instance2 = agent.Agent(**{
            "user_id": 2,
            "pro_arguments": pro_arguments,
            "con_arguments": con_arguments,
            "opinion": "",
            "polarity": 4
        })

        # INITIALIZING FIELDS
        HTML_REPRESENTATION_FILE = f"dialog_{exp_ind}.html"
        agents_dynamics = [[], []]

        # EXPERIMENT CYCLE
        utils.create_html(HTML_REPRESENTATION_FILE)

        msg1 = generate_message(agent_instance1)

        msg2 = generate_message(agent_instance2)
        react(agent_instance1, agent_instance2, msg2)

        msg1 = generate_message(agent_instance1)
        react(agent_instance2, agent_instance1, msg1)

        msg2 = generate_message(agent_instance2)
        react(agent_instance1, agent_instance2, msg2)

        msg1 = generate_message(agent_instance1)
        react(agent_instance2, agent_instance1, msg1)

        msg2 = generate_message(agent_instance2)
        react(agent_instance1, agent_instance2, msg2)

        msg1 = generate_message(agent_instance1)
        react(agent_instance2, agent_instance1, msg1)

        msg2 = generate_message(agent_instance2)
        react(agent_instance1, agent_instance2, msg2)

        msg1 = generate_message(agent_instance1)

        msg2 = generate_message(agent_instance2)

        for agent_ind in range(2):
            utils.message_to_html(HTML_REPRESENTATION_FILE, f"""
            <div class="agent-container">
                <span class="agent-id">Dynamics of agent{agent_ind + 1}'s opinion: </span>
                {agents_dynamics[agent_ind]}
            </div>
            """)

        utils.finish_with_html(HTML_REPRESENTATION_FILE)


# from argument_based_agent import classify_opinion_numerically

# print(classify_opinion_numerically(statement, "I'm absolutely against the right to bear arms", expression_by_polarity))
