#!/usr/bin/env python3
"""
Test script for the project management functionality.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import project_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project_utils import create_project_folder, list_projects, generate_project_title


def test_project_creation():
    """Test project creation and folder structure."""
    print("🧪 Testing Project Manager")
    print("=" * 40)
    
    # Test project creation
    test_requests = [
        "Create a restaurant ordering web application",
        "Build a todo list app with user authentication",
        "Develop a weather forecast dashboard"
    ]
    
    created_projects = []
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📝 Test {i}: {request}")
        
        try:
            project_path = create_project_folder(request)
            created_projects.append(project_path)
            
            project_name = Path(project_path).name
            print(f"✅ Created: {project_name}")
            
            # Verify folder structure
            expected_folders = [
                "planning", "requirements", "architecture", "design",
                "src", "tests", "docs", "reviews", "deployment", "assets"
            ]
            
            missing_folders = []
            for folder in expected_folders:
                folder_path = Path(project_path) / folder
                if not folder_path.exists():
                    missing_folders.append(folder)
            
            if missing_folders:
                print(f"❌ Missing folders: {missing_folders}")
            else:
                print("✅ All subfolders created successfully")
                
            # Check for PROJECT_INFO.md
            info_file = Path(project_path) / "PROJECT_INFO.md"
            if info_file.exists():
                print("✅ PROJECT_INFO.md created")
            else:
                print("❌ PROJECT_INFO.md missing")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test project listing
    print("\n📂 Listing projects:")
    projects = list_projects()
    for proj in projects:
        print(f"  - {proj['folder']}: {proj['title']}")
    
    # Test title generation
    print("\n🏷️  Testing title generation:")
    test_titles = [
        "I want to build a React dashboard for analytics",
        "Create a Python API for user management",
        "Build a mobile app for food delivery"
    ]
    
    for request in test_titles:
        title = generate_project_title(request)
        print(f"  '{request}' → '{title}'")
    
    print(f"\n✅ Test completed! Created {len(created_projects)} projects.")
    return created_projects


def cleanup_test_projects(project_paths):
    """Clean up test projects."""
    import shutil
    
    print("\n🧹 Cleaning up test projects...")
    for project_path in project_paths:
        try:
            shutil.rmtree(project_path)
            project_name = Path(project_path).name
            print(f"🗑️  Removed: {project_name}")
        except Exception as e:
            print(f"❌ Error removing {project_path}: {e}")


if __name__ == "__main__":
    created_projects = test_project_creation()
    
    # Ask user if they want to keep the test projects
    print("\n❓ Keep test projects? (y/N): ", end="")
    try:
        response = input().lower()
        if response not in ['y', 'yes']:
            cleanup_test_projects(created_projects)
        else:
            print("📁 Test projects kept for inspection.")
    except (KeyboardInterrupt, EOFError):
        print("\n🧹 Cleaning up test projects...")
        cleanup_test_projects(created_projects)