import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from src.services.task_service import TaskService
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
except NameError as e:
    print(f"NameError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
