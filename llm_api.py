from fastapi import FastAPI
from pydantic import BaseModel
from llm import test_case_prompt, llm_model

app = FastAPI()

class RequestModel(BaseModel):
    user_story: str
    jira_id: str
    acceptance_criteria: str = ""

@app.post("/generate")
async def generate_test_cases(data: RequestModel):
    prompt = test_case_prompt.format(
        user_story=data.user_story,
        jira_id=data.jira_id,
        acceptance_criteria=data.acceptance_criteria
    )
    response = await llm_model.ainvoke(prompt)
    return {"testCases": response}

@app.get("/")
def root():
    return {"message": "LLM API is live"}
