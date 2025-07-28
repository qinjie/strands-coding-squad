"""
Implement a tool which provides the functions of a code reviewer, i.e. reviewing code quality, security, performance, and best practices.
"""
import os
from pathlib import Path
from typing import Optional
from strands.models import BedrockModel
from strands import Agent, tool
from strands_tools import file_read, file_write
from constants import MODEL_CODE_REVIEWER
from project_utils import update_agent_staging_readme, update_project_readme_with_agent_work
from context_manager import get_condensed_context

# Define the tools we need
tools = [file_read, file_write]

os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Script directory for relative paths
script_dir = Path(__file__).parent


def code_reviewer_work(input_text: str, complexity_level: str = "SIMPLE") -> str:
    """
    Code reviewer work function that processes input text and returns the agent's response.

    Args:
        input_text (str): The input text containing code to review or review specifications
        complexity_level (str): Project complexity level (SIMPLE, MODERATE, COMPLEX)

    Returns:
        str: The agent's response including code review feedback and recommendations
    """
    try:

        # Agent will be created dynamically based on complexity level
        bedrock_model = BedrockModel(
            model_id=MODEL_CODE_REVIEWER,
            temperature=0.2,
            top_p=0.8
        )

        # Get context based on complexity level
        system_prompt = get_condensed_context(
            "code_reviewer", complexity_level)

        # Create agent with appropriate context
        agent = Agent(model=bedrock_model,
                      system_prompt=system_prompt, tools=tools)

        response = agent(input_text)
        return response
    except ValueError as e:
        return f"Input value error in code reviewer tool: {str(e)}"
    except RuntimeError as e:
        return f"Runtime error in code reviewer tool: {str(e)}"
    except ImportError as e:
        return f"Import error in code reviewer tool: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred in code reviewer tool: {str(e)}"


@tool
def code_reviewer_tool(
    code_review_request: str,
    project_path: str,
    complexity_level: Optional[str] = None,
    source_code_files: Optional[str] = None,
    coding_standards: Optional[str] = None,
    security_requirements: Optional[str] = None,
    performance_criteria: Optional[str] = None,
    architecture_guidelines: Optional[str] = None,
    test_coverage_requirements: Optional[str] = None
) -> str:
    """
    Code reviewer tool that reviews code quality, security, performance, and best practices.

    Creates review files in the staging/code_reviewer/ folder and returns a JSON response
    listing the generated files and their contents.

    This tool provides the functionality of a code reviewer agent that can:
    - Review code quality and adherence to best practices
    - Identify security vulnerabilities and potential risks
    - Assess performance implications and optimization opportunities
    - Validate code structure, design patterns, and maintainability
    - Provide detailed feedback and improvement recommendations

    Args:
        code_review_request (str): The code review request and requirements
        project_path (str): Path to the project folder (to access staging area)
        complexity_level (Optional[str]): Project complexity level (SIMPLE/MODERATE/COMPLEX)
        source_code_files (Optional[str]): Source code files and implementations to review
        coding_standards (Optional[str]): Coding standards and style guide requirements
        security_requirements (Optional[str]): Security compliance requirements and regulations
        performance_criteria (Optional[str]): Performance requirements and optimization goals
        architecture_guidelines (Optional[str]): Architecture constraints and design patterns
        test_coverage_requirements (Optional[str]): Test coverage requirements and quality metrics

    Returns:
        str: JSON response with list of generated files and their descriptions
    """
    # Construct structured input for the agent
    input_text = f"""
CODE REVIEW REQUEST:

Project Path: {project_path}
Primary Output: {project_path}/docs/reviews/
Staging Folder: {project_path}/staging/code_reviewer/

Code Review Request: {code_review_request}

{f'Project Complexity Level: {complexity_level}' if complexity_level else ''}
{f'Source Code Files: {source_code_files}' if source_code_files else ''}
{f'Coding Standards: {coding_standards}' if coding_standards else ''}
{f'Security Requirements: {security_requirements}' if security_requirements else ''}
{f'Performance Criteria: {performance_criteria}' if performance_criteria else ''}
{f'Architecture Guidelines: {architecture_guidelines}' if architecture_guidelines else ''}
{f'Test Coverage Requirements: {test_coverage_requirements}' if test_coverage_requirements else ''}

INSTRUCTIONS:
1. Create review files in docs/reviews/ folder
2. Also create copies in staging/code_reviewer/ folder for traceability
3. Generate whatever files you think are necessary (review reports, security assessments, etc.)
4. Each file should contain detailed, well-structured review content
5. Return a JSON response with the primary file locations (not staging paths) using the following format:

{{
  "status": "completed",
  "summary": "Brief summary of the code review work completed",
  "generated_files": [
    {{
      "file_path": "docs/reviews/filename.md",
      "file_name": "filename.md", 
      "content_description": "Description of what this file contains",
      "key_insights": ["List", "of", "key", "review", "findings"]
    }}
  ],
  "recommendations": ["Key", "improvement", "recommendations"]
}}

Expected deliverables:
- Detailed code review feedback with line-by-line comments (docs/reviews/)
- Security vulnerability assessment and remediation steps (docs/reviews/)
- Performance analysis and optimization recommendations (docs/reviews/)
- Code quality metrics and technical debt assessment (docs/reviews/)
- Best practices compliance checklist (docs/reviews/)
- Refactoring suggestions and improvement priorities (docs/reviews/)
- Test coverage analysis and testing recommendations (docs/reviews/)
- Documentation quality assessment and improvements (docs/reviews/)
"""

    # Use provided complexity level or default to SIMPLE
    comp_level = complexity_level if complexity_level else "SIMPLE"
    result = code_reviewer_work(input_text.strip(), comp_level)

    # Update staging README with generated file information
    update_agent_staging_readme(project_path, "code_reviewer", result)

    # Update main project README with agent work progress
    update_project_readme_with_agent_work(
        project_path, "code_reviewer", result)

    return result


if __name__ == "__main__":
    # Simple test for the code reviewer tool
    test_request = """
    Review the Flask API code for a restaurant ordering system for security vulnerabilities,
    error handling, best practices, performance considerations, and code maintainability.
    """

    test_source_code = """
    ```python
    from flask import Flask, request, jsonify
    import sqlite3
    
    app = Flask(__name__)
    
    @app.route('/api/orders', methods=['POST'])
    def create_order():
        data = request.json
        customer_name = data['customer_name']
        items = data['items']
        total = data['total']
        
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        
        query = f"INSERT INTO orders (customer_name, items, total) VALUES ('{customer_name}', '{items}', {total})"
        cursor.execute(query)
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Order created'})
    
    @app.route('/api/orders/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")
        order = cursor.fetchone()
        
        conn.close()
        
        if order:
            return jsonify({'order': order})
        else:
            return jsonify({'error': 'Order not found'})
    
    if __name__ == '__main__':
        app.run(debug=True)
    ```
    """

    test_project_path = "/tmp/test_project"

    print("Testing Code Reviewer Tool")
    print("=" * 50)
    print(f"Request: {test_request.strip()}")
    print(f"Source Code: {test_source_code.strip()}")
    print("\nOutput:")
    print("-" * 30)

    try:
        result = code_reviewer_tool(
            code_review_request=test_request,
            project_path=test_project_path,
            source_code_files=test_source_code,
            security_requirements="OWASP security standards",
            performance_criteria="Sub-100ms API response time"
        )
        print(result)
    except Exception as e:
        print(f"Error during testing: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
