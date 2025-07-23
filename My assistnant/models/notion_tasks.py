from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID

class NotionTasks:
    def __init__(self):
        self.client = Client(auth=NOTION_API_KEY)
        self.database_id = NOTION_DATABASE_ID

    def create_task(self, title, description=None, due_date=None):
        """Create a new task in Notion."""
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
                }
            }

            if due_date:
                properties["Due Date"] = {
                    "date": {
                        "start": due_date.isoformat()
                    }
                }

            page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )

            if description:
                self.client.blocks.children.append(
                    block_id=page["id"],
                    children=[
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": description
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                )

            return page
        except Exception as e:
            print(f"Error creating Notion task: {str(e)}")
            return None

    def get_tasks(self, filter_status=None):
        """Get tasks from Notion database."""
        try:
            query = {
                "database_id": self.database_id,
                "sorts": [
                    {
                        "property": "Due Date",
                        "direction": "ascending"
                    }
                ]
            }

            if filter_status:
                query["filter"] = {
                    "property": "Status",
                    "select": {
                        "equals": filter_status
                    }
                }

            response = self.client.databases.query(**query)
            return response["results"]
        except Exception as e:
            print(f"Error getting Notion tasks: {str(e)}")
            return [] 