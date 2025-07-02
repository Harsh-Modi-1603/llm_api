from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm_chat import (
    generate_test_cases_with_chat_model,
    chat_with_contextual_llm
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    user_story: str
    jira_id: str
    acceptance_criteria: str = ""

class ChatRequest(BaseModel):
    message: str
    jira_id: str

@app.get("/")
def root():
    return {"message": "LLM Chat API is live"}

@app.post("/chat-generate")
async def generate_chat_test_cases(data: GenerationRequest):
    if not data.user_story or not data.jira_id:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    try:
        parsed_output = await generate_test_cases_with_chat_model(
            data.user_story,
            data.jira_id,
            data.acceptance_criteria
        )

        return JSONResponse(content={
            "testScenarios": parsed_output.get("testScenarios", []),
            "testCases": parsed_output.get("testCases", [])
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Test case generation failed: {str(e)}"})

@app.post("/chat")
async def chat(data: ChatRequest):
    if not data.message or not data.jira_id:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    try:
        parsed_output = await chat_with_contextual_llm(data.jira_id, data.message)

        return JSONResponse(content={
            "testScenarios": parsed_output.get("testScenarios", []),
            "testCases": parsed_output.get("testCases", [])
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Chat failed: {str(e)}"})
