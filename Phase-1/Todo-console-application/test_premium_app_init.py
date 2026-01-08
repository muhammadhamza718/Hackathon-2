
import sys
import os
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

try:
    # Mock TaskService
    task_service_mock = MagicMock()
    
    # Import PremiumTodoApp
    from src.ui.premium_todo_app import PremiumTodoApp
    
    # Try to instantiate
    app = PremiumTodoApp(task_service_mock)
    
    # Check that it initialized generally (we aren't checking for priority_filter anymore)
    print("Success: PremiumTodoApp instantiated successfully.")
    
    if hasattr(app, 'priority_filter'):
        print("Note: priority_filter still exists (unexpected for Phase 1 basic).")
    else:
        print("Verified: priority_filter correctly removed.")

except ImportError as e:
    import traceback
    traceback.print_exc()
    print(f"Import failed: {e}")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"An error occurred: {e}")
