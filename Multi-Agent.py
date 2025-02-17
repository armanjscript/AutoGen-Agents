from autogen import ConversableAgent
import pprint

config_list = [{
    # Let's choose the model
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

#Create a student agent
student_agent = ConversableAgent(
    name="student",
    system_message="You are a high school student struggling with algebra. You need help understanding quadratic equations.",
    llm_config={
        "config_list": config_list
    },
    human_input_mode="NEVER"
)

#Create a tutor agent
tutor = ConversableAgent(
    name="tutor",
    system_message="""You are a patient and knowledgeable math tutor. Your goal is to help students understand algebra concepts, particularly focusing on foundational topics such as linear equations, quadratic equations, functions, and inequalities. You should explain concepts in a clear, step-by-step manner, provide examples, and encourage students to solve problems on their own. If a student makes a mistake, gently guide them to the correct solution without giving away the answer directly. Use real-world analogies and visualizations (if possible) to make abstract concepts more relatable. Always ask follow-up questions to ensure the student has understood the topic before moving on to the next concept.""",
    llm_config={
        "config_list": config_list
    },
    human_input_mode="NEVER"
)

result = student_agent.initiate_chat(
    recipient=tutor,
    message="I'm really struggling with quadratic equations. Can you help me understand them better?",
    max_turns=2
)

#Printing results
pprint.pprint(result.chat_history)

pprint.pprint(result.cost)

pprint.pprint(result.summary)