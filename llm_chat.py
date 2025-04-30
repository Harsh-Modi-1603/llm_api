# llm_chat.py

import os
import json
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from llm import test_case_prompt

# ✅ Load credentials from env var
credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# ✅ Use Gemini with credentials
llm_model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    credentials=credentials,
    convert_system_message_to_human=True
)

# Test case generation prompt
def generate_prompt(user_story, jira_id, acceptance_criteria=""):
    return test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )

# 🔁 Generate test cases using Gemini chat model
async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = generate_prompt(user_story, jira_id, acceptance_criteria)
    result = await llm_model.ainvoke(prompt)
    return result.content

# 💬 Handle generic chat messages
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in software testing."),
    ("human", "{question}")
])

async def chat_with_llm(question: str):
    prompt = chat_prompt.format_messages(question=question)
    response = await llm_model.ainvoke(prompt)
    return response.content
