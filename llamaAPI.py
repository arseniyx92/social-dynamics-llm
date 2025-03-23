from langchain_community.chat_models import ChatOllama 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from utils import debug_print

def callLLM(system_prompt, user_prompt, model = "mistral"):
    llm = ChatOllama(model = model) 

    template = """
        {user_prompt}
        ------------------------------
        {system_prompt}

        Print text as a real human messaging in solcial network, less than 100 words, within one paragraph.
        """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    output = "".join(AIMessage(content=chain.stream({
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    })).content)

    # with open("log.txt", 'a') as file:
    #     file.write("PROMPTS:\n" + system_prompt + '\n' + user_prompt + "\n###########################\n")
    #     file.write("OUTPUT: " + output + '\n\n')
    debug_print("PROMPTS:\n" + system_prompt + '\n' + user_prompt + "\n###########################\n")
    debug_print("OUTPUT: " + output + '\n\n')

    return output

def directly_callLLM(given_prompt):
    llm = ChatOllama(model = "llama3.2") 

    template = """{prompt}"""
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    output = "".join(AIMessage(content=chain.stream({
        "prompt": given_prompt
    })).content)

    # with open("log.txt", 'a') as file:
    #     file.write("PROMPTS:\n" + system_prompt + '\n' + user_prompt + "\n###########################\n")
    #     file.write("OUTPUT: " + output + '\n\n')
    debug_print("PROMPT:\n" + given_prompt + "\n###########################\n")
    debug_print("OUTPUT: " + output + '\n\n')

    return output