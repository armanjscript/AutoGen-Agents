from autogen import UserProxyAgent, ConversableAgent, config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability

config_list = [{
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

llm_config = {
    "config_list": config_list
}


#Create agents
teachable_agent = ConversableAgent(
    name="teachable_agent",
    llm_config=llm_config
)

teachability = Teachability(
    reset_db=False,
    path_to_db_dir="./tmp/interactive/teachability_db"
)


teachability.add_to_agent(teachable_agent)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    code_execution_config={"use_docker": False}
)

teachable_agent.initiate_chat(user_proxy, message="Hi, I'm a teachable user assistant! What's on your mind?")