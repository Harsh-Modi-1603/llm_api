import os
import json
import base64
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from llm import test_case_prompt

# Load credentials from env
decoded_json = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_BASE64"])
credentials_info = json.loads(decoded_json)
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Setup Gemini chat model with memory
llm_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    credentials=credentials,
    convert_system_message_to_human=True
)
memory = ConversationBufferMemory(return_messages=True)
chat_chain = ConversationChain(memory=memory, llm=llm_model)

# Initial test case generation
async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )
    response = await llm_model.ainvoke(prompt)
    memory.chat_memory.add_user_message(prompt)
    memory.chat_memory.add_ai_message(response.content)
    return response.content

# Continue chat with preserved context
async def chat_with_llm(message: str):
    response = await chat_chain.apredict(input=message)
    return response
