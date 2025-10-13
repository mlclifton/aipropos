import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        # In a real application, you would initialize your LLM client here

    def get_commands(self, prompt: str) -> tuple[str, str]:
        # This is a placeholder for actual LLM API call
        # In a real scenario, you would call your LLM here and parse its response
        if "list files" in prompt.lower():
            return "ls -l", "Lists files in the current directory in a long format." 
        elif "create directory" in prompt.lower():
            return "mkdir new_dir", "Creates a new directory named 'new_dir'."
        else:
            return "echo 'No command found for your request.'", "Please try a different request."
