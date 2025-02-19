from autogen import ConversableAgent, UserProxyAgent, initiate_chats, AssistantAgent

config_list = [{
    # Let's choose the model
    "model": "qwen2.5:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}]

#Writer Agent
writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise "
    "blog post {with title} on given topics. You must publish your "
    "writing based on the feedback you recieve and give a refined "
    "version. Only return your final work without additional comments.",
    llm_config={
        "config_list": config_list
    }
)

task = """
        Write a concise but engaging blogpost about GPUs. 
        Make sure the blogpost is within 100 words. 
       """
       
reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])
print(reply)

#Simple review of the post
reviewer = AssistantAgent(
    name="Reviewer",
    is_termination_msg=lambda x: x.get("content", "").find('TERMINATE') > 0,
    llm_config={
        "config_list": config_list
    },
    system_message="You are a reviewer. You review the work of "
    "the writer and provide constructive "
    "feedback to help improve the quality of the content.",
)


res = reviewer.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

#SEO Reviewer
seo_reviewer = AssistantAgent(
    name="SEO_Reviewer",
    llm_config={
        "config_list": config_list
    },
    system_message="As an SEO expert, your role is to analyze and enhance content for optimal search engine performance. "
    "Focus on providing actionable recommendations that boost rankings and drive organic traffic. "
    "Limit your feedback to 3 key points, ensuring they are specific and directly applicable. "
    "Start each review by introducing yourself as an SEO Reviewer.",
)

#Grammatical Reviewer
grammatical_error_reviewer = AssistantAgent(
    name="Grammatical_Error_Reviewer",
    llm_config={
        "config_list": config_list
    },
    system_message="As a grammar specialist , your task is to meticulously examine content "
    "for grammatical errors, punctuation mistakes, and style inconsistencies. "
    "Provide up to 3 key points addressing the most significant grammatical issues. "
    "Ensure your feedback is specific, actionable, and includes examples where approptiate. "
    "Begin each review by introducing your self as a Grammatical Error Reviewer.",
)


#Ethics Reviewer
ethics_reviewer = AssistantAgent(
    name="Ethics_Reviewer",
    llm_config={
        "config_list": config_list
    },
    system_message="As an ethics specialist, your role is to evaluate content for ethical integrity "
    "and identify any potential moral concerns. "
    "Provide up to 3 specific, actionable recommendations to address ethical issues. "
    "Ensure your feedback is concise and directly applicable. "
    "Start each review by introducing yourself as an Ethics Reviewer.",
)

#Meta Reviewer
meta_reviewer = AssistantAgent(
    name="Meta_Reviewer",
    llm_config={
        "config_list": config_list
    },
    system_message="You are a meta reviewer, you aggregate and review "
    "the work of other reviewers and give a final suggestion on the content.",
)



def reflection_message(recipient, messages, sender, config):
    return f"""Review the following content.
        \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"""
        


review_chats = [
{
    "recipient": seo_reviewer ,
    "messgae": reflection_message,
    "summary_method": "reflection_with_llm",
    "summary_args": {
        "summary_prompt": "Return review into as JSON object only:"
        "into a JSON object: "
        "{'Reviewer': '', 'Review': ''}. Here Reviewer Should be your role.",
    },
    "max_turns": 1,
},
{
    "recipient": grammatical_error_reviewer ,
    "messgae": reflection_message,
    "summary_method": "reflection_with_llm",
    "summary_args": {
        "summary_prompt": "Return review into as JSON object only:"
        "into a JSON object: "
        "{'Reviewer': '', 'Review': ''}.",
    },
    "max_turns": 1,
},
{
    "recipient": ethics_reviewer,
    "messgae": reflection_message,
    "summary_method": "reflection_with_llm",
    "summary_args": {
        "summary_prompt": "Return review into as JSON object only:"
        "into a JSON object: "
        "{'Reviewer': '', 'Review': ''}.",
    },
    "max_turns": 1,
},
{
    "recipient": meta_reviewer,
    "message": "Aggregate feedback from all reviewers and give final suggestions on the writing.",
    "max_turns": 1,
},
]

meta_reviewer.register_nested_chats(
    review_chats,
    trigger=writer
)

res = meta_reviewer.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)


#Get Summary
print(res.summary)