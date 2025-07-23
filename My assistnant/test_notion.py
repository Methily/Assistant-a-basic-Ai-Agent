from tasks.notion_notes import NotionClient
from tasks.notion_tasks import NotionTasks
from datetime import datetime
import os
from dotenv import load_dotenv

def verify_env_variables():
    """Verify that required environment variables are set."""
    load_dotenv()  # Load environment variables from .env file
    
    required_vars = ['NOTION_API_KEY', 'NOTION_DATABASE_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please make sure your .env file contains these variables.")
        return False
    return True

def test_notion():
    try:
        # First verify environment variables
        if not verify_env_variables():
            return
        
        print("\n=== Testing Notion Notes ===")
        # Initialize Notion client
        notion_notes = NotionClient()
        
        # Test 1: Create a note
        print("\nTest 1: Creating a note...")
        result = notion_notes.create_note(
            "Test Note",
            "This is a test note created by the assistant",
            ["test", "api"]
        )
        print(f"Result: {result}")
        
        # Test 2: Create a todo
        print("\nTest 2: Creating a todo...")
        result = notion_notes.create_todo(
            "Test Todo",
            due_date=datetime.now().isoformat(),
            priority="High"
        )
        print(f"Result: {result}")
        
        # Test 3: Get recent notes
        print("\nTest 3: Getting recent notes...")
        notes = notion_notes.get_recent_notes(limit=3)
        print(f"Recent notes:\n{notes}")
        
        print("\n=== Testing Notion Tasks ===")
        # Initialize Notion tasks
        notion_tasks = NotionTasks()
        
        # Test 4: Create a task
        print("\nTest 4: Creating a task...")
        result = notion_tasks.create_task(
            "Test Task",
            "This is a test task",
            "High"
        )
        print(f"Result: {result}")
        
        # Test 5: Get tasks
        print("\nTest 5: Getting tasks...")
        tasks = notion_tasks.get_tasks()
        print(f"Tasks:\n{tasks}")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your .env file exists and contains NOTION_API_KEY and NOTION_DATABASE_ID")
        print("2. Verify that your Notion API key is valid")
        print("3. Make sure your database ID is correct")
        print("4. Ensure your integration has access to the database")
        print("5. Check if your database has the required properties (Name, Date, Tags, Status, Priority)")

if __name__ == "__main__":
    test_notion() 