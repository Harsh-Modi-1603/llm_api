from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_chat import generate_test_cases_with_chat_model, chat_with_llm

app = FastAPI()

# ✅ CORS middleware to allow requests from the Jira Forge frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Replace with specific domain for production like ["https://*.atlassian.net"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Request models
class GenerationRequest(BaseModel):
    user_story: str
    jira_id: str
    acceptance_criteria: str = ""

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "LLM Chat API is live"}

# 🔧 Endpoint for test case generation via chat LLM
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

# 💬 Endpoint for chat interaction
@app.post("/chat")
async def chat(data: ChatRequest):
    if not data.message:
        return {"error": "No chat message provided"}

    try:
        response = await chat_with_llm(data.message)
        return {"response": response}
    except Exception as e:
        return {"error": f"Chat failed: {str(e)}"}
