from langchain_community.chat_models import ChatOllama 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

def callLLM(system_prompt, user_prompt):
    llm = ChatOllama(model = "llama3.2") 

    template = """
        System prompt: {system_prompt}
        ------------------------------
        User prompt: {user_prompt}

        Your answer should be less than 20 words.
        """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    output = "".join(AIMessage(content=chain.stream({
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    })).content)

    print("PROMPTS:\n" + system_prompt, user_prompt, "\n###########################")
    for ch in output:
            if str.isdigit(ch):
                print("OUTPUT:", int(ch), '\n')
                return output
    print("OUTPUT:", output, '\n')

    return output