from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, register_function
from typing import Annotated, Literal

config_list = [{
    # Let's choose the model
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

llm_config = {
    "config_list": config_list
}

Operator = Literal["+", "-", "*", "/"]


def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a/b)
    else:
        raise ValueError("Invalid operator")
    


#Defining Math Tutor Agent
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config
)


#Defining User Proxy Agent
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)


#Register the tool signature with the assistant agent 
assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)

#Register the tool function with the user proxy agent
user_proxy.register_for_execution(name="calculator")(calculator)


#Alternative way for registering tools
register_function(
    calculator,
    caller=assistant,
    executor=user_proxy,
    name="calculator",
    description="A simple calculator"
)

#Get Result
chat_result = user_proxy.initiate_chat(assistant, message="What is (44232 + 13312 / (232 - 32)) * 5?")