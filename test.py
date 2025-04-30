from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Initialize the LLM model
llm_model = ChatGoogleGenerativeAI(
    api_key=os.getenv("gemini_api_key_2"),
    model="gemma-3-27b-it",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define the prompt template
test_case_prompt = PromptTemplate(
    input_variables=["user_story", "jira_id", "acceptance_criteria"],
    template= """
Task: AI Test Case Generator

Objective  
You are an AI Test Case Generator that converts JIRA user stories into enterprise-grade **functional** test scenarios and test cases. Your output must meet the expectations of a senior QA engineer and be directly usable in QA planning and execution.

---
Instructions  
1. Analyze the user story and acceptance criteria thoroughly.
2. If acceptance criteria are not provided, derive them accurately from the story.
3. Focus **only** on **functional** aspects — do not include non-functional cases like performance, usability, security, or accessibility.
4. Clearly **separate** test scenarios from test cases:
   - Test Scenarios = High-level *what to test* (breadth of coverage)
   - Test Cases = Low-level *how to test* (step-by-step validations, conditions, and outcomes)
5. **Test Scenarios** must be framed as "validate whether..." and should address:
   - Positive flows
   - Negative flows
   - Edge cases
   - Input validation
   - UI behavior (if applicable)
   - Business logic
6. **Test Cases** must be:
   - Unique and detailed
   - Derived from each scenario
   - Comprehensive, including steps, expected outcome, and pass/fail criteria
7. **Avoid duplicating** scenario wording in test cases — they should differ in granularity.
8. Ensure the following minimums are respected:
   - **20–30 unique test scenarios**
   - **40–60 functional test cases** (at least 2–3 for each scenario, more where needed)
9. Output must **always** be consistent for the same input (same count, wording, and structure).
10. Do **not** include any explanations, metadata, or commentary outside the specified format.

---
Response Format (Strictly Follow This Structure)  

---
User Story  
Story Title [Extracted from JIRA]  
Description [Extracted from JIRA]  
JIRA Issue ID {jira_id}  

Acceptance Criteria  
{acceptance_criteria}

---
Test Scenarios & Test Cases  

TS_01: validate whether [briefly describe high-level feature or flow to verify]  
TS_02: validate whether [another high-level scenario]  
TS_03: validate whether [another high-level scenario]  
...  
[Minimum 20–30 such test scenarios — ensure variety and full functional coverage]

TC_01: validate whether [detailed step-by-step verification related to a specific scenario]  
- Preconditions: [What must be set up before this test]  
- Test Data: [Guidance: “The test data is just for guidance. Actual test data should be determined by the tester.”]  
- Test Execution Steps:  
  1. Step 1  
  2. Step 2  
  3. Step 3  
  ... (As many detailed steps as needed)  
- Expected Outcome: [Expected result of the test]  
- Pass/Fail Criteria:  
  - Pass: [Define pass conditions]  
  - Fail: [Define fail conditions]  
- Priority: [High | Medium | Low]  
- References: {jira_id}

[Minimum 40–60 test cases — provide 2–4 per scenario based on necessity. Ensure no test case is a simple rephrasing of a scenario.]

---
Now generate test scenarios and test cases for the following user story:

User Story  
{user_story}  

JIRA Issue ID {jira_id}  

Expected Acceptance Criteria  
{acceptance_criteria}  

---
Response Format Requirements  
1. First list **all** test scenarios together. Then list **all** test cases together. Do not mix.  
2. Test scenarios must be abstract and high-level. Test cases must be detailed and concrete.  
3. Do not include any non-functional test cases.  
4. Ensure coverage is deep and wide. Missing edge or alternate cases is not acceptable.  
5. Maintain consistency in tone and structure — response should be usable in real QA documentation.  
6. Minimum 20 test scenarios and 40 test cases. More if story complexity demands.

Now generate the response.

""",

)

def get_multiline_input(prompt):
    """Get multiline input from the user."""
    print(prompt)
    print("Enter your text (type 'DONE' on a new line when finished):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'DONE':
            break
        lines.append(line)
    return '\n'.join(lines)

def main():
    print("=== Test Case Generator ===")
    
    # Get multiline user story input
    user_story = get_multiline_input("Enter the user story:")
    
    # Get JIRA ID
    jira_id = input("Enter the JIRA ID: ")
    
    # Get acceptance criteria (optional)
    print("Enter the acceptance criteria (type 'DONE' on a new line when finished, or just type 'DONE' immediately if none):")
    acceptance_criteria_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'DONE':
            break
        acceptance_criteria_lines.append(line)
    
    acceptance_criteria = '\n'.join(acceptance_criteria_lines)
    if not acceptance_criteria.strip():
        acceptance_criteria = "To be derived from the user story"
    
    # Format the prompt
    formatted_prompt = test_case_prompt.format(
        user_story=user_story,
        jira_id=jira_id,
        acceptance_criteria=acceptance_criteria
    )
    
    # Run the LLM
    print("\nGenerating test cases... (this may take a few moments)")
    try:
        response = llm_model.invoke(formatted_prompt)
        
        # Display the response
        print("\n=== Generated Test Cases ===\n")
        print(response.content)
    except Exception as e:
        print(f"Error generating test cases: {e}")

if __name__ == "__main__":
    main()