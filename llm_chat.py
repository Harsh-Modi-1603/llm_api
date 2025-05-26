import os
import json
import base64
from typing import Dict, List
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from llm import test_case_prompt


if "GOOGLE_CREDENTIALS_BASE64" in os.environ:
    decoded_json = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_BASE64"])
    credentials_info = json.loads(decoded_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
else:
    raise EnvironmentError("Missing GOOGLE_CREDENTIALS_BASE64 environment variable.")


llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    credentials=credentials,
    convert_system_message_to_human=True
)


memory_store: Dict[str, List[Dict[str, str]]] = {}



async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )
    result = await llm_model.ainvoke(prompt)
    
    memory_store[jira_id] = [
        {"role": "system", "content": "You are a helpful assistant specialized in software testing."},
        {"role": "user", "content": prompt},
        {"role": "ai", "content": result.content}
    ]
    return result.content



async def chat_with_contextual_llm(jira_id: str, message: str) -> str:
    if jira_id not in memory_store:
        memory_store[jira_id] = [
            {"role": "system", "content": "You are a helpful assistant specialized in software testing."}
        ]

    # Append new user message to context
    memory_store[jira_id].append({"role": "user", "content": message})

    # Invoke Gemini with full context
    response = await llm_model.ainvoke(memory_store[jira_id])

    # Add model's response to memory
    memory_store[jira_id].append({"role": "ai", "content": response.content})

    return response.content