"""
Implement a tool which provides the functions of a UI designer, i.e. creating user interface designs and user experience optimization.
"""
import os
from pathlib import Path
from typing import Optional
from strands.models import BedrockModel
from strands import Agent, tool
from strands_tools import file_read, file_write
from constants import MODEL_UI_DESIGNER
from project_utils import update_agent_staging_readme, update_project_readme_with_agent_work
from context_manager import get_condensed_context

# Define the tools we need
tools = [file_read, file_write]

os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Script directory for relative paths
script_dir = Path(__file__).parent


def ui_designer_work(input_text: str, complexity_level: str = "SIMPLE") -> str:
    """
    UI designer work function that processes input text and returns the agent's response.

    Args:
        input_text (str): The input text containing UI/UX requirements or specifications
        complexity_level (str): Project complexity level (SIMPLE, MODERATE, COMPLEX)

    Returns:
        str: The agent's response including design recommendations and UI specifications
    """
    try:
        # Get context based on complexity level
        system_prompt = get_condensed_context("ui_designer", complexity_level)

        # Agent will be created dynamically based on complexity level

        bedrock_model = BedrockModel(
            model_id=MODEL_UI_DESIGNER,
            temperature=0.2,
            top_p=0.8
        )
        # Create agent with appropriate context
        agent = Agent(model=bedrock_model,
                      system_prompt=system_prompt, tools=tools)

        response = agent(input_text)
        return response
    except ValueError as e:
        return f"Input value error in UI designer tool: {str(e)}"
    except RuntimeError as e:
        return f"Runtime error in UI designer tool: {str(e)}"
    except ImportError as e:
        return f"Import error in UI designer tool: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred in UI designer tool: {str(e)}"


@tool
def ui_designer_tool(
    user_requirements: str,
    project_path: str,
    complexity_level: Optional[str] = None,
    user_personas: Optional[str] = None,
    brand_guidelines: Optional[str] = None,
    platform_requirements: Optional[str] = None,
    accessibility_requirements: Optional[str] = None,
    content_structure: Optional[str] = None,
    design_constraints: Optional[str] = None
) -> str:
    """
    UI designer tool that creates user interface designs and optimizes user experience.

    Creates markdown files in the staging/ui_designer/ folder and returns a JSON response
    listing the generated files and their contents.

    This tool provides the functionality of a UI designer agent that can:
    - Create wireframes, mockups, and visual designs
    - Design user flows and interaction patterns
    - Optimize user experience and accessibility
    - Establish design systems and style guides
    - Create responsive and mobile-friendly designs

    Args:
        user_requirements (str): User stories and functional requirements
        project_path (str): Path to the project folder (to access staging area)
        complexity_level (Optional[str]): Project complexity level (SIMPLE/MODERATE/COMPLEX)
        user_personas (Optional[str]): Target audience and user personas
        brand_guidelines (Optional[str]): Brand guidelines and visual identity
        platform_requirements (Optional[str]): Platform requirements (web, mobile, desktop)
        accessibility_requirements (Optional[str]): Accessibility requirements and standards
        content_structure (Optional[str]): Content structure and information architecture
        design_constraints (Optional[str]): Design constraints and limitations

    Returns:
        str: JSON response with list of generated files and their descriptions
    """
    # Construct structured input for the agent
    input_text = f"""
UI/UX DESIGN REQUEST:

Project Path: {project_path}
Primary Output: {project_path}/assets/designs/
Staging Folder: {project_path}/staging/ui_designer/

User Requirements: {user_requirements}

{f'Project Complexity Level: {complexity_level}' if complexity_level else ''}
{f'User Personas: {user_personas}' if user_personas else ''}
{f'Brand Guidelines: {brand_guidelines}' if brand_guidelines else ''}
{f'Platform Requirements: {platform_requirements}' if platform_requirements else ''}
{f'Accessibility Requirements: {accessibility_requirements}' if accessibility_requirements else ''}
{f'Content Structure: {content_structure}' if content_structure else ''}
{f'Design Constraints: {design_constraints}' if design_constraints else ''}

INSTRUCTIONS:
1. Create design files in assets/designs/ folder
2. Also create copies in staging/ui_designer/ folder for traceability
3. Generate whatever files you think are necessary (e.g., wireframes.md, design_system.md, etc.)
4. Each file should contain detailed, well-structured content
5. Return a JSON response with the primary file locations (not staging paths) using the following format:

{{
  "status": "completed",
  "summary": "Brief summary of the UI/UX design work completed",
  "generated_files": [
    {{
      "file_path": "assets/designs/filename.md",
      "file_name": "filename.md", 
      "content_description": "Description of what this file contains",
      "key_insights": ["List", "of", "key", "design", "decisions"]
    }}
  ],
  "recommendations": ["Key", "design", "recommendations"]
}}

Expected deliverables:
- Wireframes and user flow diagrams (assets/designs/)
- High-fidelity mockups and prototypes (assets/designs/)
- Design system and style guide (assets/designs/)
- Component library and UI patterns (assets/designs/)
- Responsive design specifications (assets/designs/)
- Accessibility guidelines and compliance checklist (assets/designs/)
- Interaction design and micro-animations (assets/designs/)
- User testing recommendations (assets/designs/)
"""

    # Use provided complexity level or default to SIMPLE
    comp_level = complexity_level if complexity_level else "SIMPLE"
    result = ui_designer_work(input_text.strip(), comp_level)

    # Update staging README with generated file information
    update_agent_staging_readme(project_path, "ui_designer", result)

    # Update main project README with agent work progress
    update_project_readme_with_agent_work(project_path, "ui_designer", result)

    return result


if __name__ == "__main__":
    # Simple test for the UI designer tool
    test_input = """
    Design the user interface for a restaurant ordering web application:
    
    Customer Features:
    - Homepage with restaurant branding and featured items
    - Menu browsing with categories (appetizers, mains, desserts, drinks)
    - Item details with photos, descriptions, and customization options
    - Shopping cart with quantity adjustments
    - Checkout process with delivery/pickup options
    - Order tracking page with real-time status
    - User account for order history and preferences
    
    Design Requirements:
    - Mobile-first responsive design
    - Accessible for users with disabilities
    - Modern, clean aesthetic that reflects food quality
    - Fast loading and intuitive navigation
    - Visual hierarchy to guide user actions
    """

    print("Testing UI Designer Tool")
    print("=" * 50)
    print(f"Input: {test_input.strip()}")
    print("\nOutput:")
    print("-" * 30)

    try:
        result = ui_designer_tool(
            user_requirements=test_input,
            project_path=script_dir.parent / "tmp"
        )
        print(result)
    except Exception as e:
        print(f"Error during testing: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
