# llm_chat.py

from langchain.prompts import ChatPromptTemplate
from llm import test_case_prompt, llm_model  # Reuse from your existing llm.py

# Prompt for test case generation
def generate_prompt(user_story, jira_id, acceptance_criteria=""):
    return test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )

# Initial test case generation
async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = generate_prompt(user_story, jira_id, acceptance_criteria)
    result = await llm_model.ainvoke(prompt)
    return result.content

# Generic chat response after generation
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in software testing."),
    ("human", "{question}")
])

async def chat_with_llm(question: str):
    prompt = chat_prompt.format_messages(question=question)
    response = await llm_model.ainvoke(prompt)
    return response.content
