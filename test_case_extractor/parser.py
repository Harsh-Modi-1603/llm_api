import re
import json
from typing import List, Dict


def extract_test_scenarios(text: str) -> List[Dict]:
    scenario_pattern = re.compile(
        r'(TS-\d+):\s*(.*?)\n', re.DOTALL
    )

    matches = scenario_pattern.findall(text)
    scenarios = []

    for scenario_id, scenario_title in matches:
        scenarios.append({
            "Test Scenario ID": scenario_id.strip(),
            "Scenario": scenario_title.strip()
        })

    return scenarios


def extract_test_cases(text: str) -> List[Dict]:
    test_case_pattern = re.compile(
        r'(TC-\d+):?\s*(.*?)\s*- Preconditions:(.*?)'
        r'- Test Data:(.*?)'
        r'- Test Execution Steps:(.*?)- Expected Outcome:(.*?)'
        r'- Pass/Fail Criteria:(.*?)'
        r'- Priority:(.*?)'
        r'- References:(.*?)(?=\nTC-\d+:|\Z)',
        re.DOTALL
    )

    matches = test_case_pattern.findall(text)
    test_cases = []

    for match in matches:
        (
            test_case_id, title, preconditions, test_data,
            steps, expected_outcome, pass_fail_criteria,
            priority, references
        ) = [m.strip() for m in match]

        test_case = {
            "Test Case ID": test_case_id,
            "Title": title,
            "Preconditions": preconditions,
            "Test Data": test_data,
            "Test Execution Steps": [
                step.strip() for step in steps.strip().split("\n") if step.strip()
            ],
            "Expected Outcome": expected_outcome,
            "Pass Criteria": extract_pass_fail(pass_fail_criteria, "pass"),
            "Fail Criteria": extract_pass_fail(pass_fail_criteria, "fail"),
            "Priority": priority,
            "References": references
        }

        test_cases.append(test_case)

    return test_cases


def extract_pass_fail(text: str, label: str) -> str:
    pattern = re.compile(rf'{label}:\s*(.*?)(?:\n|$)', re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


# For local testing
if __name__ == "__main__":
    with open("llm_output.txt", "r", encoding="utf-8") as file:
        content = file.read()

    try:
        parsed = {
            "testScenarios": extract_test_scenarios(content),
            "testCases": extract_test_cases(content)
        }
        with open("parsed_output.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
        print("✅ Parsed output saved to parsed_output.json")
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
