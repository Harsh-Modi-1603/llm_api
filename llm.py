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
   - **Test Scenarios**: High-level descriptions of what needs to be tested. These should focus on broader aspects of the functionality.
   - **Test Cases**: Detailed, step-by-step instructions for testing specific aspects of the test scenarios. Each test scenario should have 2-3 test cases covering positive, negative, and edge cases.
5. Ensure the generated output covers at least 95% of possible test scenarios and test cases.
6. Maintain strict format consistency for readability and usability.
7. Use the provided example to understand the expected output structure.
8. The response should include a minimum of 25-30 test scenarios and 2-3 test cases per scenario.
9. Test scenarios and test cases should be distinct. For example:
   - Test Scenario: Validate whether the login functionality works as expected.
   - Test Cases:
     - Validate whether the user can log in with valid credentials.
     - Validate whether the user cannot log in with invalid credentials.
     - Validate whether the user cannot log in with empty fields.
10. Ensure the test cases are detailed and exhaustive, covering all possible steps and outcomes.

---
Example Output Format
(Use this exact format in your response)

---
User Story  
Story Title [Extracted from JIRA]  
Description [Extracted from JIRA]  
JIRA Issue ID {jira_id}  

Acceptance Criteria  
{acceptance_criteria}

---
Test Scenarios  

TS-01: Validate whether [High-level description of the scenario].  
TS-02: Validate whether [High-level description of the scenario].  
TS-03: Validate whether [High-level description of the scenario].  
...continue listing all test scenarios...

---
Test Cases  

TC-01: Validate whether [Detailed description of the test case].  
- Preconditions: [Any necessary setup before execution]  
- Test Data: [Example test data if applicable, with the disclaimer "The test data is just for guidance and the actual test data is to be determined by the user."]  
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

---
Response Format Requirements  
1. Maintain structure exactly as shown above.  
2. Provide all test scenarios first, followed by test cases.  
3. Include a minimum of 25-30 test scenarios covering different cases depending on the user story.  
4. Generate 2-3 detailed test cases per scenario.  
5. Strictly follow the example format for readability and consistency.  
6. Avoid unnecessary explanations—output should be directly usable by QA engineers.  
7. Ensure the test scenarios and test cases are distinct and exhaustive, covering all possible aspects of the user story.
"""
)
