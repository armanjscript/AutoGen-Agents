from autogen import ConversableAgent, UserProxyAgent, GroupChat, GroupChatManager, AssistantAgent

config_list = [{
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

llm_config = {
    "config_list": config_list
}

task = "Analyze the daily closing prices of Apple (AAPL) stock for the past 1 month and create a brief report."

user_proxy = UserProxyAgent(
    name="Admin",
    system_message="Give the task, and send instructions to the writer to refine the stock analysis report.",
    code_execution_config=False,
    llm_config=llm_config,
    human_input_mode="ALWAYS"
)

planner = ConversableAgent(
    name="Planner",
    system_message="""
    Given a task, please determine what stock information is needed to complete the task.
    Please note that the information will all be retrieved using Python code.
    Please only sugget information that can be retrieved using Python code.
    After each step is done by others, check the progress and instruct the remaining steps.
    If a step fails. try to workaround.
    """,
    llm_config=llm_config
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    description="An engineer that writes code to fetch and analyze stock data based on the plan provided by the planner."
)

executor =  ConversableAgent(
    name="Executor",
    system_message="Execute the code written by the engineer and report the stock data results.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 6,
        "work_dir": "coding",
        "use_docker": False,
    },
)

writer = ConversableAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="Stock Analysis Report. Please write stock analysis report in markdown format (with relevant titles).",
    description = "Writer. Write Stock analysis report based on the code execution results and take feedback from admin to refine the report."
)

#Define Group Chat
groupchat = GroupChat(
    agents = [user_proxy, engineer, writer, executor, planner],
    messages=[],
    max_round=10
)


manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

groupchat_result = user_proxy.initiate_chat(
    manager,
    message=task
)