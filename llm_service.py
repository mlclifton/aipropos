import os
import json
from dotenv import load_dotenv
import ollama

load_dotenv()

class LLMService:
    def __init__(self, system_prompt: str):
        self.ollama_api_base_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")
        self.ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "gemma3:4b")
        self.system_prompt = system_prompt

    @staticmethod
    def load_prompts(filepath: str) -> dict:
        prompts = {}
        current_profile = None
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_profile = line[1:-1]
                    prompts[current_profile] = ""
                elif current_profile and line:
                    prompts[current_profile] += line + "\n"
        
        for profile, prompt in prompts.items():
            prompts[profile] = prompts[profile].strip()

        if 'default' not in prompts:
            raise ValueError("The '[default]' profile is missing from the prompts file.")
            
        return prompts

    def get_commands(self, prompt: str) -> tuple[dict | None, str, str, str]:
        try:
            client = ollama.Client(host=self.ollama_api_base_url)
            messages_payload = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]

            response = client.chat(
                model=self.ollama_model_name,
                messages=messages_payload,
                stream=False
            )

            content = response["message"]["content"].strip()
            diagnostic_message = f"Sent: {messages_payload}"

            try:
                # Find the start and end of the JSON object
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = content[json_start:json_end]
                    parsed_json = json.loads(json_str)
                    return parsed_json, "", diagnostic_message, content
                else:
                    return None, f"No JSON object found in the response: {content}", diagnostic_message, content
            except json.JSONDecodeError:
                return None, f"Failed to decode JSON from response: {content}", diagnostic_message, content

        except ollama.ResponseError as e:
            return None, f"Ollama API Error: {e.status_code} - {str(e)}", f"Sent: {messages_payload}", ""
        except Exception as e:
            return None, f"Error communicating with Ollama: {e}", f"Sent: {messages_payload}", ""