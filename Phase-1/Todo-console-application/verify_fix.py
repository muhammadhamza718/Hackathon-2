import sys
import os
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

def test_initialization():
    try:
        from src.ui.premium_todo_app import PremiumTodoApp
        
        # Mock TaskService
        task_service = MagicMock()
        task_service.get_all_tasks.return_value = []
        
        app = PremiumTodoApp(task_service)
        
        # Verify defensive attributes
        if getattr(app, 'priority_filter', None) == 'All':
            print("SUCCESS: priority_filter initialized correctly.")
        else:
            print("FAILURE: priority_filter missing or incorrect.")
            
        # Verify method existence
        if hasattr(app, 'apply_filters'):
             print("SUCCESS: apply_filters method exists.")
             
        # Mock load tasks call to ensure no crash in logic
        try:
             app.apply_filters([])
             print("SUCCESS: apply_filters execution successful (empty list).")
        except Exception as e:
             print(f"FAILURE: apply_filters crashed: {e}")

    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    test_initialization()
