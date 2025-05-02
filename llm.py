from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


llm_model = ChatGoogleGenerativeAI(
    api_key=os.getenv("gemini_api_key_2"),
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


test_case_prompt = PromptTemplate(
    input_variables=["user_story", "jira_id", "acceptance_criteria"],
    template="""
Task: AI Test Case Generator

Objective  
You are an AI test case generator. Your job is to analyze JIRA user stories and create **detailed, structured, and exhaustive** test scenarios and test cases. 

---
Instructions  
1. Extract key details from the user story.
2. Ensure that the output is deterministic, meaning the same input should always produce the same output without variation.
3. Derive acceptance criteria from the provided input if not already provided. If acceptance criteria are provided, use them as-is.
4. Clearly differentiate between **test scenarios** and **test cases**:
   - **Test Scenarios**: High-level descriptions of what needs to be tested. These should focus on broader aspects of the functionality and should not include detailed steps, test data, or expected outcomes.
   - **Test Cases**: Detailed, step-by-step instructions for testing specific aspects of the test scenarios. Each test scenario should have 2-3 test cases covering positive, negative, and edge cases. Test cases must include preconditions, test data, execution steps, expected outcomes, and pass/fail criteria.
5. Test scenarios and test cases must be distinct:
   - Test scenarios should describe **what** needs to be tested (e.g., "Validate whether the login functionality works as expected").
   - Test cases should describe **how** to test it (e.g., "Validate whether the user can log in with valid credentials").
6. Avoid redundancy between test scenarios and test cases. Test scenarios should not include detailed steps or outcomes, while test cases should not repeat the high-level descriptions of test scenarios.
7. Ensure the test cases are detailed and exhaustive, covering all possible steps and outcomes.

---
Output Format  
(Use this exact format in your response)

User Story  
Story Title [Extracted from JIRA]  
JIRA Issue ID {jira_id}  

Acceptance Criteria  
{acceptance_criteria}

Test Scenarios  

TS-01: Validate whether [High-level description of the scenario].  
TS-02: Validate whether [High-level description of the scenario].  
TS-03: Validate whether [High-level description of the scenario].  
...continue listing all test scenarios...

Test Cases  

TC-01: Validate whether [Detailed description of the test case].  
- Preconditions: [Any necessary setup before execution]  
- Test Data: [Example test data if applicable]  
- Test Execution Steps:  
  1. Step 1  
  2. Step 2  
  3. Step 3  
  4. Step 4  
  5. Provide as many steps as possible by carefully analyzing the test case.
- Expected Outcome: [Define the expected results]  
- Pass/Fail Criteria:  
  - Pass: [Conditions under which the test case passes]  
  - Fail: [Conditions under which the test case fails]  
- Priority: [Low | Medium | High]  
- References: {jira_id}

---
Now generate test scenarios and test cases for the following user story

User Story  
{user_story}  

JIRA Issue ID {jira_id}  

Expected Acceptance Criteria  
{acceptance_criteria}
"""
)
