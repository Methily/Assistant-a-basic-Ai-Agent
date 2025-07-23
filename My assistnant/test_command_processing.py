#!/usr/bin/env python3
"""
Test script for command processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tasks.agent_router import handle_input

def test_commands():
    """Test various commands to ensure they're processed correctly."""
    
    test_commands = [
        "check if there are any events for tomorrow",
        "what events do I have tomorrow",
        "show my calendar for tomorrow",
        "list events for today",
        "what's on my schedule today",
        "check my calendar",
        "show upcoming events",
        "what events do I have today",
        "show events for tomorrow",
        "check tomorrow's schedule"
    ]
    
    print("Testing Command Processing")
    print("=" * 40)
    
    for command in test_commands:
        print(f"\nTesting command: '{command}'")
        try:
            response = handle_input(command)
            print(f"Response: {response}")
            
            # Check if it's a proper calendar response
            if "Sorry, I didn't understand" in response:
                print("✗ Command not recognized as calendar command")
            elif "Error" in response:
                print("✗ Error in calendar processing")
            elif "tomorrow" in command and "tomorrow" in response:
                print("✓ Tomorrow command processed correctly")
            elif "today" in command and "today" in response:
                print("✓ Today command processed correctly")
            else:
                print("✓ Command processed successfully")
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")

if __name__ == "__main__":
    test_commands() 