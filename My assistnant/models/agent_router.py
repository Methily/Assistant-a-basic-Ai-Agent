from .google_calendar import GoogleCalendar
from .gmail import GmailClient
from .notion_notes import NotionClient
from .notion_tasks import NotionTasks
import re
from datetime import datetime, timedelta
import dateutil.parser

def parse_datetime(text):
    """Parse date and time from natural language text."""
    try:
        return dateutil.parser.parse(text)
    except:
        return None

def extract_attendees(text):
    """Extract email addresses from text."""
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    return re.findall(email_pattern, text)

def handle_calendar_command(command):
    """Handle calendar-related commands."""
    calendar = GoogleCalendar()
    
    # Check for events or view calendar
    if any(word in command for word in ["check", "show", "list", "what", "when", "see", "view", "display"]):
        # Check for specific time periods
        if "tomorrow" in command:
            events = calendar.get_events_for_tomorrow(max_results=10)
            if "No events found" in events:
                return "You have no events scheduled for tomorrow."
            else:
                return f"Here are your events for tomorrow:\n{events}"
        elif "today" in command:
            events = calendar.get_events_for_today(max_results=10)
            if "No events found" in events:
                return "You have no events scheduled for today."
            else:
                return f"Here are your events for today:\n{events}"
        elif "week" in command:
            events = calendar.get_events_for_week(max_results=30)
            if "No events found" in events:
                return "You have no events scheduled for this week."
            else:
                return f"Here are your events for this week:\n{events}"
        elif "month" in command:
            events = calendar.get_events_for_month(max_results=100)
            if "No events found" in events:
                return "You have no events scheduled for this month."
            else:
                return f"Here are your events for this month:\n{events}"
        else:
            # Default to showing upcoming events
            events = calendar.get_upcoming_events(max_results=5)
            if "No upcoming events found" in events:
                return "You have no upcoming events scheduled."
            else:
                return f"Here are your upcoming events:\n{events}"
    
    # Create event
    elif any(word in command for word in ["schedule", "create", "add", "set up", "book"]):
        # Extract date and time
        date_match = re.search(r'(?:on|for|at)\s+([^,]+)', command)
        time_match = re.search(r'at\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)', command)
        
        # Extract title
        title_match = re.search(r'(?:schedule|create|add|set up|book)\s+(?:a|an)?\s+([^,]+)', command)
        title = title_match.group(1) if title_match else "New Event"
        
        # Extract attendees
        attendees = extract_attendees(command)
        
        # Set default times if not specified
        start_time = datetime.now() + timedelta(days=1)
        if date_match:
            date_str = date_match.group(1)
            try:
                start_time = parse_datetime(date_str)
                if start_time is None:
                    start_time = datetime.now() + timedelta(days=1)
            except:
                start_time = datetime.now() + timedelta(days=1)
        
        if time_match:
            time_str = time_match.group(1)
            if time_str:
                try:
                    # Parse time (e.g., "3:00 PM" or "3 PM")
                    if ":" in time_str:
                        time_parts = time_str.split(":")
                        hour = int(time_parts[0])
                        minute = int(time_parts[1].split()[0])
                    else:
                        hour = int(time_str.split()[0])
                        minute = 0
                    
                    # Handle AM/PM
                    if "PM" in time_str.upper() and hour != 12:
                        hour += 12
                    elif "AM" in time_str.upper() and hour == 12:
                        hour = 0
                    
                    start_time = start_time.replace(hour=hour, minute=minute)
                except:
                    pass  # Keep default time if parsing fails
        
        end_time = start_time + timedelta(hours=1)
        
        return calendar.create_event(
            title,
            start_time,
            end_time,
            "Created by Jarvis",
            attendees
        )
    
    # Delete event
    elif any(word in command for word in ["delete", "remove", "cancel"]):
        # Extract event title
        title_match = re.search(r'(?:delete|remove|cancel)\s+(?:the)?\s+([^,]+)', command)
        if title_match:
            title = title_match.group(1)
            return calendar.delete_event(title)
        return "Please specify which event to delete."
    
    else:
        return "I can help you check your calendar, schedule events, or delete events. What would you like to do?"

def handle_input(user_command):
    user_command = user_command.lower()
    calendar = GoogleCalendar()  # Create calendar instance
    gmail = GmailClient()  # Create Gmail instance
    notion_notes = NotionClient()  # Create Notion notes instance
    notion_tasks = NotionTasks()  # Create Notion tasks instance

    # Check for calendar-related commands (expanded keywords)
    calendar_keywords = ["calendar", "schedule", "event", "events", "meeting", "appointment", "tomorrow", "today", "week", "month"]
    if any(keyword in user_command for keyword in calendar_keywords):
        return handle_calendar_command(user_command)

    elif "email" in user_command or "gmail" in user_command:
        return gmail.send_email("bob@example.com", "Quick check-in", "Hey Bob, are you free to sync up tomorrow?")

    elif "note" in user_command:
        return notion_notes.create_note("Project Summary", "Discussed architecture and tasks.")
    
    elif "task" in user_command:
        return notion_tasks.create_task("New Task", "Task description", "High")

    elif "notion" in user_command:
        # Handle general Notion commands
        if "list" in user_command:
            if "tasks" in user_command:
                return notion_tasks.get_tasks()
            else:
                return notion_notes.get_recent_notes()
        elif "create" in user_command:
            if "task" in user_command:
                return notion_tasks.create_task("New Task", "Task description", "High")
            else:
                return notion_notes.create_note("New Note", "Note content")

    else:
        return "Sorry, I didn't understand that command."
