# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project implements a complete software engineering team powered by multiple GenAI agents. The system provides an intelligent, multi-agent approach to software development that can handle projects of varying complexity.

**Core System Components:**
- **Project Manager Agent**: Main orchestrator that runs directly within the application
- **Worker Agents**: Specialized tools for different roles (business analyst, software architect, UI designer, developer, UI tester, code reviewer)

## Current Architecture

The application follows a mature tool-based architecture with intelligent workflow management:

```
User Request → Project Manager Agent → Worker Agent Tools → Organized Project Output
```

**Workflow Process:**
1. Receives software project requirements via interactive CLI
2. AI-powered project naming and folder organization
3. Project Manager agent analyzes requirements and plans workflow
4. Delegates tasks to appropriate worker agents based on complexity
5. Worker agents provide structured outputs with downstream inputs
6. Supports continuing work on existing projects

## Tech Stack

- **Language**: Python 3.8+
- **Framework**: Strands Agents SDK (https://github.com/strands-agents/sdk-python)
- **Architecture**: Multi-agent system with structured information flow
- **Tools**: File I/O, Python REPL, structured JSON responses

## Current Development Status

**Status**: ✅ **FULLY IMPLEMENTED AND FUNCTIONAL**

### ✅ Completed Features

#### Core System
- [x] Interactive CLI application (`main.py`)
- [x] Project Manager agent with intelligent orchestration (`project_manager.py`)
- [x] Project utilities with AI-powered naming (`project_utils.py`)
- [x] Simplified project folder structure
- [x] Agent staging areas for work organization

#### Agent Implementation
- [x] Business Analyst agent with smart complexity analysis
- [x] Software Architect agent with technical design capabilities
- [x] UI Designer agent with user experience focus
- [x] Developer agent with code implementation
- [x] UI Tester agent with testing capabilities
- [x] Code Reviewer agent with quality assurance

#### Advanced Features
- [x] Smart complexity assessment to prevent over-engineering
- [x] AI-powered project naming system
- [x] Structured agent communication with downstream inputs
- [x] Project continuation functionality
- [x] Agent dependency management
- [x] Comprehensive context files for each agent

#### User Experience
- [x] Interactive project creation
- [x] Project listing and selection
- [x] Continue existing projects workflow
- [x] Clear command interface
- [x] Organized project output structure

### 📁 Current Project Structure

```
strands-coding-squad/
├── main.py                    # CLI entry point
├── project_manager.py         # Project Manager agent
├── project_utils.py          # Project utilities with AI naming
├── pyproject.toml            # Python project configuration
├── context/                  # Agent context files
│   ├── business_analyst.md   # Enhanced with complexity analysis
│   ├── software_architect.md # Technical design context
│   ├── ui_designer.md        # UI/UX design context
│   ├── developer.md          # Development context
│   ├── ui_tester.md          # Testing context
│   ├── code_reviewer.md      # Code review context
│   └── project_manager.md    # Project management context
├── tools/                    # Worker agent implementations
│   ├── business_analyst.py   # Requirements and complexity analysis
│   ├── software_architect.py # System architecture design
│   ├── ui_designer.py        # UI/UX design
│   ├── developer.py          # Code implementation
│   ├── ui_tester.py          # UI testing
│   └── code_reviewer.py      # Code quality review
├── tests/                    # Test files
│   └── test_project_manager.py
├── README.md                 # Comprehensive documentation
└── CLAUDE.md                 # This file
```

### 🔄 Agent Dependencies (Implemented)

The system implements structured information flow:

```
Business Analyst → Software Architect → Developer → Code Reviewer
                ↓
              UI Designer → UI Tester
```

**Key Dependency Features:**
- Each agent outputs structured JSON with `downstream_inputs`
- Parameter names match between agent outputs and inputs
- Clear information flow prevents data loss
- Agents can work in parallel where appropriate

### 🧠 Smart Features

1. **Complexity Analysis**: Business Analyst assesses project complexity (Simple/Moderate/Complex) and adjusts documentation accordingly
2. **AI Naming**: Projects are named using AI analysis of requirements
3. **Structured Communication**: Agents provide specific inputs for downstream agents
4. **Project Continuation**: Users can resume work on existing projects
5. **Flexible Workflow**: System adapts to different project types and complexities

## Working with This Codebase

### Key Files to Understand

1. **`main.py`**: CLI interface with interactive commands
2. **`project_manager.py`**: Core orchestration logic
3. **`project_utils.py`**: Project creation and AI naming
4. **`context/`**: Agent behavior and output specifications
5. **`tools/`**: Worker agent implementations

### Common Development Tasks

#### Adding New Agent
1. Create context file in `context/new_agent.md`
2. Implement tool in `tools/new_agent.py`
3. Add to Project Manager's tool list
4. Update downstream dependencies

#### Modifying Agent Behavior
1. Edit the relevant context file in `context/`
2. Test agent responses
3. Update downstream dependencies if needed

#### Enhancing Project Structure
1. Modify `project_utils.py` for folder changes
2. Update `project_manager.py` context if needed
3. Update README.md documentation

### Testing
```bash
python -m pytest tests/
```

### Running the System
```bash
python main.py
```

## Enhancement Opportunities

### 🚀 Potential Improvements

#### System Enhancements
- [ ] Configuration management system
- [ ] Logging and monitoring capabilities
- [ ] Performance metrics and optimization
- [ ] Error handling and recovery mechanisms
- [ ] Agent communication validation

#### Agent Capabilities
- [ ] More sophisticated complexity analysis
- [ ] Integration with external APIs
- [ ] Real-time collaboration features
- [ ] Version control integration
- [ ] Automated testing execution

#### User Experience
- [ ] Web interface for project management
- [ ] Project templates and presets
- [ ] Export capabilities (PDF, HTML)
- [ ] Search and filter functionality
- [ ] Progress tracking and notifications

#### Technical Improvements
- [ ] Async agent execution for better performance
- [ ] Caching system for repeated operations
- [ ] Plugin architecture for extensibility
- [ ] Database integration for project persistence
- [ ] API endpoints for external integration

### 🔧 Development Guidelines

#### Code Quality
- Follow existing patterns in agent implementations
- Maintain structured JSON response format
- Update agent dependencies when modifying outputs
- Write comprehensive context files for new agents

#### Testing
- Test agent tools individually
- Test Project Manager orchestration
- Test CLI interface functionality
- Test project creation and continuation

#### Documentation
- Update README.md for new features
- Maintain context files for agent behavior
- Document agent dependencies
- Update this CLAUDE.md for significant changes

## Recent Major Updates

### Latest Enhancements (Current Session)
1. **Smart Complexity Analysis**: Business Analyst now assesses project complexity to prevent over-engineering
2. **Agent Dependencies**: Implemented structured information flow between agents
3. **Project Continuation**: Added ability to resume work on existing projects
4. **AI Naming**: Enhanced project naming with AI analysis
5. **Simplified Structure**: Streamlined project folders to focus on essentials
6. **Documentation**: Comprehensive README and context updates

### System Maturity
The system has evolved from a basic concept to a fully functional multi-agent software development platform. It successfully handles:
- Simple utility functions with minimal overhead
- Complex applications with comprehensive analysis
- Structured workflows with clear dependencies
- Organized project management with AI assistance

## Getting Started for New Contributors

1. **Understand the Architecture**: Review the agent workflow and dependencies
2. **Run the System**: Try creating different types of projects
3. **Examine Agent Outputs**: Look at generated files in staging folders
4. **Read Context Files**: Understand how agents are configured
5. **Test Modifications**: Make small changes and observe behavior

The system is production-ready and can be extended with additional agents, features, and integrations as needed.