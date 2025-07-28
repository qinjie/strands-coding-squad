"""
Implement a tool which provides the functions of a software architect, i.e. designing system architecture and technical blueprints.
"""
import os
from pathlib import Path
from typing import Optional
from strands.models import BedrockModel
from strands import Agent, tool
from strands_tools import file_read, file_write
from constants import MODEL_SOFTWARE_ARCHITECT
from project_utils import update_agent_staging_readme, update_project_readme_with_agent_work
from context_manager import get_condensed_context

# Define the tools we need
tools = [file_read, file_write]

os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Script directory for relative paths
script_dir = Path(__file__).parent


def software_architect_work(input_text: str, complexity_level: str = "SIMPLE") -> str:
    """
    Software architect work function that processes input text and returns the agent's response.

    Args:
        input_text (str): The input text containing architectural requirements or specifications
        complexity_level (str): Project complexity level (SIMPLE, MODERATE, COMPLEX)

    Returns:
        str: The agent's response including architectural designs and recommendations
    """
    try:

        # Agent will be created dynamically based on complexity level
        bedrock_model = BedrockModel(
            model_id=MODEL_SOFTWARE_ARCHITECT,
            temperature=0.2,
            top_p=0.8
        )

        # Get context based on complexity level
        system_prompt = get_condensed_context(
            "software_architect", complexity_level)

        # Create agent with appropriate context
        agent = Agent(model=bedrock_model,
                      system_prompt=system_prompt, tools=tools)

        response = agent(input_text)
        return response
    except ValueError as e:
        return f"Input value error in software architect tool: {str(e)}"
    except RuntimeError as e:
        return f"Runtime error in software architect tool: {str(e)}"
    except ImportError as e:
        return f"Import error in software architect tool: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred in software architect tool: {str(e)}"


@tool
def software_architect_tool(
    requirements: str,
    project_path: str,
    complexity_level: Optional[str] = None,
    performance_requirements: Optional[str] = None,
    security_requirements: Optional[str] = None,
    integration_requirements: Optional[str] = None,
    technology_constraints: Optional[str] = None,
    scalability_requirements: Optional[str] = None,
    compliance_requirements: Optional[str] = None,
    existing_systems: Optional[str] = None
) -> str:
    """
    Software architect tool that designs system architecture and technical blueprints.

    Creates markdown files in the staging/software_architect/ folder and returns a JSON response
    listing the generated files and their contents.

    This tool provides the functionality of a software architect agent that can:
    - Design system architecture and component interactions
    - Make technology stack decisions and recommendations
    - Create technical blueprints and design patterns
    - Define integration patterns and data flow
    - Establish architectural constraints and guidelines

    Args:
        requirements (str): Business requirements and functional specifications
        project_path (str): Path to the project folder (to access staging area)
        complexity_level (Optional[str]): Project complexity level (SIMPLE/MODERATE/COMPLEX)
        performance_requirements (Optional[str]): Performance and scalability requirements
        security_requirements (Optional[str]): Security and compliance requirements
        integration_requirements (Optional[str]): Integration requirements with external systems
        technology_constraints (Optional[str]): Technology constraints and preferences
        scalability_requirements (Optional[str]): Scalability and load requirements
        compliance_requirements (Optional[str]): Compliance and regulatory requirements
        existing_systems (Optional[str]): Existing systems and legacy considerations

    Returns:
        str: JSON response with list of generated files and their descriptions
    """
    # Construct structured input for the agent
    input_text = f"""
SYSTEM ARCHITECTURE REQUEST:

Project Path: {project_path}
Primary Output: {project_path}/docs/architecture/ and {project_path}/docs/api/
Staging Folder: {project_path}/staging/software_architect/

Business Requirements: {requirements}

{f'Project Complexity Level: {complexity_level}' if complexity_level else ''}
{f'Performance Requirements: {performance_requirements}' if performance_requirements else ''}
{f'Security Requirements: {security_requirements}' if security_requirements else ''}
{f'Integration Requirements: {integration_requirements}' if integration_requirements else ''}
{f'Technology Constraints: {technology_constraints}' if technology_constraints else ''}
{f'Scalability Requirements: {scalability_requirements}' if scalability_requirements else ''}
{f'Compliance Requirements: {compliance_requirements}' if compliance_requirements else ''}
{f'Existing Systems: {existing_systems}' if existing_systems else ''}

INSTRUCTIONS:
1. Create architecture documentation files in docs/architecture/ and API documentation in docs/api/
2. Also create copies in staging/software_architect/ folder for traceability
3. Generate whatever files you think are necessary (e.g., system_architecture.md, technology_stack.md, api_design.md, etc.)
4. Each file should contain detailed, well-structured content
5. Return a JSON response with the primary file locations (not staging paths) using the following format:

{{
  "status": "completed",
  "summary": "Brief summary of the architecture design completed",
  "generated_files": [
    {{
      "file_path": "docs/architecture/filename.md",
      "file_name": "filename.md", 
      "content_description": "Description of what this file contains",
      "key_insights": ["List", "of", "key", "architectural", "decisions"]
    }}
  ],
  "recommendations": ["Key", "technical", "recommendations"]
}}

Expected deliverables:
- System architecture diagrams and documentation (docs/architecture/)
- Technology stack recommendations with justifications (docs/architecture/)
- API design specifications and data models (docs/api/)
- Database schema and data flow diagrams (docs/architecture/)
- Security architecture and authentication patterns (docs/architecture/)
- Deployment architecture and infrastructure requirements (docs/architecture/)
- Integration patterns and communication protocols (docs/architecture/)
- Performance optimization strategies (docs/architecture/)
"""

    # Use provided complexity level or default to SIMPLE
    comp_level = complexity_level if complexity_level else "SIMPLE"
    result = software_architect_work(input_text.strip(), comp_level)

    # Update staging README with generated file information
    update_agent_staging_readme(project_path, "software_architect", result)

    # Update main project README with agent work progress
    update_project_readme_with_agent_work(
        project_path, "software_architect", result)

    return result


if __name__ == "__main__":
    # Simple test for the software architect tool
    test_input = """
    Design the system architecture for a restaurant ordering web application with these requirements:
    - Customer portal: menu browsing, ordering, payment, order tracking
    - Admin panel: menu management, order management, analytics
    - Real-time order status updates
    - Integration with payment gateway (Stripe)
    - Support for 1000+ concurrent users
    - Mobile responsive design
    - Database for menu items, orders, customers
    """

    print("Testing Software Architect Tool")
    print("=" * 50)
    print(f"Input: {test_input.strip()}")
    print("\nOutput:")
    print("-" * 30)

    try:
        result = software_architect_tool(
            requirements=test_input,
            project_path=script_dir.parent / "tmp"
        )
        print(result)
    except Exception as e:
        print(f"Error during testing: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
