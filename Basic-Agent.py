from autogen import ConversableAgent

config_list = [{
    # Let's choose the model
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

llm_config = {"config_list": config_list}

#Creating the agent
agent = ConversableAgent(
    name="ChatBot",
    llm_config=llm_config,
    human_input_mode="NEVER"
)


#Generating reply from the agent
reply = agent.generate_reply(
    messages=[{"content": "How to make delicious ramen?", "role": "user"}]
)

print(reply)


reply = agent.generate_reply(
    messages=[{"content": "How to set up a marketing campaign?", "role": "user"}]
)

print(reply)