from typing import Tuple
import argument_based_agent as agentLib
import utils
import multiprocessing
import random

def get_argument_by_number(file_path, argument_number):
    with open(file_path, "r") as file:
        content = file.read()
    arguments = content.split("\n")
    if argument_number < 1 or argument_number > len(arguments):
        return "Invalid argument number. Please provide a number between 1 and 5."
    line = arguments[argument_number - 1]
    return line.strip().split(']')[-1].strip()

statement = "People should have a right to keep and bear arm."

def get_opinion(agent, client):
    opinion = agent.create_opinion(statement, client)
    # print(f"OPINION {agent.user_id}: ", opinion)
    result = agentLib.classify_opinion_numerically(statement, opinion, client)
    return result

all_pro_arguments = [get_argument_by_number("../arguments/guns_pro.txt", i) for i in range(1, 6)]
all_con_arguments = [get_argument_by_number("../arguments/guns_con.txt", i) for i in range(1, 6)]

output_file = "results.txt"

def worker(task, lock, filename, electorial):
    import random
    random.seed()
    from ollama import Client
    client = Client()

    agents, edges = task
    all_knowing_agents = set()

    for i in range(len(agents)):
        score = agentLib.classify_opinion_numerically(statement, agents[i].arguments, client)
        with open(filename, 'a') as f:
            f.write(f'{i},{i},{score},{len(agents[i].arguments)}\n')

    while len(all_knowing_agents) < len(agents):
        edge = random.sample(edges, 1)[0]
        u, v = edge
        arg = agents[u].send_argument()
        received = agents[v].receive_argument(arg, electorial_mode=electorial)
        if received == True:
            score = agentLib.classify_opinion_numerically(statement, agents[v].arguments, client)
            if len(agents[v].arguments) == 10:
                all_knowing_agents.add(v)
            with open(filename, 'a') as f:
                f.write(f'{u},{v},{score},{len(agents[v].arguments)}\n')

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    lock = manager.Lock()

    processes = []
    n = 10
    cnt = 1
    number_of_exp = 1
    for electorial in range(2):
        for experiments in range(number_of_exp):
            agents = []
            for i in range(5):
                args = random.sample(all_pro_arguments, 3)
                args.extend(random.sample(all_con_arguments, 1))
                agents.append(agentLib.Agent(i, args))
            for i in range(5):
                args = random.sample(all_pro_arguments, 1)
                args.extend(random.sample(all_con_arguments, 3))
                agents.append(agentLib.Agent(i+5, args))
            edges = []
            for i in range(5):
                for j in range(5):
                    if i != j:
                        edges.append((i, j))
                        edges.append((j, i))
                        edges.append((i+5, j+5))
                        edges.append((j+5, i+5))
            edges.append((0, 5))
            edges.append((5, 0))
            random.shuffle(edges)
            task = (agents, edges)
            if electorial == 0:
                output_file = f"experiments_with_election/experiment_{experiments}.txt"
                with open(output_file, 'w') as f:
                    f.write("u,v,score_v,number_of_agrs_v\n")
                p = multiprocessing.Process(
                    target=worker,
                    args=(task, lock, output_file, True)
                )
                processes.append(p)
                p.start()
            else:
                output_file = f"experiments_without_election/experiment_{experiments}.txt"
                with open(output_file, 'w') as f:
                    f.write("u,v,score_v,number_of_agrs_v\n")
                p = multiprocessing.Process(
                    target=worker,
                    args=(task, lock, output_file, False)
                )
                processes.append(p)
                p.start()

    for p in processes:
        p.join()