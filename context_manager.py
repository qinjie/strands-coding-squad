"""
Context Manager for Token Optimization
Provides complexity-based context loading to reduce token usage.
"""

from pathlib import Path
from typing import Dict, Optional


def get_condensed_context(agent_type: str, complexity_level: str = "SIMPLE") -> str:
    """
    Get context based on project complexity to minimize token usage.
    
    Args:
        agent_type: Type of agent (business_analyst, developer, etc.)
        complexity_level: SIMPLE, MODERATE, or COMPLEX
        
    Returns:
        Optimized context string
    """
    
    # Condensed contexts for SIMPLE projects (10-15 lines vs 100+ lines)
    simple_contexts = {
        "business_analyst": """# BUSINESS ANALYST AGENT
You analyze requirements and assess complexity. Create business analysis files in staging/business_analyst/.

## Core Rules
1. Assess complexity first (SIMPLE/MODERATE/COMPLEX)
2. Create proportional documentation - SIMPLE projects need minimal docs
3. Focus on essential requirements only
4. Generate user stories and functional specs
5. For risk assessment: ONLY focus on technical risks in implemented solution, not requirements/operational/management risks

## Output: JSON with status, summary, generated_files, recommendations, downstream_inputs
Files: complexity_assessment.md, functional_specification.md, user_stories.md (for SIMPLE)""",

        "software_architect": """# SOFTWARE ARCHITECT AGENT
You design system architecture. Create architecture files in staging/software_architect/.

## Core Rules
1. Design based on complexity level from Business Analyst
2. SIMPLE projects: basic architecture only
3. Focus on essential technical decisions
4. Create implementation guidelines

## Output: JSON with status, summary, generated_files, recommendations, downstream_inputs
Files: technical_specification.md, system_architecture.md (for SIMPLE)""",

        "ui_designer": """# UI/UX DESIGNER AGENT
You create UI/UX designs. Create design files in staging/ui_designer/.

## Core Rules
1. Design based on complexity level
2. SIMPLE projects: basic wireframes and components
3. Focus on essential user experience
4. Ensure accessibility compliance

## Output: JSON with status, summary, generated_files, recommendations, downstream_inputs
Files: wireframes.md, design_system.md (for SIMPLE)""",

        "developer": """# DEVELOPER AGENT
You implement code based on specifications. Create code files in staging/developer/.

## Core Rules
1. Follow specifications from architect
2. SIMPLE projects: essential implementation only
3. Write clean, working code
4. Include basic tests

## Output: JSON with status, summary, generated_files, recommendations, downstream_inputs
Files: source_code/, README.md, tests/ (for SIMPLE)""",

        "ui_tester": """# UI TESTER AGENT
You test UI functionality. Create test files in staging/ui_tester/.

## Core Rules
1. Test based on complexity level
2. SIMPLE projects: essential functional tests
3. Focus on core user workflows
4. Generate test scripts

## Output: JSON with status, summary, generated_files, recommendations, downstream_inputs
Files: test_plan.md, functional_tests.py (for SIMPLE)""",

        "code_reviewer": """# CODE REVIEWER AGENT
You review code quality. Create review files in staging/code_reviewer/.

## Core Rules
1. Review based on complexity level
2. SIMPLE projects: essential quality checks
3. Focus on functionality and basic best practices
4. Provide actionable feedback

## Output: JSON with status, summary, generated_files, recommendations, downstream_inputs
Files: code_review_report.md, quality_metrics.md (for SIMPLE)"""
    }
    
    # For COMPLEX projects, load full context
    if complexity_level == "COMPLEX":
        return load_full_context(agent_type)
    
    # For MODERATE projects, use condensed but more detailed
    if complexity_level == "MODERATE":
        return get_moderate_context(agent_type)
    
    # For SIMPLE projects, use minimal context
    return simple_contexts.get(agent_type, simple_contexts["business_analyst"])


def get_moderate_context(agent_type: str) -> str:
    """Get medium-detail context for MODERATE projects."""
    base_context = get_condensed_context(agent_type, "SIMPLE")
    
    if agent_type == "business_analyst":
        return base_context + "\n\n## Additional Guidelines for MODERATE projects:\n- Include more detailed documentation\n- Add extra validation steps\n- Consider additional edge cases\n- Risk assessment should focus ONLY on technical risks in the implemented solution"
    else:
        return base_context + "\n\n## Additional Guidelines for MODERATE projects:\n- Include more detailed documentation\n- Add extra validation steps\n- Consider additional edge cases"


def load_full_context(agent_type: str) -> str:
    """Load full context file for COMPLEX projects."""
    script_dir = Path(__file__).parent
    context_file = script_dir / "context" / f"{agent_type}.md"
    
    try:
        with open(context_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return get_condensed_context(agent_type, "SIMPLE")


def get_lean_project_context(project_path: str) -> str:
    """
    Get minimal project context (3-5 lines vs 71 lines).
    
    Args:
        project_path: Path to project folder
        
    Returns:
        Lean project context string
    """
    return f"""## PROJECT INFO
Path: {project_path}
Staging: {project_path}/staging/[agent_name]/
Task: Create files in staging folder, return JSON with status/files/summary."""


def get_complexity_based_file_limits(complexity_level: str) -> Dict[str, int]:
    """
    Get file generation limits based on complexity.
    
    Args:
        complexity_level: SIMPLE, MODERATE, or COMPLEX
        
    Returns:
        Dictionary with file limits
    """
    limits = {
        "SIMPLE": {
            "max_files": 3,
            "max_lines_per_file": 100,
            "business_analyst_files": ["complexity_assessment.md", "functional_specification.md", "user_stories.md"],
            "software_architect_files": ["technical_specification.md", "system_architecture.md"],
            "ui_designer_files": ["wireframes.md", "design_system.md"],
            "developer_files": ["source_code/", "README.md", "tests/"],
            "ui_tester_files": ["test_plan.md", "functional_tests.py"],
            "code_reviewer_files": ["code_review_report.md", "quality_metrics.md"]
        },
        "MODERATE": {
            "max_files": 6,
            "max_lines_per_file": 200,
            "business_analyst_files": ["complexity_assessment.md", "functional_specification.md", "user_stories.md", "requirements.md", "stakeholder_analysis.md"],
            "software_architect_files": ["technical_specification.md", "system_architecture.md", "technology_stack.md", "api_design_spec.md"],
            "ui_designer_files": ["wireframes.md", "mockups.md", "design_system.md", "components.md"],
            "developer_files": ["source_code/", "README.md", "tests/", "dependencies.md", "api_documentation.md"],
            "ui_tester_files": ["test_plan.md", "functional_tests.py", "accessibility_tests.py", "performance_tests.py"],
            "code_reviewer_files": ["code_review_report.md", "security_assessment.md", "performance_analysis.md", "quality_metrics.md"]
        },
        "COMPLEX": {
            "max_files": 12,
            "max_lines_per_file": 500,
            "business_analyst_files": ["complexity_assessment.md", "functional_specification.md", "user_stories.md", "requirements.md", "stakeholder_analysis.md", "risk_assessment.md", "business_processes.md", "success_metrics.md"],
            "software_architect_files": ["technical_specification.md", "system_architecture.md", "technology_stack.md", "api_design_spec.md", "database_schema.md", "security_architecture.md", "deployment_architecture.md", "integration_patterns.md", "performance_strategy.md", "implementation_guidelines.md"],
            "ui_designer_files": ["wireframes.md", "mockups.md", "design_system.md", "components.md", "responsive_design.md", "accessibility.md", "interactions.md", "user_testing.md"],
            "developer_files": ["source_code/", "README.md", "dependencies.md", "tests/", "database/", "api_documentation.md", "deployment_config/", "implementation_notes.md", "performance_guide.md", "security_implementation.md", "development_guide.md"],
            "ui_tester_files": ["test_plan.md", "test_cases.md", "functional_tests.py", "accessibility_tests.py", "performance_tests.py", "cross_browser_tests.py", "regression_tests.py", "test_data.json", "test_execution_report.md", "bug_reports.md", "testing_guidelines.md"],
            "code_reviewer_files": ["code_review_report.md", "security_assessment.md", "performance_analysis.md", "quality_metrics.md", "best_practices_checklist.md", "refactoring_suggestions.md", "test_coverage_analysis.md", "documentation_review.md"]
        }
    }
    
    return limits.get(complexity_level, limits["SIMPLE"])