"""
Implement a tool which provides the functions of a developer, i.e. writing code according to the requirements in input.
"""
import os
# Fix imports to match project structure
import os
from pathlib import Path
from typing import Optional
from strands.models import BedrockModel
from strands import Agent, tool
from strands_tools import file_read, file_write
from constants import MODEL_DEVELOPER
from project_utils import update_agent_staging_readme, update_project_readme_with_agent_work
from context_manager import get_condensed_context

# Define the tools we need
tools = [file_read, file_write]


os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Script directory for relative paths
script_dir = Path(__file__).parent


def developer_work(input_text: str, complexity_level: str = "SIMPLE") -> str:
    """
    Developer work function that processes input text and returns the agent's response.

    Args:
        input_text (str): The input text containing development requirements or specifications
        complexity_level (str): Project complexity level (SIMPLE, MODERATE, COMPLEX)

    Returns:
        str: The agent's response including code implementation and explanations
    """
    try:

        # Agent will be created dynamically based on complexity level
        bedrock_model = BedrockModel(
            model_id=MODEL_DEVELOPER,
            temperature=0.2,
            top_p=0.8
        )
        # Get context based on complexity level
        system_prompt = get_condensed_context("developer", complexity_level)

        # Create agent with appropriate context
        agent = Agent(model=bedrock_model,
                      system_prompt=system_prompt, tools=tools)

        response = agent(input_text)
        return response
    except ValueError as e:
        return f"Input value error in developer tool: {str(e)}"
    except RuntimeError as e:
        return f"Runtime error in developer tool: {str(e)}"
    except ImportError as e:
        return f"Import error in developer tool: {str(e)}"
    except Exception as e:  # Fallback for unexpected errors
        return f"An unexpected error occurred in developer tool: {str(e)}"


@tool
def developer_tool(
    technical_specifications: str,
    project_path: str,
    complexity_level: Optional[str] = None,
    architecture_guidelines: Optional[str] = None,
    coding_requirements: Optional[str] = None,
    technology_stack: Optional[str] = None,
    file_structure: Optional[str] = None,
    performance_requirements: Optional[str] = None,
    testing_requirements: Optional[str] = None,
    security_requirements: Optional[str] = None
) -> str:
    """
    Developer tool that writes code based on input requirements.

    Creates code files in src/app/, src/tests/, src/config/, and docs/ folders 
    (with copies in staging/developer/ for traceability) and returns a JSON response
    listing the generated files and their contents.

    This tool provides the functionality of a software developer agent that can:
    - Write Python scripts and functions
    - Implement algorithms and data structures
    - Create code following best practices and design patterns
    - Handle debugging and code optimization
    - Generate comprehensive unit tests

    Args:
        technical_specifications (str): Technical specifications and functional requirements
        project_path (str): Path to the project folder (to access staging area)
        complexity_level (Optional[str]): Project complexity level (SIMPLE/MODERATE/COMPLEX)
        architecture_guidelines (Optional[str]): System architecture and design patterns to follow
        coding_requirements (Optional[str]): Specific coding tasks and implementation details
        technology_stack (Optional[str]): Technology stack and framework preferences
        file_structure (Optional[str]): File paths and project structure guidelines
        performance_requirements (Optional[str]): Performance and optimization requirements
        testing_requirements (Optional[str]): Testing requirements and coverage expectations
        security_requirements (Optional[str]): Security requirements and best practices

    Returns:
        str: JSON response with list of generated files and their descriptions
    """
    # Construct structured input for the agent
    input_text = f"""
DEVELOPMENT REQUEST:

Project Path: {project_path}
Source Code Location: {project_path}/src/app/
Tests Location: {project_path}/src/tests/
Config Location: {project_path}/src/config/
Documentation Location: {project_path}/docs/
Staging Folder: {project_path}/staging/developer/

Technical Specifications: {technical_specifications}

{f'Project Complexity Level: {complexity_level}' if complexity_level else ''}
{f'Architecture Guidelines: {architecture_guidelines}' if architecture_guidelines else ''}
{f'Coding Requirements: {coding_requirements}' if coding_requirements else ''}
{f'Technology Stack: {technology_stack}' if technology_stack else ''}
{f'File Structure: {file_structure}' if file_structure else ''}
{f'Performance Requirements: {performance_requirements}' if performance_requirements else ''}
{f'Testing Requirements: {testing_requirements}' if testing_requirements else ''}
{f'Security Requirements: {security_requirements}' if security_requirements else ''}

INSTRUCTIONS:
1. Create source code files in src/app/ folder
2. Create test files in src/tests/ folder 
3. Create configuration files in src/config/ folder
4. Create documentation files in docs/ folder
5. Also create copies in staging/developer/ for traceability
6. Return a JSON response with the primary file locations (not staging paths)

{{
  "status": "completed",
  "summary": "Brief summary of the development work completed",
  "generated_files": [
    {{
      "file_path": "src/app/filename.py",
      "file_name": "filename.py", 
      "content_description": "Description of what this file contains",
      "key_insights": ["List", "of", "key", "implementation", "decisions"]
    }}
  ],
  "recommendations": ["Key", "development", "recommendations"],
  "downstream_inputs": {{
    "code_reviewer": {{
      "code_review_request": "Code review request and requirements",
      "source_code_files": "Source code files and implementations to review",
      "test_coverage_requirements": "Test coverage requirements and quality metrics"
    }},
    "ui_tester": {{
      "application_urls": "Application URLs and testing environments",
      "test_data": "Test data and regression testing requirements"
    }}
  }}
}}

Expected deliverables:
- src/app/ - Complete application source code
- src/config/ - Configuration files and environment templates  
- src/tests/ - Unit tests, integration tests, and test coverage reports
- docs/README.md - Setup, installation, and deployment instructions
- docs/dependencies.md - Dependency specifications and package management files
- docs/api/api_documentation.md - API documentation and technical specifications
- docs/implementation_notes.md - Implementation decisions and technical rationale
- docs/performance_guide.md - Performance optimization recommendations
- docs/security_implementation.md - Security implementation and best practices
- docs/development_guide.md - Development setup and contribution guidelines
- staging/developer/ - Working copies of all files for traceability
"""

    # Use provided complexity level or default to SIMPLE
    comp_level = complexity_level if complexity_level else "SIMPLE"
    result = developer_work(input_text.strip(), comp_level)

    # Update staging README with generated file information
    update_agent_staging_readme(project_path, "developer", result)

    # Update main project README with agent work progress
    update_project_readme_with_agent_work(project_path, "developer", result)

    return result


if __name__ == "__main__":
    # Simple test for the developer tool
    test_input = """
    Implement a Python class for managing restaurant menu items with the following requirements:
    
    Features:
    1. MenuItem class with properties: name, description, price, category, available
    2. MenuManager class that can:
       - Add/remove menu items
       - Get items by category
       - Search items by name
       - Calculate total for a list of items
       - Toggle item availability
    
    Requirements:
    - Use proper data validation (price > 0, non-empty names)
    - Include error handling for invalid operations
    - Add comprehensive docstrings
    - Follow PEP 8 style guidelines
    - Include basic unit tests to verify functionality
    
    Categories: appetizer, main_course, dessert, beverage
    
    Example usage:
    ```python
    manager = MenuManager()
    manager.add_item("Caesar Salad", "Fresh romaine with parmesan", 12.99, "appetizer")
    items = manager.get_items_by_category("appetizer")
    total = manager.calculate_total(["Caesar Salad", "Grilled Chicken"])
    ```
    """

    print("Testing Developer Tool")
    print("=" * 50)
    print(f"Input: {test_input.strip()}")
    print("\nOutput:")
    print("-" * 30)

    try:
        result = developer_tool(
            technical_specifications=test_input,
            project_path=script_dir.parent / "tmp"
        )
        print(result)
    except Exception as e:
        print(f"Error during testing: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
