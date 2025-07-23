import requests
import json
import config

class LlamaClient:
    def __init__(self):
        """Initialize the Llama client."""
        self.server_url = config.LLAMA_SERVER_URL
        self.command_patterns = config.COMMAND_PATTERNS

    def _create_prompt(self, user_input):
        """
        Create a structured prompt for the LLM.
        Includes context about available commands and their patterns.
        """
        prompt = f"""You are Jarvis, a privacy-focused voice assistant. Analyze the following user input and determine the appropriate action.
Available commands:
- Calendar (for scheduling meetings and events): {', '.join(self.command_patterns['calendar'])}
- Notion (for creating notes and tasks): {', '.join(self.command_patterns['notion'])}
- Email (for managing emails): {', '.join(self.command_patterns['email'])}

User input: {user_input}

Respond in JSON format with the following structure:
{{
    "action": "calendar|notion|email|general",
    "intent": "create|read|update|delete",
    "parameters": {{
        "summary": "Event title",
        "start_time": "Event start time",
        "end_time": "Event end time",
        "description": "Event description",
        "attendees": ["email1", "email2"]
    }},
    "response": "Your natural language response to the user"
}}

Only include parameters that are relevant to the action.
"""
        return prompt

    def process_command(self, user_input):
        """
        Process user input through the local llama.cpp server.
        Returns a structured response with action and parameters.
        """
        try:
            prompt = self._create_prompt(user_input)
            
            response = requests.post(
                self.server_url,
                json={
                    "prompt": prompt,
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "stop": ["User input:", "\n\n"]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', '')
                
                # Default response structure
                response_dict = {
                    "action": "general",
                    "intent": "create",
                    "parameters": {},
                    "response": content
                }
                
                # Try to extract JSON from the response
                try:
                    # First try to find JSON in the content
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    
                    if json_start != -1 and json_end != 0:
                        json_str = content[json_start:json_end]
                        parsed = json.loads(json_str)
                        # Ensure all required keys are present
                        response_dict.update(parsed)
                        return response_dict
                    
                    # If no JSON found, try to parse the content as a structured response
                    content_lower = content.lower()
                    
                    # Check for calendar-related keywords first
                    if any(word in content_lower for word in ['schedule', 'meeting', 'event', 'appointment', 'calendar']):
                        response_dict["action"] = "calendar"
                        response_dict["intent"] = "create"
                        response_dict["parameters"] = {
                            "summary": "Meeting",  # Default title
                            "start_time": None,
                            "end_time": None
                        }
                        
                        # Extract time information
                        if "tomorrow" in content_lower:
                            response_dict["parameters"]["start_time"] = "tomorrow"
                        if "2:00 p.m." in content_lower or "2 pm" in content_lower:
                            response_dict["parameters"]["start_time"] = "14:00"
                            
                    # Then check for notion-related keywords
                    elif any(word in content_lower for word in ['note', 'todo', 'task', 'reminder']):
                        response_dict["action"] = "notion"
                        response_dict["intent"] = "create"
                        response_dict["parameters"] = {
                            "title": "New Task",  # Default title
                            "type": "todo"
                        }
                        
                    # Finally check for email-related keywords
                    elif any(word in content_lower for word in ['email', 'mail', 'inbox']):
                        response_dict["action"] = "email"
                        response_dict["intent"] = "create"
                    
                    return response_dict
                    
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error parsing LLM response: {e}")
                    print(f"Raw response: {result}")
                    return response_dict  # Return the default response structure
            else:
                print(f"Error from llama.cpp server: {response.status_code}")
                print(f"Response content: {response.text}")
                return {
                    "action": "general",
                    "intent": "error",
                    "parameters": {},
                    "response": "I'm having trouble processing your request. Please try again."
                }
                
        except Exception as e:
            print(f"Error communicating with llama.cpp server: {e}")
            return {
                "action": "general",
                "intent": "error",
                "parameters": {},
                "response": "I'm having trouble connecting to my brain. Please try again."
            }

if __name__ == "__main__":
    # Test LLM processing
    client = LlamaClient()
    test_input = "Schedule a meeting with John tomorrow at 2 PM"
    result = client.process_command(test_input)
    print(f"Test result: {json.dumps(result, indent=2)}") 