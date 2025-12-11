# Quickstart Guide: Todo Console App

## Prerequisites
- Python 3.13 or higher
- UV package manager (optional, for dependency management)

## Setup
1. Clone or download the project
2. Navigate to the project directory
3. No additional setup required (uses only Python standard library)

## Running the Application
```bash
python todo_app.py
```

## Basic Usage
1. The application starts with a numbered menu
2. Select options by entering the corresponding number
3. Follow the on-screen prompts for each operation
4. Exit the application by typing "exit" or "quit"

## Available Operations
- **Add Task**: Create a new task with title and description
- **View Tasks**: Display all tasks in table format
- **Update Task**: Modify an existing task's title or description
- **Delete Task**: Remove a task with confirmation prompt
- **Mark Complete**: Toggle a task's completion status
- **Exit**: Gracefully close the application

## Input Validation
- Title: 1-50 characters
- Description: 0-200 characters
- Task IDs must be valid and exist in the system
- Invalid inputs will show error messages with guidance

## Error Handling
- All invalid operations show clear error messages
- The application continues running after errors
- Confirmation prompts prevent accidental deletions