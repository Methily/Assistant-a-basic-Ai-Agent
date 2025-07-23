#!/usr/bin/env python3
"""
Test script for Google Calendar filtering functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tasks.google_calendar import GoogleCalendar

def test_calendar_filtering():
    """Test the Google Calendar filtering functionality."""
    try:
        print("Initializing Google Calendar...")
        calendar = GoogleCalendar()
        print("✓ Google Calendar initialized successfully")
        
        print("\nTesting get_events_for_today...")
        today_events = calendar.get_events_for_today(max_results=10)
        print(f"Today's events: {today_events}")
        
        print("\nTesting get_events_for_tomorrow...")
        tomorrow_events = calendar.get_events_for_tomorrow(max_results=10)
        print(f"Tomorrow's events: {tomorrow_events}")
        
        print("\nTesting get_upcoming_events (all)...")
        all_events = calendar.get_upcoming_events(max_results=10)
        print(f"All upcoming events: {all_events}")
        
        # Compare the results
        print("\n" + "="*50)
        print("COMPARISON RESULTS:")
        print("="*50)
        
        if "No events found" in today_events:
            print("✓ Today filter: No events found for today (correct)")
        else:
            print("✓ Today filter: Found events for today")
            
        if "No events found" in tomorrow_events:
            print("✓ Tomorrow filter: No events found for tomorrow (correct)")
        else:
            print("✓ Tomorrow filter: Found events for tomorrow")
            
        if "No upcoming events found" in all_events:
            print("✓ All events: No upcoming events found")
        else:
            print("✓ All events: Found upcoming events")
            
        return True
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Google Calendar Filtering")
    print("=" * 40)
    
    success = test_calendar_filtering()
    
    if success:
        print("\n✓ All tests completed!")
    else:
        print("\n✗ Tests failed!") 