"""
Project Manager - Main orchestrator for the software engineering squad.
Handles project creation, agent coordination, and workflow management.
"""
from pathlib import Path

from strands import Agent
from strands.models import BedrockModel
from strands_tools import file_read, file_write

from constants import MODEL_PROJECT_MANAGER
from context_manager import get_lean_project_context
from project_utils import create_project_folder, list_projects
from tools.business_analyst import business_analyst_tool
from tools.code_reviewer import code_reviewer_tool
from tools.developer import developer_tool
from tools.software_architect import software_architect_tool
from tools.ui_designer import ui_designer_tool
from tools.ui_tester import ui_tester_tool

bedrock_model = BedrockModel(
    model_id=MODEL_PROJECT_MANAGER,
    temperature=0.2,
    top_p=0.8
)


def load_project_manager_prompt() -> str:
    """Load the project manager system prompt."""
    script_dir = Path(__file__).parent
    context_file = script_dir / "context" / "project_manager.md"
    with open(context_file, "r", encoding="utf-8") as f:
        return f.read()


def create_project_aware_agent(project_path: str, base_prompt: str) -> Agent:
    """
    Create an agent with project context.

    Args:
        project_path (str): Path to the current project folder
        base_prompt (str): Base system prompt for the project manager

    Returns:
        Agent: Configured agent with project context
    """
    project_context = get_lean_project_context(project_path)

    enhanced_prompt = base_prompt + project_context

    tools = [
        file_read, file_write,
        business_analyst_tool,
        software_architect_tool,
        ui_designer_tool,
        developer_tool,
        ui_tester_tool,
        code_reviewer_tool
    ]

    return Agent(model=bedrock_model, system_prompt=enhanced_prompt, tools=tools)


def handle_user_request(user_input: str) -> None:
    """
    Handle a user request by creating a project and processing it.

    Args:
        user_input (str): User's project request
    """
    # Load the project manager prompt
    base_prompt = load_project_manager_prompt()
    print("\n🏗️  Creating new project...")
    try:
        project_path = create_project_folder(user_input)
        project_folder = Path(project_path).name

        print(f"✅ Project created: {project_folder}")
        print(f"📁 Location: {project_path}")

        # Create project-aware agent
        agent = create_project_aware_agent(project_path, base_prompt)

        # Send the input to the agent
        print("\n🤖 Project Manager thinking...\n")
        agent(user_input)

    except Exception as e:
        print(f"❌ Error creating project: {e}")


def show_projects_list() -> None:
    """Display the list of existing projects."""
    projects = list_projects()
    if projects:
        print("\n📂 Existing Projects:")
        print("-" * 50)
        for i, proj in enumerate(projects[:10], 1):  # Show last 10 projects
            print(f"  {i}. {proj['folder']} - {proj['title']}")
    else:
        print("\n📂 No projects found.")


def select_project() -> str:
    """
    Let user select a project and return the project path.

    Returns:
        str: Path to selected project, or empty string if cancelled
    """
    projects = list_projects()
    if not projects:
        print("❌ No existing projects found.")
        return ""

    # Show projects with numbers
    print("\n📂 Select a project:")
    print("-" * 50)
    for i, proj in enumerate(projects[:10], 1):
        print(f"  {i}. {proj['folder']} - {proj['title']}")

    # Get user selection
    try:
        selection = input(
            "\n🔢 Enter project number (or 'back' to cancel): ").strip()
        if selection.lower() == 'back':
            return ""

        project_idx = int(selection) - 1
        if 0 <= project_idx < len(projects):
            selected_project = projects[project_idx]
            print(f"\n📁 Selected project: {selected_project['title']}")
            print(f"📂 Location: {selected_project['path']}")
            return selected_project['path']
        else:
            print("❌ Invalid project number.")
            return ""

    except ValueError:
        print("❌ Please enter a valid number.")
        return ""
    except Exception as e:
        print(f"❌ Error selecting project: {e}")
        return ""


def continue_project(project_path: str, user_input: str) -> None:
    """
    Continue working on an existing project.

    Args:
        project_path (str): Path to the project folder
        user_input (str): User's additional request for the project
    """
    try:
        # Load the project manager prompt
        base_prompt = load_project_manager_prompt()

        # Create project-aware agent for existing project
        agent = create_project_aware_agent(project_path, base_prompt)

        # Send the input to the agent
        print("\n🤖 Project Manager thinking...\n")
        agent(user_input)

    except Exception as e:
        print(f"❌ Error continuing project: {e}")
