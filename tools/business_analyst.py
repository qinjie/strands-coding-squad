"""
Implement a tool which provides the functions of a business analyst, i.e. gathering requirements and creating user stories.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import boto3
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import file_read, file_write

from constants import MODEL_BUSINESS_ANALYST
from context_manager import get_condensed_context
from project_utils import (update_agent_staging_readme,
                           update_project_readme_with_agent_work)

# Define the tools we need
tools = [file_read, file_write]

os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Script directory for relative paths
script_dir = Path(__file__).parent


def business_analyst_work(input_text: str, complexity_level: str = "SIMPLE") -> str:
    """
    Business analyst work function that processes input text and returns the agent's response.

    Args:
        input_text (str): The input text containing business requirements or specifications
        complexity_level (str): Project complexity level (SIMPLE, MODERATE, COMPLEX)

    Returns:
        str: The agent's response including analysis and recommendations
    """
    try:
        bedrock_model = BedrockModel(
            model_id=MODEL_BUSINESS_ANALYST,
            temperature=0.2,
            top_p=0.8
        )

        # Get context based on complexity level
        system_prompt = get_condensed_context(
            "business_analyst", complexity_level)

        # Create agent with appropriate context
        agent = Agent(model=bedrock_model,
                      system_prompt=system_prompt, tools=tools)

        response = agent(input_text)
        return response
    except ValueError as e:
        return f"Input value error in business analyst tool: {str(e)}"
    except RuntimeError as e:
        return f"Runtime error in business analyst tool: {str(e)}"
    except ImportError as e:
        return f"Import error in business analyst tool: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred in business analyst tool: {str(e)}"


@tool
def business_analyst_tool(
    project_description: str,
    project_path: str,
    stakeholders: Optional[str] = None,
    business_objectives: Optional[str] = None,
    target_users: Optional[str] = None,
    constraints: Optional[str] = None,
    timeline: Optional[str] = None,
    budget: Optional[str] = None,
    market_context: Optional[str] = None
) -> str:
    """
    Business analyst tool that gathers requirements and creates user stories.

    Creates markdown files in the staging/business_analyst/ folder and returns a JSON response
    listing the generated files and their contents.

    This tool provides the functionality of a business analyst agent that can:
    - Gather and analyze business requirements
    - Create detailed user stories and acceptance criteria
    - Bridge the gap between business needs and technical solutions
    - Perform stakeholder analysis and requirements documentation
    - Create business process flows and workflows

    Args:
        project_description (str): Main project description and goals
        project_path (str): Path to the project folder (to access staging area)
        stakeholders (Optional[str]): Key stakeholders and their roles
        business_objectives (Optional[str]): Specific business objectives and success criteria
        target_users (Optional[str]): Target audience and user demographics
        constraints (Optional[str]): Business constraints and limitations
        timeline (Optional[str]): Project timeline and milestones
        budget (Optional[str]): Budget constraints and considerations
        market_context (Optional[str]): Market context and competitive landscape

    Returns:
        str: JSON response with list of generated files and their descriptions
    """
    # Convert to formatted string for the agent
    input_text = f"""
BUSINESS ANALYSIS REQUEST:

Project Path: {project_path}
Requirements Location: {project_path}/docs/requirements/
Staging Folder: {project_path}/staging/business_analyst/

Project Description: {project_description}

{f'Stakeholders: {stakeholders}' if stakeholders else ''}
{f'Business Objectives: {business_objectives}' if business_objectives else ''}
{f'Target Users: {target_users}' if target_users else ''}
{f'Constraints: {constraints}' if constraints else ''}
{f'Timeline: {timeline}' if timeline else ''}
{f'Budget: {budget}' if budget else ''}
{f'Market Context: {market_context}' if market_context else ''}

INSTRUCTIONS:
1. Create business analysis files in docs/requirements/ folder
2. Also create copies in staging/business_analyst/ for traceability
3. Generate whatever files you think are necessary (e.g., user_stories.md, requirements.md, etc.)
4. Each file should contain detailed, well-structured content
5. Return a JSON response with the primary file locations (not staging paths)

{{
  "status": "completed",
  "summary": "Brief summary of the business analysis completed",
  "generated_files": [
    {{
      "file_path": "docs/requirements/filename.md",
      "file_name": "filename.md", 
      "content_description": "Description of what this file contains",
      "key_insights": ["List", "of", "key", "insights", "from", "this", "file"]
    }}
  ],
  "recommendations": ["Key", "recommendations", "from", "the", "analysis"],
  "downstream_inputs": {{
    "complexity_level": "Project complexity assessment (SIMPLE/MODERATE/COMPLEX)",
    "software_architect": {{
      "requirements": "Consolidated business requirements for architecture design",
      "complexity_level": "Project complexity assessment (SIMPLE/MODERATE/COMPLEX)",
      "performance_requirements": "Performance criteria and benchmarks",
      "security_requirements": "Security constraints and compliance needs",
      "integration_requirements": "External system integration requirements",
      "scalability_requirements": "Scalability and load requirements",
      "compliance_requirements": "Regulatory and compliance requirements"
    }},
    "ui_designer": {{
      "user_requirements": "User stories and functional requirements",
      "complexity_level": "Project complexity assessment (SIMPLE/MODERATE/COMPLEX)",
      "user_personas": "Target audience and user personas",
      "accessibility_requirements": "Accessibility standards and requirements",
      "content_structure": "Content structure and information architecture"
    }}
  }}
}}

Expected deliverables:
- docs/requirements/complexity_assessment.md - Project complexity analysis
- docs/requirements/functional_specification.md - SDD functional specification blueprint
- docs/requirements/user_stories.md - User stories with acceptance criteria
- docs/requirements/requirements.md - Functional and non-functional requirements
- Additional files based on complexity: stakeholder_analysis.md, risk_assessment.md, business_processes.md, success_metrics.md
- staging/business_analyst/ - Working copies of all files for traceability
"""

    # Determine complexity level based on project description
    # Simple heuristic: check for keywords that indicate complexity
    complexity_keywords = {
        "SIMPLE": ["function", "utility", "small", "simple", "basic", "single"],
        "MODERATE": ["application", "app", "system", "multiple", "integration"],
        "COMPLEX": ["enterprise", "platform", "architecture", "microservices", "distributed", "scalable", "large-scale", "complex"]
    }

    complexity_level = "SIMPLE"  # Default
    description_lower = project_description.lower()

    # Check for complex keywords first
    for keyword in complexity_keywords["COMPLEX"]:
        if keyword in description_lower:
            complexity_level = "COMPLEX"
            break

    # If not complex, check for moderate keywords
    if complexity_level == "SIMPLE":
        for keyword in complexity_keywords["MODERATE"]:
            if keyword in description_lower:
                complexity_level = "MODERATE"
                break

    result = business_analyst_work(input_text.strip(), complexity_level)

    # Update staging README with generated file information
    update_agent_staging_readme(project_path, "business_analyst", result)

    # Update main project README with agent work progress
    update_project_readme_with_agent_work(
        project_path, "business_analyst", result)

    return result


if __name__ == "__main__":
    # Simple test for the business analyst tool with structured inputs
    print("Testing Business Analyst Tool")
    print("=" * 50)

    try:
        result = business_analyst_tool(
            project_description="Build a web application for a small restaurant that allows customers to view menu, place orders, track status, and make payments. Restaurant owner needs to manage menu items and orders.",
            project_path=script_dir.parent / "tmp",  # Test project path
            stakeholders="Restaurant owner, customers, delivery drivers, kitchen staff",
            business_objectives="Increase order volume by 30%, reduce order processing time, improve customer satisfaction",
            target_users="Local restaurant customers aged 25-65, tech-savvy diners, busy professionals",
            constraints="Limited budget ($10,000), 3-month timeline, must integrate with existing POS system",
            timeline="3 months development, 1 month testing, go-live in 4 months",
            budget="$10,000 total budget including development and hosting",
            market_context="Competing with delivery apps like UberEats, DoorDash in local market"
        )
        print("Output:")
        print("-" * 30)
        print(result)
    except Exception as e:
        print(f"Error during testing: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
