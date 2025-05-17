from typing import Tuple
import argument_based_agent as agentLib
import utils
import multiprocessing

def get_argument_by_number(file_path, argument_number):
    with open(file_path, "r") as file:
        content = file.read()
    arguments = content.split("\n")
    if argument_number < 1 or argument_number > len(arguments):
        return "Invalid argument number. Please provide a number between 1 and 25."
    line = arguments[argument_number - 1]
    return line.strip().split(']')[-1].strip()

statement = "People should have a right to keep and bear arm."

def get_opinion(agent, client):
    opinion = agent.create_opinion(statement, client)
    # print(f"OPINION {agent.user_id}: ", opinion)
    result = agentLib.classify_opinion_numerically(statement, opinion, client)
    return result

all_pro_arguments = [get_argument_by_number("../arguments/guns_pro.txt", i) for i in range(1, 11)]
all_con_arguments = [get_argument_by_number("../arguments/guns_con.txt", i) for i in range(1, 11)]

output_file = "results.txt"

def worker(task, lock, filename):
    import random
    random.seed()  # Reset seed for process
    
    # Create separate Ollama client instance
    from ollama import Client
    client = Client()
    """Process wrapper with file writing and error handling"""
    pro_indices, con_indices = task
    pro_arguments = [all_pro_arguments[i] for i in pro_indices]
    con_arguments = [all_con_arguments[i] for i in con_indices]
    try:
        agent_instance = agentLib.Agent(**{
            "user_id": 1,
            "pro_arguments": pro_arguments,
            "con_arguments": con_arguments
        })
        score = get_opinion(agent_instance, client)
        with lock:
            with open(filename, 'a') as f:
                f.write(f'{pro_indices},{con_indices},{score}\n')
    except Exception as e:
        print(f"Error processing '{statement[:20]}...': {str(e)}")

if __name__ == '__main__':
    with open(output_file, 'w') as f:
        f.write("pros,cons,score\n")

    manager = multiprocessing.Manager()
    lock = manager.Lock()

    processes = []
    n = 10
    cnt = 1
    for pros in range(2**cnt):
        for cons in range(2**cnt):
            pro_indices = []
            con_indices = []
            for i in range(n):
                if (2**i)&pros > 0:
                    pro_indices.append(i)
                if (2**i)&cons > 0:
                    con_indices.append(i)
            for i in range(3):
                task = (pro_indices, con_indices)
                p = multiprocessing.Process(
                    target=worker,
                    args=(task, lock, output_file)
                )
                processes.append(p)
                p.start()

    for p in processes:
        p.join()