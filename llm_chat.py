# llm_chat.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate

# ✅ Use Gemini-Pro (chat model)
llm_model = ChatGoogleGenerativeAI(
    model="gemini-pro",  # Must be chat-capable
    temperature=0.7
)

# 📄 Prompt template for test case generation
test_case_prompt = PromptTemplate.from_template("""
You are a test case generation assistant.

Generate detailed test scenarios and test cases in plain text format (NOT markdown).

User Story:
{user_story}

JIRA ID:
{jira_id}

Acceptance Criteria:
{acceptance_criteria}
""")

# Function to fill the test case prompt
def generate_prompt(user_story, jira_id, acceptance_criteria=""):
    return test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )

# 🚀 Test case generation using chat model
async def generate_test_cases_with_chat_model(user_story, jira_id, acceptance_criteria=""):
    prompt = generate_prompt(user_story, jira_id, acceptance_criteria)
    response = await llm_model.ainvoke(prompt)
    return response.content

# 💬 Chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in software testing."),
    ("human", "{question}")
])

# 🧠 Chat with the LLM
async def chat_with_llm(question: str):
    prompt = chat_prompt.format_messages(question=question)
    response = await llm_model.ainvoke(prompt)
    return response.content
