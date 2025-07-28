"""
Main entry point for the Software Engineer Squad system.
Handles user interaction and delegates project management tasks.
"""
import sys
import logging
from pathlib import Path
from project_manager import handle_user_request, continue_project
from project_utils import list_projects

# # Enable debug logging for Strands
# logging.getLogger("strands").setLevel(logging.INFO)
# logging.basicConfig(
#     format="%(levelname)s | %(name)s | %(message)s",
#     handlers=[logging.StreamHandler()],
# )


def show_main_menu():
    """Display the main menu options."""
    print("\n" + "=" * 60)
    print("🚀 Software Engineer Squad - Multi-Agent Development System")
    print("=" * 60)
    print("Please select an option:")
    print()
    print("1. 🆕 Create New Project")
    print("2. 📂 Continue Existing Project")
    print("3. ❌ Quit")
    print()


def get_user_choice():
    """Get user menu choice with input validation."""
    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            return 3


def get_new_project_request():
    """Get project request for new project creation."""
    print("\n📝 Enter your project request:")
    print("(Press Ctrl+D or Ctrl+Z then Enter to finish)")

    try:
        full_input = sys.stdin.read()
        lines = full_input.splitlines()
        user_input = "\n".join(lines).strip()
        return user_input
    except (EOFError, KeyboardInterrupt):
        print("\n❌ Cancelled.")
        return None


def show_project_menu():
    """Show existing projects and let user select one."""
    projects = list_projects()
    if not projects:
        print("\n❌ No existing projects found.")
        input("Press Enter to continue...")
        return None

    print(f"\n📂 Found {len(projects)} existing project(s):")
    print("-" * 50)
    for i, proj in enumerate(projects, 1):
        print(f"  {i}. {proj['folder']} - {proj['title']}")
    print("  0. 🔙 Back to main menu")

    while True:
        try:
            choice = input(
                f"\nEnter project number (0-{len(projects)}): ").strip()
            if choice == '0':
                return None

            project_idx = int(choice) - 1
            if 0 <= project_idx < len(projects):
                selected_project = projects[project_idx]
                return selected_project['path']
            else:
                print(f"❌ Invalid choice. Please enter 0-{len(projects)}.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Cancelled.")
            return None


def handle_existing_project(project_path):
    """Handle continuation of an existing project."""
    print(f"\n📁 Selected project: {Path(project_path).name}")
    print(f"📂 Location: {project_path}")

    print("\n📝 Enter your additional request for the project:")
    print("(Press Ctrl+D or Ctrl+Z to continue without changes, or type your request)")

    try:
        # This will immediately catch Ctrl+D/Ctrl+Z without requiring Enter first
        additional_input = sys.stdin.read()
        additional_lines = additional_input.splitlines()
        additional_request = "\n".join(additional_lines).strip()

        if additional_request:
            print(f"\n📋 Request: {additional_request}")
            continue_project(project_path, additional_request)
        else:
            # Continue with existing project without additional requirements
            default_request = "Please review the current project status and continue with the next appropriate steps in the development workflow."
            print("📋 Continuing with existing project workflow...")
            continue_project(project_path, default_request)

    except (EOFError, KeyboardInterrupt):
        # User pressed Ctrl+D or Ctrl+Z - continue without additional requirements
        default_request = "Please review the current project status and continue with the next appropriate steps in the development workflow."
        print("\n📋 Continuing with existing project workflow...")
        continue_project(project_path, default_request)


def run_interactive_session():
    """Run the main interactive session for the project manager."""
    print("Welcome to the Strands Coding Squad!")

    while True:
        show_main_menu()
        choice = get_user_choice()

        if choice == 1:
            # Create new project
            user_input = get_new_project_request()
            if user_input:
                print(f"\n📋 Request: {user_input}")
                handle_user_request(user_input)
                input("\nPress Enter to continue...")

        elif choice == 2:
            # Continue existing project
            project_path = show_project_menu()
            if project_path:
                handle_existing_project(project_path)
                input("\nPress Enter to continue...")

        elif choice == 3:
            # Quit
            print("👋 Goodbye!")
            break


def main():
    """Main entry point."""
    run_interactive_session()


if __name__ == "__main__":
    main()
