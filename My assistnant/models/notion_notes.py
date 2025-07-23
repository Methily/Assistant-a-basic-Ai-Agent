from notion_client import Client
import config
from datetime import datetime

class NotionClient:
    def __init__(self):
        """Initialize Notion client with API key."""
        self.notion = Client(auth=config.get_notion_client())
        self.database_id = config.NOTION_DATABASE_ID

    def create_note(self, title, content, tags=None):
        """
        Create a new note in Notion.
        
        Args:
            title (str): Note title
            content (str): Note content
            tags (list, optional): List of tags
        """
        try:
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }

            if tags:
                properties["Tags"] = {
                    "multi_select": [{"name": tag} for tag in tags]
                }

            page = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": content
                                    }
                                }
                            ]
                        }
                    }
                ]
            )
            return f"Note created successfully: {page['url']}"
        except Exception as e:
            return f"Error creating note: {str(e)}"

    def create_todo(self, title, due_date=None, priority=None):
        """
        Create a new todo item in Notion.
        
        Args:
            title (str): Todo title
            due_date (str, optional): Due date in ISO format
            priority (str, optional): Priority level (High, Medium, Low)
        """
        try:
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "To Do"
                    }
                }
            }

            if due_date:
                properties["Due Date"] = {
                    "date": {
                        "start": due_date
                    }
                }

            if priority:
                properties["Priority"] = {
                    "select": {
                        "name": priority
                    }
                }

            page = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            return f"Todo created successfully: {page['url']}"
        except Exception as e:
            return f"Error creating todo: {str(e)}"

    def get_recent_notes(self, limit=5):
        """
        Get recent notes from Notion.
        
        Args:
            limit (int): Maximum number of notes to return
        """
        try:
            response = self.notion.databases.query(
                database_id=self.database_id,
                page_size=limit,
                sorts=[
                    {
                        "property": "Date",
                        "direction": "descending"
                    }
                ]
            )

            notes = []
            for page in response["results"]:
                title = page["properties"]["Name"]["title"][0]["text"]["content"]
                date = page["properties"]["Date"]["date"]["start"]
                notes.append(f"{date}: {title}")

            return "\n".join(notes) if notes else "No recent notes found."
        except Exception as e:
            return f"Error fetching notes: {str(e)}"

if __name__ == "__main__":
    # Test Notion integration
    notion = NotionClient()
    
    # Test creating a note
    result = notion.create_note(
        "Test Note",
        "This is a test note content",
        ["test", "example"]
    )
    print(result)
    
    # Test creating a todo
    result = notion.create_todo(
        "Test Todo",
        due_date="2024-12-31",
        priority="High"
    )
    print(result)
    
    # Test getting recent notes
    notes = notion.get_recent_notes()
    print("\nRecent notes:")
    print(notes) 