import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.database import create_db_and_tables
from src.models.conversation import Conversation
from src.models.message import Message
from models.task import Task
from models.user import User

if __name__ == "__main__":
    print("Running synchronous database initialization...")
    try:
        create_db_and_tables()
        print("Successfully created database tables.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        import traceback
        traceback.print_exc()
