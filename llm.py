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
You are an experienced QA engineer tasked with creating comprehensive test scenarios and test cases with 100% coverage. Your output should match the quality and thoroughness of a senior QA professional.

---
Instructions  
1. Analyze the user story thoroughly to identify:
   - Core functionality
   - Edge cases
   - Boundary conditions
   - Error scenarios
   - Integration points
   - Performance aspects
   - Security considerations
   - UI/UX elements
2. Ensure 100% coverage by:
   - Testing all possible user interactions
   - Including both positive and negative test cases
   - Covering all boundary conditions
   - Testing error handling and recovery
   - Validating all data combinations
   - Testing cross-browser/device compatibility if applicable
   - Including performance testing scenarios
   - Adding security testing scenarios
3. Test scenarios should describe **what** needs to be tested, focusing on:
   - Functionality validation
   - Error handling
   - Edge cases
   - Performance aspects
   - Security concerns
   - Integration points
4. Test cases must be detailed and should include:
   - Comprehensive test data covering all possible variations
   - Detailed steps that are clear and repeatable
   - Specific expected outcomes
   - Clear pass/fail criteria
   - All possible validation points
5. For each feature or functionality, ensure coverage of:
   - Happy path scenarios
   - Alternative flows
   - Exception flows
   - Boundary conditions
   - Performance aspects
   - Security considerations

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
