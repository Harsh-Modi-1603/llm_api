import os
import json
import base64
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from llm import test_case_prompt

# ✅ Decode service account JSON from base64
if "GOOGLE_CREDENTIALS_BASE64" not in os.environ:
    raise EnvironmentError("Missing GOOGLE_CREDENTIALS_BASE64 environment variable.")

decoded_json = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_BASE64"])
credentials_info = json.loads(decoded_json)
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# ✅ Initialize Gemini with correct credentials
llm_model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    credentials=credentials
)

# Prompt formatting
def generate_prompt(user_story, jira_id, acceptance_criteria=""):
    return test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )

# Generate test cases
async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = generate_prompt(user_story, jira_id, acceptance_criteria)
    result = await llm_model.ainvoke(prompt)
    return result.content

# Chat interface
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in software testing."),
    ("human", "{question}")
])

async def chat_with_llm(question: str):
    prompt = chat_prompt.format_messages(question=question)
    response = await llm_model.ainvoke(prompt)
    return response.content
