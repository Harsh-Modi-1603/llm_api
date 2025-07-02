import os
import json
import base64
import re
from typing import Dict, List
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
from llm import test_case_prompt
from test_case_extractor import parser

# Load service account credentials
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
    raw_output = result.content.strip()

    try:
        test_scenarios = parser.extract_test_scenarios(raw_output)
        test_cases = parser.extract_test_cases(raw_output)
        parsed_output = {
            "testScenarios": test_scenarios,
            "testCases": test_cases
        }
    except Exception as e:
        raise ValueError(f"Test case generation failed: {e}")

    memory_store[jira_id] = [
        {"role": "system", "content": "You are a helpful assistant specialized in software testing."},
        {"role": "user", "content": prompt},
        {"role": "ai", "content": raw_output}
    ]

    return parsed_output

async def chat_with_contextual_llm(jira_id: str, message: str) -> dict:
    if jira_id not in memory_store:
        memory_store[jira_id] = [
            {"role": "system", "content": "You are a helpful assistant specialized in software testing."}
        ]

    # Append new message with strong system instruction to return structured format
    instruction = (
        "You must return your response strictly in JSON format with two keys: "
        "`testScenarios` and `testCases`. No extra commentary or explanation."
    )
    memory_store[jira_id].append({"role": "user", "content": f"{instruction}\n\n{message}"})

    # Invoke model with updated memory
    response = await llm_model.ainvoke(memory_store[jira_id])
    memory_store[jira_id].append({"role": "ai", "content": response.content})

    raw_output = response.content.strip()

    try:
        test_scenarios = parser.extract_test_scenarios(raw_output)
        test_cases = parser.extract_test_cases(raw_output)
        return {
            "testScenarios": test_scenarios,
            "testCases": test_cases
        }
    except Exception as e:
        raise ValueError(f"Failed to extract structured test cases: {e}")
