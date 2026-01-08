
import sys
import os
from rich.text import Text
from textual.widgets import DataTable

# Add current directory to path
sys.path.append(os.getcwd())

from src.models.task import Task
from src.models.priority import Priority
from src.ui.premium_todo_app import TaskTable

def reproduce_crash():
    print("Attempting to reproduce crash...")
    try:
        # Simulate creating a task like TaskService.add_task does
        # Note: TaskService.add_task does NOT pass priority, so it is None
        new_task = Task(id=1, title="Crash Test", description="Testing", completed=False)
        print(f"Created task: {new_task}")
        
        # Instantiate table
        table = TaskTable()
        
        # internal Textual setup (simplified)
        
        print("Calling update_tasks...")
        table.update_tasks([new_task])
        print("SUCCESS: update_tasks completed without error.")
        
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce_crash()
