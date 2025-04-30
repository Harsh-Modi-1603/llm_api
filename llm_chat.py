import os
import json
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from llm import test_case_prompt  # Reuse the prompt

# 🔐 Load service account credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not credentials_json:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable is missing.")

credentials_dict = json.loads(credentials_json)

# 🔁 Initialize Gemini LLM (chat-capable)
llm_model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    credentials=credentials_dict
)

# 🧪 Prompt for test case generation
def generate_prompt(user_story, jira_id, acceptance_criteria=""):
    return test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )

# 🚀 Generate test cases using chat-compatible model
async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = generate_prompt(user_story, jira_id, acceptance_criteria)
    result = await llm_model.ainvoke(prompt)
    return result.content

# 💬 Interactive chat support
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in software testing."),
    ("human", "{question}")
])

async def chat_with_llm(question: str):
    prompt = chat_prompt.format_messages(question=question)
    result = await llm_model.ainvoke(prompt)
    return result.content
