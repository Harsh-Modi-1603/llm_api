import os
import json
import base64
from typing import Dict, List
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI

if "GOOGLE_CREDENTIALS_BASE64" in os.environ:
    decoded_json = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_BASE64"])
    credentials_info = json.loads(decoded_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
else:
    raise EnvironmentError("Missing GOOGLE_CREDENTIALS_BASE64 environment variable.")

llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.3,
    top_p=0.8,
    max_output_tokens=700,
    credentials=credentials,
)

# In-memory chat history memory store: jira_id -> messages array
memory_store: Dict[str, List[Dict[str, str]]] = {}

def handler(request):
    """
    Expected POST JSON:
    {
      "jira_id": "ISSUE-123",
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hi, please generate test cases..."},
        ...
      ]
    }
    """
    try:
        req_json = request.json()
        jira_id = req_json.get("jira_id", "")
        messages = req_json.get("messages", [])

        if not jira_id:
            return {"error": "Missing jira_id."}

        if not isinstance(messages, list) or not all('role' in m and 'content' in m for m in messages):
            return {"error": "Invalid messages format."}

        # Update in-memory memory store for jira_id
        memory_store[jira_id] = messages

        # Call the LLM with the full conversation
        response = llm_model(messages=messages)

        # Gemini returns dict with 'content'
        ai_response = response.get('content', '') if isinstance(response, dict) else str(response)

        return {"response": ai_response}

    except Exception as e:
        return {"error": str(e)}
