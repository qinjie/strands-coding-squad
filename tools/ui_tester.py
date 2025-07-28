"""
Implement a tool which provides the functions of a UI tester, i.e. performing comprehensive web UI testing using Playwright.
"""
import os
from pathlib import Path
from typing import Optional
from strands.models import BedrockModel
from strands import Agent, tool
from constants import MODEL_UI_TESTER
from strands_tools import file_read, file_write
from project_utils import update_agent_staging_readme, update_project_readme_with_agent_work
from context_manager import get_condensed_context

# Define the tools we need
tools = [file_read, file_write]

os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Script directory for relative paths
script_dir = Path(__file__).parent


def ui_tester_work(input_text: str, complexity_level: str = "SIMPLE") -> str:
    """
    UI tester work function that processes input text and returns the agent's response.

    Args:
        input_text (str): The input text containing testing requirements or specifications
        complexity_level (str): Project complexity level (SIMPLE, MODERATE, COMPLEX)

    Returns:
        str: The agent's response including test results and recommendations
    """
    try:
        bedrock_model = BedrockModel(
            model_id=MODEL_UI_TESTER,
            temperature=0.2,
            top_p=0.8
        )
        # Get context based on complexity level
        system_prompt = get_condensed_context("ui_tester", complexity_level)

        # Create agent with appropriate context
        agent = Agent(model=bedrock_model,
                      system_prompt=system_prompt, tools=tools)

        response = agent(input_text)
        return response
    except ValueError as e:
        return f"Input value error in UI tester tool: {str(e)}"
    except RuntimeError as e:
        return f"Runtime error in UI tester tool: {str(e)}"
    except ImportError as e:
        return f"Import error in UI tester tool: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred in UI tester tool: {str(e)}"


@tool
def ui_tester_tool(
    testing_requirements: str,
    project_path: str,
    complexity_level: Optional[str] = None,
    application_urls: Optional[str] = None,
    test_scenarios: Optional[str] = None,
    browser_requirements: Optional[str] = None,
    performance_benchmarks: Optional[str] = None,
    accessibility_standards: Optional[str] = None,
    test_data: Optional[str] = None
) -> str:
    """
    UI tester tool that performs comprehensive web UI testing using Playwright.

    Creates test files in the staging/ui_tester/ folder and returns a JSON response
    listing the generated files and their contents.

    This tool provides the functionality of a UI tester agent that can:
    - Create and execute automated UI tests using Playwright
    - Perform functional, usability, and regression testing
    - Test responsive design and cross-browser compatibility
    - Validate accessibility and performance requirements
    - Generate comprehensive test reports and bug documentation

    Args:
        testing_requirements (str): Testing requirements and specifications
        project_path (str): Path to the project folder (to access staging area)
        complexity_level (Optional[str]): Project complexity level (SIMPLE/MODERATE/COMPLEX)
        application_urls (Optional[str]): Application URLs and testing environments
        test_scenarios (Optional[str]): Test scenarios and user acceptance criteria
        browser_requirements (Optional[str]): Browser and device compatibility requirements
        performance_benchmarks (Optional[str]): Performance benchmarks and standards
        accessibility_standards (Optional[str]): Accessibility standards and compliance requirements
        test_data (Optional[str]): Test data and regression testing requirements

    Returns:
        str: JSON response with list of generated files and their descriptions
    """
    # Construct structured input for the agent
    input_text = f"""
UI TESTING REQUEST:

Project Path: {project_path}
Primary Output: {project_path}/src/tests/, {project_path}/docs/, {project_path}/assets/data/
Staging Folder: {project_path}/staging/ui_tester/

Testing Requirements: {testing_requirements}

{f'Project Complexity Level: {complexity_level}' if complexity_level else ''}
{f'Application URLs: {application_urls}' if application_urls else ''}
{f'Test Scenarios: {test_scenarios}' if test_scenarios else ''}
{f'Browser Requirements: {browser_requirements}' if browser_requirements else ''}
{f'Performance Benchmarks: {performance_benchmarks}' if performance_benchmarks else ''}
{f'Accessibility Standards: {accessibility_standards}' if accessibility_standards else ''}
{f'Test Data: {test_data}' if test_data else ''}

INSTRUCTIONS:
1. Create test files in src/tests/, documentation in docs/, and test data in assets/data/
2. Also create copies in staging/ui_tester/ folder for traceability
3. Generate whatever files you think are necessary (test scripts, reports, documentation, etc.)
4. Each file should contain well-structured, executable test code and documentation
5. Return a JSON response with the primary file locations (not staging paths) using the following format:

{{
  "status": "completed",
  "summary": "Brief summary of the testing work completed",
  "generated_files": [
    {{
      "file_path": "src/tests/filename.py",
      "file_name": "filename.py", 
      "content_description": "Description of what this file contains",
      "key_insights": ["List", "of", "key", "testing", "insights"]
    }}
  ],
  "recommendations": ["Key", "testing", "recommendations"]
}}

Expected deliverables:
- Automated test scripts (Playwright/Selenium) (src/tests/)
- Test execution reports with pass/fail status (docs/)
- Bug reports with detailed reproduction steps (docs/)
- Performance testing results and metrics (docs/)
- Accessibility compliance audit reports (docs/)
- Cross-browser compatibility test results (docs/)
- Screenshots and videos of test executions (assets/data/)
- Recommendations for test automation improvements (docs/)
"""

    # Use provided complexity level or default to SIMPLE
    comp_level = complexity_level if complexity_level else "SIMPLE"
    result = ui_tester_work(input_text.strip(), comp_level)

    # Update staging README with generated file information
    update_agent_staging_readme(project_path, "ui_tester", result)

    # Update main project README with agent work progress
    update_project_readme_with_agent_work(project_path, "ui_tester", result)

    return result


if __name__ == "__main__":
    # Simple test for the UI tester tool
    test_input = """
    Create comprehensive UI tests for a restaurant ordering web application:
    
    Test Scenarios:
    1. Homepage Loading and Navigation
       - Verify page loads within 3 seconds
       - Check all navigation links work correctly
       - Validate responsive design on mobile/tablet/desktop
    
    2. Menu Browsing and Item Selection
       - Test category filtering (appetizers, mains, etc.)
       - Verify item details display correctly
       - Test add to cart functionality
       - Validate quantity adjustment controls
    
    3. Checkout Process
       - Test form validation (required fields, email format)
       - Verify delivery/pickup option selection
       - Test payment form integration
       - Validate order confirmation display
    
    4. Order Tracking
       - Test order status updates
       - Verify real-time status changes
       - Check order history accessibility
    
    Requirements:
    - Use Playwright for cross-browser testing (Chrome, Firefox, Safari)
    - Include accessibility tests (WCAG compliance)
    - Test performance (page load times, image optimization)
    - Generate detailed test reports with screenshots
    """

    print("Testing UI Tester Tool")
    print("=" * 50)
    print(f"Input: {test_input.strip()}")
    print("\nOutput:")
    print("-" * 30)

    try:
        result = ui_tester_tool(
            testing_requirements=test_input,
            project_path=script_dir.parent / "tmp"
        )
        print(result)
    except Exception as e:
        print(f"Error during testing: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
