#!/usr/bin/env python3
"""
Test script for Google Calendar functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tasks.google_calendar import GoogleCalendar

def test_calendar():
    """Test the Google Calendar functionality."""
    try:
        print("Initializing Google Calendar...")
        calendar = GoogleCalendar()
        print("✓ Google Calendar initialized successfully")
        
        print("\nTesting get_upcoming_events...")
        events = calendar.get_upcoming_events(max_results=5)
        print(f"Events result: {events}")
        
        if "Error" in events:
            print("✗ Error fetching events")
            return False
        else:
            print("✓ Successfully fetched events")
            return True
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Google Calendar Integration")
    print("=" * 40)
    
    success = test_calendar()
    
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Tests failed!") 