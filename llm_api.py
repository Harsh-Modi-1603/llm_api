from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import test_case_prompt, llm_model
import uuid
import asyncio

app = FastAPI()

# Enable CORS for browser-side fetch from Forge frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["https://your-jira-site.atlassian.net"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (use Redis/DB in production)
job_store = {}

class RequestModel(BaseModel):
    user_story: str
    jira_id: str
    acceptance_criteria: str = ""

@app.post("/generate")
async def generate(data: RequestModel):
    job_id = str(uuid.uuid4())
    job_store[job_id] = {"status": "pending", "result": None}

    # Run job in background
    asyncio.create_task(run_llm_job(job_id, data))
    return {"job_id": job_id}

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = job_store.get(job_id)
    if not job:
        return {"status": "not_found"}
    return job

async def run_llm_job(job_id, data):
    prompt = test_case_prompt.format(
        user_story=data.user_story,
        jira_id=data.jira_id,
        acceptance_criteria=data.acceptance_criteria
    )
    try:
        result = await llm_model.ainvoke(prompt)
        job_store[job_id] = {
            "status": "complete",
            "result": result.content
        }
    except Exception as e:
        job_store[job_id] = {
            "status": "error",
            "result": str(e)
        }

@app.get("/")
def root():
    return {"message": "LLM async job API is live"}
