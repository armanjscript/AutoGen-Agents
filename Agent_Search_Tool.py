from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, register_function, config_list_from_json
from tavily import TavilyClient
import os
from typing import Annotated

config_list = [{
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

llm_config = {
    "config_list": config_list
}

os.environ["TAVILY_API_KEY"] = "YOUR_TAVILY_API_KEY"

# Set Tavily Search Web Tool
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_tool(query: Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:
    try:
        return tavily.get_search_context(query=query, search_depth="basic")
    except Exception as e:
        return f"Error: {str(e)}"

# Adding the ReACt prompt
ReAct_prompt = """
Answer the following questions as best you can. You have access to tools provided. 

Use the following format:

Question: the input question you must answer 
Thought: you should always think about what to do 
Action: the action to take 
Action Input: the input to the action 
Observation: the result of the action 
... (this process can repeat multiple times) 
Thought: I now know the final answer 
Final Answer: the final answer to the original input question 

Begin! 
Question: {input} 
"""

def react_prompt_message(sender, recipient, context):
    print(f"Context: {context}")  # Debug print
    return ReAct_prompt.format(input=context["question"])

# Define Agents
user_proxy = UserProxyAgent(
    name="User",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config=False
)

research_assistant = AssistantAgent(
    name="Assistant",
    system_message="""
                    You are a helpful research assistant who has ability to search the web using the provided tools. 
                    Only use the tools you have been provided it. Reply TERMINATE when the task is done. 
                   """,
    llm_config=llm_config
)

# Register the search tool
register_function(
    search_tool,
    caller=research_assistant,
    executor=user_proxy,
    name="search_tool",
    description="Search the web for the given query"
)

user_proxy.initiate_chat(
    research_assistant,
    message=react_prompt_message,
    question="Who won the T20 cricket world cup in 2024?"
)