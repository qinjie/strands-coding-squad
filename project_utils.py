"""
Project management utilities for the coding squad system.
Handles project folder creation, organization, and management.
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import dotenv_values
from strands import Agent
from strands.models import BedrockModel

from constants import MODEL_MINOR_TASK

# Global variable to track current project
_current_project: Optional[str] = None


def generate_project_title_with_agent(user_request: str) -> str:
    """
    Generate a project title using an AI agent to analyze the user request.

    Args:
        user_request (str): User's project request

    Returns:
        str: Generated project title
    """
    naming_prompt = """You are a project naming assistant. Your task is to analyze user requirements and suggest a concise, descriptive project name.

Rules for project names:
1. Use only lowercase letters, numbers, and underscores
2. Keep it between 2-4 words maximum
3. Make it descriptive but concise
4. Avoid common words like 'app', 'system', 'project' unless essential
5. Focus on the core functionality or domain

Examples:
- "Create a todo list app" → "todo_list"
- "Build an e-commerce website for selling books" → "book_store"
- "Develop a chat application with real-time messaging" → "realtime_chat"
- "Create a weather dashboard with forecasts" → "weather_dashboard"

Respond with ONLY the suggested project name, no explanations or additional text."""

    try:
        bedrock_model = BedrockModel(
            model_id=MODEL_MINOR_TASK,
            temperature=0.2,
            top_p=0.8
        )

        agent = Agent(model=bedrock_model,
                      system_prompt=naming_prompt, tools=[])
        response = agent(f"Generate a project name for: {user_request}")

        # Extract and clean the response
        suggested_name = str(response).strip().lower()

        # Clean and validate the name
        suggested_name = re.sub(r'[^\w\-_]', '', suggested_name)
        suggested_name = suggested_name[:50]  # Limit length

        if suggested_name and len(suggested_name) > 0:
            return suggested_name
        else:
            return generate_fallback_title(user_request)

    except Exception:
        # Fallback to simple method if agent fails
        return generate_fallback_title(user_request)


def generate_fallback_title(user_request: str) -> str:
    """
    Generate a fallback project title using simple word extraction.

    Args:
        user_request (str): User's project request

    Returns:
        str: Generated project title
    """
    # Extract key words and create a title
    words = re.findall(r'\b[a-zA-Z]+\b', user_request.lower())

    # Filter out common words
    stop_words = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'were', 'will', 'with', 'i', 'want', 'need', 'can',
        'would', 'like', 'please', 'help', 'me', 'my', 'we', 'us', 'our'
    }

    meaningful_words = [word for word in words if word not in stop_words]

    # Take first 3-4 meaningful words or use fallback
    if meaningful_words:
        title_words = meaningful_words[:4]
        title = '_'.join(title_words)
    else:
        title = "project"

    # Clean title and ensure it's valid for folder names
    title = re.sub(r'[^\w\-_]', '', title)
    title = title[:50]  # Limit length

    return title


def create_project_folder(user_request: str, custom_title: Optional[str] = None, base_path: str = ".") -> str:
    """
    Create a new project folder with subfolders.

    Args:
        user_request (str): User's project request
        custom_title (str, optional): Custom project title
        base_path (str): Base path where projects will be created

    Returns:
        str: Path to the created project folder
    """
    global _current_project

    base_path_obj = Path(base_path)

    # Generate title
    if custom_title:
        title = re.sub(r'[^\w\-_]', '', custom_title)
    else:
        title = generate_project_title_with_agent(user_request)

    # Create folder name with date
    date_str = datetime.now().strftime("%Y%m%d")
    folder_name = f"project_{date_str}_{title}"

    # Ensure unique folder name
    counter = 1
    original_folder_name = folder_name
    while (base_path_obj / folder_name).exists():
        folder_name = f"{original_folder_name}_{counter}"
        counter += 1

    # Create project folder
    project_path = base_path_obj / folder_name
    project_path.mkdir(exist_ok=True)

    # Create subfolders
    _create_subfolders(project_path)

    # Create project info file
    _create_project_info(project_path, user_request, title)

    # Create initial project README
    create_project_readme(str(project_path))

    _current_project = str(project_path)
    return str(project_path)


def _create_subfolders(project_path: Path) -> None:
    """
    Create standard subfolders in the project.

    Args:
        project_path (Path): Path to the project folder
    """
    # Main project structure
    main_folders = [
        "src",              # Source code
        "src/app",          # Main application code
        "src/tests",        # Test files
        "src/config",       # Configuration files
        "docs",             # Documentation
        "docs/requirements",  # Business analysis documents
        "docs/architecture",  # Software architecture documents
        "docs/reviews",     # Code review documents
        "docs/api",         # API documentation
        "assets",           # Static resources
        "assets/designs",   # UI designs and wireframes
        "assets/images",    # Images and graphics
        "assets/data"       # Sample/test data
    ]

    # Worker agent staging folders (kept for traceability)
    staging_folders = [
        "staging/business_analyst",    # Business analyst working files
        "staging/software_architect",  # Software architect working files
        "staging/ui_designer",         # UI designer working files
        "staging/developer",           # Developer working files
        "staging/ui_tester",           # UI tester working files
        "staging/code_reviewer"        # Code reviewer working files
    ]

    # Create main subfolders
    for subfolder in main_folders:
        (project_path / subfolder).mkdir(parents=True, exist_ok=True)

    # Create staging folders
    for staging_folder in staging_folders:
        (project_path / staging_folder).mkdir(parents=True, exist_ok=True)

    # Create README files in key folders
    _create_folder_readmes(project_path)
    _create_staging_readmes(project_path)


def _create_folder_readmes(project_path: Path) -> None:
    """Create README files in subfolders to explain their purpose."""
    readme_content = {
        "src": "# Source Code\n\nApplication source code organized by modules and components.\n\n- `app/` - Main application code\n- `tests/` - Test files and test suites\n- `config/` - Configuration files and settings",
        "docs": "# Documentation\n\nTechnical documentation, user guides, and project specifications.\n\n- `requirements/` - Business requirements and analysis\n- `architecture/` - System architecture and design\n- `reviews/` - Code review reports and assessments\n- `api/` - API documentation and specifications",
        "assets": "# Assets\n\nStatic resources and design materials.\n\n- `designs/` - UI wireframes, mockups, and design specifications\n- `images/` - Images, icons, and graphics\n- `data/` - Sample data and test fixtures",
        "docs/requirements": "# Requirements Documentation\n\nBusiness analysis, user stories, and project requirements generated by the Business Analyst agent.",
        "docs/architecture": "# Architecture Documentation\n\nSystem architecture, technical specifications, and design decisions generated by the Software Architect agent.",
        "docs/reviews": "# Code Review Documentation\n\nCode quality assessments, security reviews, and improvement recommendations generated by the Code Reviewer agent.",
        "docs/api": "# API Documentation\n\nAPI specifications, endpoint documentation, and integration guides.",
        "assets/designs": "# Design Assets\n\nUI/UX wireframes, mockups, design systems, and visual specifications generated by the UI Designer agent.",
        "assets/images": "# Image Assets\n\nImages, icons, logos, and graphics used in the project.",
        "assets/data": "# Data Assets\n\nSample data, test fixtures, and data files used for development and testing.",
        "src/app": "# Application Code\n\nMain application source code organized by features and modules.",
        "src/tests": "# Test Files\n\nTest suites, test cases, and testing utilities generated by the UI Tester agent.",
        "src/config": "# Configuration Files\n\nApplication configuration, environment settings, and deployment configurations."
    }

    for folder_path, content in readme_content.items():
        readme_path = project_path / folder_path / "README.md"
        readme_path.write_text(content, encoding="utf-8")


def _create_staging_readmes(project_path: Path) -> None:
    """Create simple README files in staging folders."""
    agents = ["business_analyst", "software_architect",
              "ui_designer", "developer", "ui_tester", "code_reviewer"]

    for agent in agents:
        readme_content = f"""# {agent.replace('_', ' ').title()} Staging

Working folder for the {agent.replace('_', ' ')} agent.
Files are generated dynamically based on task requirements.
"""
        readme_path = project_path / "staging" / agent / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")


def _create_project_info(project_path: Path, user_request: str, title: str) -> None:
    """
    Create a project information file.

    Args:
        project_path (Path): Path to the project folder
        user_request (str): Original user request
        title (str): Project title
    """
    info_content = f"""# Project Information

**Project Title:** {title}
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Folder:** {project_path.name}

## Original Request
{user_request}

## Project Structure
- `src/` - Source code
- `docs/` - Documentation
- `assets/` - Static resources
- `staging/` - Worker agent staging folders

## Status
- **Phase:** Planning
- **Progress:** Started
"""

    info_path = project_path / "PROJECT_INFO.md"
    info_path.write_text(info_content, encoding="utf-8")


def get_current_project_path() -> Optional[str]:
    """Get the current project path."""
    return _current_project


def list_projects(base_path: str = ".") -> List[Dict[str, str]]:
    """
    List all existing projects.

    Args:
        base_path (str): Base path where projects are located

    Returns:
        List[Dict[str, str]]: List of project information
    """
    base_path_obj = Path(base_path)
    projects = []

    for item in base_path_obj.iterdir():
        if item.is_dir() and item.name.startswith("project_"):
            info_file = item / "PROJECT_INFO.md"
            if info_file.exists():
                try:
                    content = info_file.read_text(encoding="utf-8")
                    # Extract title from content
                    title_line = [line for line in content.split(
                        '\n') if line.startswith('**Project Title:**')]
                    title = title_line[0].split(
                        ':', 1)[1].strip() if title_line else item.name

                    projects.append({
                        "folder": item.name,
                        "title": title,
                        "path": str(item),
                        "created": item.stat().st_ctime
                    })
                except Exception:
                    # Fallback if info file is corrupted
                    projects.append({
                        "folder": item.name,
                        "title": item.name,
                        "path": str(item),
                        "created": item.stat().st_ctime
                    })

    # Sort by creation time (newest first)
    projects.sort(key=lambda x: x["created"], reverse=True)
    return projects


def set_current_project(project_path: str) -> bool:
    """
    Set the current active project.

    Args:
        project_path (str): Path to the project folder

    Returns:
        bool: True if successful, False otherwise
    """
    global _current_project

    if Path(project_path).exists():
        _current_project = project_path
        return True
    return False


def update_agent_staging_readme(project_path: str, agent_name: str, agent_response: str) -> None:
    """
    Update the agent's staging README.md file with generated file information.

    Args:
        project_path (str): Path to the project folder
        agent_name (str): Name of the agent (e.g., "business_analyst")
        agent_response (str): JSON response from the agent
    """
    try:
        # Parse the JSON response - convert AgentResult to string first
        try:
            response_data = json.loads(str(agent_response))
        except json.JSONDecodeError:
            # If not valid JSON, skip update
            return

        project_path_obj = Path(project_path)
        staging_path = project_path_obj / "staging" / agent_name
        readme_path = staging_path / "README.md"

        # Create staging folder if it doesn't exist
        staging_path.mkdir(parents=True, exist_ok=True)

        # Generate README content
        readme_content = _generate_staging_readme_content(
            agent_name, response_data)

        # Write README content
        readme_path.write_text(readme_content, encoding="utf-8")

    except Exception as e:
        # Don't fail the main workflow if README update fails
        print(f"⚠️  Warning: Could not update staging README.md: {e}")


def _generate_staging_readme_content(agent_name: str, response_data: Dict) -> str:
    """Generate README content for agent staging folder."""

    agent_display_name = agent_name.replace('_', ' ').title()

    # Get response information
    summary = response_data.get('summary', 'Agent completed its tasks.')
    status = response_data.get('status', 'completed')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Start building content
    content = f"""# {agent_display_name} - Generated Files

**Status:** {status.upper()}  
**Last Updated:** {timestamp}

## Summary

{summary}

"""

    # Add generated files section
    generated_files = response_data.get('generated_files', [])
    if generated_files:
        content += "## Generated Files\n\n"

        for file_info in generated_files:
            file_name = file_info.get('file_name', 'Unknown file')
            description = file_info.get(
                'content_description', 'No description provided')
            key_insights = file_info.get('key_insights', [])

            content += f"### {file_name}\n\n"
            content += f"**Description:** {description}\n\n"

            if key_insights:
                content += "**Key Insights:**\n"
                for insight in key_insights:
                    content += f"- {insight}\n"
                content += "\n"

    # Add recommendations section
    recommendations = response_data.get('recommendations', [])
    if recommendations:
        content += "## Recommendations\n\n"
        for rec in recommendations:
            content += f"- {rec}\n"
        content += "\n"

    # Add downstream inputs if available
    downstream_inputs = response_data.get('downstream_inputs', {})
    if downstream_inputs:
        content += "## Information for Downstream Agents\n\n"

        for next_agent, inputs in downstream_inputs.items():
            content += f"### For {next_agent.replace('_', ' ').title()}\n\n"

            for param_name, param_value in inputs.items():
                content += f"**{param_name}:** {param_value}\n\n"

    # Add footer
    content += "---\n\n"
    content += f"*Generated by {agent_display_name} agent from the Strands Coding Squad*\n"

    return content


def create_project_readme(project_path: str) -> None:
    """
    Create initial project README.md file in the main project folder.

    Args:
        project_path (str): Path to the project folder
    """
    try:
        project_path_obj = Path(project_path)
        readme_path = project_path_obj / "README.md"

        # Get project information
        project_name = project_path_obj.name
        project_title = project_name

        # Try to get project title from PROJECT_INFO.md
        info_file = project_path_obj / "PROJECT_INFO.md"
        if info_file.exists():
            try:
                info_content = info_file.read_text(encoding="utf-8")
                title_line = [line for line in info_content.split(
                    '\n') if line.startswith('**Project Title:**')]
                if title_line:
                    project_title = title_line[0].split(':', 1)[1].strip()
            except Exception:
                pass

        # Create initial README content
        readme_content = f"""# {project_title}

## Project Overview

This project was generated by the Strands Coding Squad multi-agent system.

**Project Status:** 🚧 In Progress

## Agent Workflow Progress

<!-- AGENT_PROGRESS_START -->
<!-- AGENT_PROGRESS_END -->

## Project Structure

```
{project_name}/
├── src/                       # Source code
├── docs/                      # Documentation
├── assets/                    # Static resources
├── staging/                   # Agent working folders
│   ├── business_analyst/      # Business analysis and requirements
│   ├── software_architect/    # System architecture and design
│   ├── ui_designer/           # UI/UX design specifications
│   ├── developer/             # Code implementation
│   ├── ui_tester/            # UI testing and validation
│   └── code_reviewer/         # Code quality review
├── PROJECT_INFO.md           # Project metadata
└── README.md                 # This file
```

## Getting Started

1. Review the project requirements in `staging/business_analyst/`
2. Check the system architecture in `staging/software_architect/`
3. Examine the source code in `src/`
4. Read the documentation in `docs/`

## Generated Files

Each agent creates files in their respective staging folders:
- **Business Analyst**: Requirements, user stories, stakeholder analysis
- **Software Architect**: Architecture diagrams, technology stack, design patterns
- **UI Designer**: Wireframes, mockups, design specifications
- **Developer**: Source code, tests, documentation
- **UI Tester**: Test reports, bug findings, accessibility audits
- **Code Reviewer**: Code quality reports, security assessments

---

*Generated by [Strands Coding Squad](https://github.com/strands-agents/sdk-python)*
"""

        # Write README file
        readme_path.write_text(readme_content, encoding="utf-8")

    except Exception as e:
        print(f"⚠️  Warning: Could not create project README.md: {e}")


def update_project_readme_with_agent_work(project_path: str, agent_name: str, agent_response: str) -> None:
    """
    Update the main project README.md file with agent work progress.

    Args:
        project_path (str): Path to the project folder
        agent_name (str): Name of the agent
        agent_response (str): JSON response from the agent
    """
    try:
        # Parse the JSON response - convert AgentResult to string first
        try:
            response_data = json.loads(str(agent_response))
        except json.JSONDecodeError:
            return

        project_path_obj = Path(project_path)
        readme_path = project_path_obj / "README.md"

        # Create README if it doesn't exist
        if not readme_path.exists():
            create_project_readme(project_path)

        # Read current README content
        current_content = readme_path.read_text(encoding="utf-8")

        # Generate agent progress entry
        agent_progress = _generate_agent_progress_entry(
            agent_name, response_data)

        # Update README with agent progress
        updated_content = _update_project_readme_progress(
            current_content, agent_name, agent_progress)

        # Write updated content back
        readme_path.write_text(updated_content, encoding="utf-8")

    except Exception as e:
        print(f"⚠️  Warning: Could not update project README.md: {e}")


def _generate_agent_progress_entry(agent_name: str, response_data: Dict) -> str:
    """Generate progress entry for an agent."""

    agent_display_name = agent_name.replace('_', ' ').title()
    status = response_data.get('status', 'completed')
    summary = response_data.get('summary', 'Agent completed its tasks.')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Count generated files
    generated_files = response_data.get('generated_files', [])
    file_count = len(generated_files)

    # Get key deliverables
    deliverables = []
    for file_info in generated_files:
        file_name = file_info.get('file_name', 'Unknown file')
        deliverables.append(file_name)

    # Status emoji
    status_emoji = "✅" if status == "completed" else "🔄"

    progress_entry = f"""### {status_emoji} {agent_display_name}

**Status:** {status.upper()} | **Updated:** {timestamp}

{summary}

**Generated Files:** {file_count} files
"""

    if deliverables:
        progress_entry += f"**Key Deliverables:** {', '.join(deliverables[:3])}"
        if len(deliverables) > 3:
            progress_entry += f" and {len(deliverables) - 3} more"
        progress_entry += "\n"

    progress_entry += f"**Details:** See `staging/{agent_name}/README.md`\n\n"

    return progress_entry


def _update_project_readme_progress(current_content: str, agent_name: str, agent_progress: str) -> str:
    """Update project README with agent progress."""

    # Find the progress markers
    start_marker = "<!-- AGENT_PROGRESS_START -->"
    end_marker = "<!-- AGENT_PROGRESS_END -->"

    start_idx = current_content.find(start_marker)
    end_idx = current_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        # Markers not found, append at the end
        return current_content + "\n\n" + agent_progress

    # Extract current progress section
    progress_start = start_idx + len(start_marker)
    progress_content = current_content[progress_start:end_idx]

    # Check if agent progress already exists
    agent_header = f"### ✅ {agent_name.replace('_', ' ').title()}"
    agent_header_alt = f"### 🔄 {agent_name.replace('_', ' ').title()}"

    if agent_header in progress_content or agent_header_alt in progress_content:
        # Replace existing agent progress
        lines = progress_content.split('\n')
        new_lines = []
        skip_section = False

        for line in lines:
            if (line.startswith(f"### ✅ {agent_name.replace('_', ' ').title()}") or
                    line.startswith(f"### 🔄 {agent_name.replace('_', ' ').title()}")):
                skip_section = True
                new_lines.append(agent_progress.strip())
            elif line.startswith("### ") and skip_section:
                skip_section = False
                new_lines.append(line)
            elif not skip_section:
                new_lines.append(line)

        new_progress_content = '\n'.join(new_lines)
    else:
        # Add new agent progress
        new_progress_content = progress_content + '\n' + agent_progress

    # Reconstruct the content
    updated_content = (
        current_content[:progress_start] +
        new_progress_content +
        current_content[end_idx:]
    )

    return updated_content
