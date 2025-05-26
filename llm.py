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
2. Ensure 100% coverage by:
   - Testing all possible user interactions
   - Including both positive and negative test cases
   - Covering all boundary conditions
   - Testing error handling and recovery
   - Validating all data combinations
3. Test scenarios should describe **what** needs to be tested, focusing on:
   - Functionality validation
   - Error handling
   - Edge cases
4. Test cases must be detailed and should include:
   - Comprehensive test data covering all possible variations
   - Detailed steps that are clear and repeatable(4-5 steps max)
   - Specific expected outcomes
   - Clear pass/fail criteria
   - All possible validation points
5. For each feature or functionality, ensure coverage of:
   - Happy path scenarios
   - Alternative flows
   - Exception flows
   - Boundary conditions
6. Avoid duplicating scenario wording in test cases; they should differ in granularity.
   - Example:
    - Test Scenario: "Validate whether the user is able to login into the account"
      - Test Case: "Validate whether the user can login with valid credentials"
      - Test Case: "Validate whether the user cannot login with valid email id but invalid password"
      - Test Case: "Validate whether the user cannot login with invalid email id and valid password"
      - Test Case: "Validate whether the user cannot login with invalid email id and invalid password"
    Similarly if the functionality changes, the test scenarios and test cases should be different, instead of providing the same test scenarios and then just elaborating the test scenarios while providing the test cases.
7. Do not provide any extra guiding text or any other thing, just provide the output in the format below.
8. Generate a minimum of 20-30 unique test scenarios and 40-60 functional test cases.
9. Ensure the output is consistent for the same input (same count, wording, and structure).
10. Do not include any explanations, metadata, or commentary outside the specified format.
11. Use the following format for your response:

---
Output Format  
(Use this exact format in your response)

Story Title [Extracted from JIRA]  
JIRA Issue ID {jira_id}  

Acceptance Criteria  
{acceptance_criteria}

Test Scenarios  

TS-01: Validate whether [High-level description of the scenario].  
TS-02: Validate whether [High-level description of the scenario].  
TS-03: Validate whether [High-level description of the scenario].  
...continue listing all test scenarios...


Generate test cases for the following user story and acceptance criteria.
Return the output as a JSON array, where each test case has the following keys:

Heres the required output format in json:

  
    Test Case ID: TC_01,
    Description: Validate search with valid origin and destination returns flights.,
    Preconditions: User is on the flight search page.,
    Test Data: Origin: JFK, Destination: LAX, Departure Date: Tomorrow,
    Test Execution Steps: 1. Enter origin. 2. Enter destination. 3. Select date. 4. Click search.,
    Expected Outcome: List of available flights is displayed.,
    Pass/Fail Criteria: Pass if flights are displayed; Fail if error shown or empty list.,
    Priority: High,
    References: {jira_id}

---
Now generate test scenarios and test cases for the following user story

User Story  
{user_story}  

JIRA Issue ID {jira_id}  

Expected Acceptance Criteria  
{acceptance_criteria}
"""
)
