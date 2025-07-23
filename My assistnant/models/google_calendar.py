from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json
from datetime import datetime, timedelta
import pytz
from config import GOOGLE_CREDENTIALS_PATH, GOOGLE_TOKEN_PATH, GOOGLE_SCOPES

class GoogleCalendar:
    def __init__(self):
        """Initialize Google Calendar client."""
        self.creds = None
        self.service = None
        self._authenticate()
        self.timezone = pytz.timezone('UTC')  # Default timezone

    def _authenticate(self):
        """Handle OAuth2 authentication for Google Calendar."""
        if os.path.exists(GOOGLE_TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_info(
                json.loads(open(GOOGLE_TOKEN_PATH).read()), GOOGLE_SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CREDENTIALS_PATH, GOOGLE_SCOPES
                )
                # Try different ports if 8080 is not available
                ports = [8080, 8081, 8082, 8083]
                for port in ports:
                    try:
                        self.creds = flow.run_local_server(port=port)
                        print(f"Successfully authenticated using port {port}")
                        break
                    except OSError as e:
                        if "Only one usage of each socket address" in str(e):
                            print(f"Port {port} is in use, trying next port...")
                            continue
                        raise e

            # Save the credentials for the next run
            os.makedirs(os.path.dirname(GOOGLE_TOKEN_PATH), exist_ok=True)
            with open(GOOGLE_TOKEN_PATH, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, summary, start_time, end_time, description=None, attendees=None):
        """
        Create a new calendar event.
        
        Args:
            summary (str): Event title
            start_time (datetime): Event start time
            end_time (datetime): Event end time
            description (str, optional): Event description
            attendees (list, optional): List of attendee email addresses
        """
        # Ensure times are timezone-aware
        if start_time.tzinfo is None:
            start_time = self.timezone.localize(start_time)
        if end_time.tzinfo is None:
            end_time = self.timezone.localize(end_time)

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': str(self.timezone),
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': str(self.timezone),
            },
        }

        if description:
            event['description'] = description

        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            
            # Format the time for user-friendly message
            start_time_str = start_time.strftime('%I:%M %p')
            date_str = start_time.strftime('%B %d')
            
            # Create user-friendly message
            message = f"The event '{summary}' has been created for {date_str} at {start_time_str}"
            
            # Add attendees info if any
            if attendees:
                message += f" with {', '.join(attendees)}"
            
            message += "."
            
            return message
        except Exception as e:
            return f"Error creating event: {str(e)}"

    def get_upcoming_events(self, max_results=10, start_date=None, end_date=None):
        """
        Get upcoming calendar events.
        
        Args:
            max_results (int): Maximum number of events to return
            start_date (datetime, optional): Start date for filtering events
            end_date (datetime, optional): End date for filtering events
        """
        try:
            # Set time range for filtering
            if start_date and end_date:
                # Filter events between specific dates
                time_min = start_date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
                time_max = end_date.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()
            else:
                # Get events from now onwards
                time_min = datetime.now(self.timezone).isoformat()
                time_max = None
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            if not events:
                if start_date and end_date:
                    date_str = start_date.strftime('%B %d')
                    if start_date.date() == end_date.date():
                        return f"No events found for {date_str}."
                    else:
                        return f"No events found between {start_date.strftime('%B %d')} and {end_date.strftime('%B %d')}."
                else:
                    return "No upcoming events found."
            
            event_list = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if 'dateTime' in event['start']:
                    # Convert to local timezone
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    start_dt = start_dt.astimezone(self.timezone)
                    start = start_dt.strftime('%Y-%m-%d %H:%M')
                event_list.append(f"{start}: {event['summary']}")
            
            return "\n".join(event_list)
        except Exception as e:
            return f"Error fetching events: {str(e)}"

    def get_events_for_today(self, max_results=10):
        """
        Get events for today only.
        
        Args:
            max_results (int): Maximum number of events to return
        """
        today = datetime.now(self.timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        return self.get_upcoming_events(max_results=max_results, start_date=today, end_date=tomorrow)

    def get_events_for_tomorrow(self, max_results=10):
        """
        Get events for tomorrow only.
        
        Args:
            max_results (int): Maximum number of events to return
        """
        tomorrow = datetime.now(self.timezone).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        day_after_tomorrow = tomorrow + timedelta(days=1)
        return self.get_upcoming_events(max_results=max_results, start_date=tomorrow, end_date=day_after_tomorrow)

    def get_events_for_week(self, max_results=30):
        """
        Get events for this week (next 7 days).
        
        Args:
            max_results (int): Maximum number of events to return
        """
        today = datetime.now(self.timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        week_later = today + timedelta(days=7)
        return self.get_upcoming_events(max_results=max_results, start_date=today, end_date=week_later)

    def get_events_for_month(self, max_results=100):
        """
        Get events for this month.
        
        Args:
            max_results (int): Maximum number of events to return
        """
        today = datetime.now(self.timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        month_later = today + timedelta(days=30)
        return self.get_upcoming_events(max_results=max_results, start_date=today, end_date=month_later)

    def delete_event(self, event_title):
        """
        Delete an event by its title.
        
        Args:
            event_title (str): Title of the event to delete
        """
        try:
            # First, find the event
            now = datetime.now(self.timezone).isoformat()
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            event_to_delete = None
            
            for event in events:
                if event['summary'].lower() == event_title.lower():
                    event_to_delete = event
                    break
            
            if not event_to_delete:
                return f"No event found with title: {event_title}"
            
            # Delete the event
            self.service.events().delete(
                calendarId='primary',
                eventId=event_to_delete['id']
            ).execute()
            
            return f"Successfully deleted event: {event_title}"
        except Exception as e:
            return f"Error deleting event: {str(e)}"

    def update_event(self, event_title, new_summary=None, new_start_time=None, new_end_time=None, new_description=None):
        """
        Update an existing event.
        
        Args:
            event_title (str): Title of the event to update
            new_summary (str, optional): New title for the event
            new_start_time (datetime, optional): New start time
            new_end_time (datetime, optional): New end time
            new_description (str, optional): New description
        """
        try:
            # First, find the event
            now = datetime.now(self.timezone).isoformat()
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            event_to_update = None
            
            for event in events:
                if event['summary'].lower() == event_title.lower():
                    event_to_update = event
                    break
            
            if not event_to_update:
                return f"No event found with title: {event_title}"
            
            # Update the event
            if new_summary:
                event_to_update['summary'] = new_summary
            if new_start_time:
                if new_start_time.tzinfo is None:
                    new_start_time = self.timezone.localize(new_start_time)
                event_to_update['start'] = {
                    'dateTime': new_start_time.isoformat(),
                    'timeZone': str(self.timezone)
                }
            if new_end_time:
                if new_end_time.tzinfo is None:
                    new_end_time = self.timezone.localize(new_end_time)
                event_to_update['end'] = {
                    'dateTime': new_end_time.isoformat(),
                    'timeZone': str(self.timezone)
                }
            if new_description:
                event_to_update['description'] = new_description
            
            # Save the updated event
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_to_update['id'],
                body=event_to_update
            ).execute()
            
            return f"Successfully updated event: {updated_event.get('summary')}"
        except Exception as e:
            return f"Error updating event: {str(e)}"

if __name__ == "__main__":
    # Test Google Calendar integration
    calendar = GoogleCalendar()
    
    # Test creating an event
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    result = calendar.create_event(
        "Test Meeting",
        start_time,
        end_time,
        "This is a test meeting",
        ["test@example.com"]
    )
    print(result)
    
    # Test getting upcoming events
    events = calendar.get_upcoming_events()
    print("\nUpcoming events:")
    print(events) 