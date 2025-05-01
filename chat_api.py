from fastapi import FastAPI
from pydantic import BaseModel
from llm_chat import (
    generate_test_cases_with_chat_model,
    chat_with_contextual_llm,
    memory_store
)

app = FastAPI()


# Request models
class GenerationRequest(BaseModel):
    user_story: str
    jira_id: str
    acceptance_criteria: str = ""

class ChatRequest(BaseModel):
    message: str
    jira_id: str  # required to preserve session


@app.get("/")
def root():
    return {"message": "LLM Chat API is live"}


@app.post("/chat-generate")
async def generate_chat_test_cases(data: GenerationRequest):
    if not data.user_story or not data.jira_id:
        return {"error": "Missing required fields: user_story and jira_id"}

    try:
        content = await generate_test_cases_with_chat_model(
            user_story=data.user_story,
            jira_id=data.jira_id,
            acceptance_criteria=data.acceptance_criteria
        )
        return {"testCases": content}
    except Exception as e:
        return {"error": f"Test case generation failed: {str(e)}"}


@app.post("/chat")
async def chat(data: ChatRequest):
    if not data.message or not data.jira_id:
        return {"error": "Missing required fields: message and jira_id"}

    try:
        response = await chat_with_contextual_llm(
            jira_id=data.jira_id,
            message=data.message
        )
        return {"response": response}
    except Exception as e:
        return {"error": f"Chat failed: {str(e)}"}
