from autogen import AssistantAgent, ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
import os
from datetime import date
from IPython.display import Image


os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"

# config_list = [{
#     "model": "qwen2.5:latest",
#     "base_url": "http://localhost:11434/v1",
#     "api_key": "ollama",
# }]

config_list = [{
    "model": "gemma2-9b-it",
    "api_type": "groq",
    "api_key": os.getenv("GROQ_API_KEY"),
}]

llm_config = {
    "config_list": config_list
}

#Create an executor instance
executor = LocalCommandLineCodeExecutor(
    timeout=10,
    work_dir="coding"
)

code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
    default_auto_reply= "Please continue. If everything is done. reply 'TERMINATE'."
)

#Agent with code writing ability
code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER"
) 

# code_writer_agent_system_message = code_writer_agent.system_message
# print(code_writer_agent_system_message)

#Defining stock analysis
current_date = date.today()

instruction = f"""
As of {current_date}, please generate a graph displaying the year-to-date (YTD) stock performance for NVIDIA and Tesla.

Ensure that you:
1. Write the necessary code within a markdown code block
2. Save the resulting graph as an image file named 'ytd_stock_gains.png'
"""

#Initiate the chat
chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=instruction
)

#Check the output
Image(os.path.join("coding", "ytd_stock_gains.png"))
