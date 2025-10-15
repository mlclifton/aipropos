import os
from dotenv import load_dotenv
import ollama

load_dotenv()

class LLMService:
    def __init__(self):
        self.ollama_api_base_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")
        self.ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "llama2")
        self.system_prompt = (
            "You are an expert Linux development assistant. "
            "When a user asks for a command, provide only the command itself, "
            "followed by a clear and concise explanation on a new line. "
            "Do not include any conversational filler or extra text. "
            "Format your response as: \n```bash\n<command>\n```\n<explanation>"
        )

    def get_commands(self, prompt: str) -> tuple[str, str]:
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
            
            # Attempt to parse the command and explanation
            if content.startswith("```bash") and "```" in content:
                parts = content.split("```")
                if len(parts) >= 3:
                    command_block = parts[1].strip()
                    # Extract the command by splitting the block and taking the second line
                    command_lines = command_block.split('\n')
                    if len(command_lines) > 1:
                        command = command_lines[1].strip()
                    else:
                        command = command_block.strip() # Fallback if only one line
                    explanation = parts[2].strip()
                    return command, explanation, diagnostic_message, content
                else:
                    return "", f"Ollama response format unexpected: {content}", diagnostic_message, content
            else:
                # Fallback if the format is not as expected
                return "", f"Ollama response format unexpected: {content}", diagnostic_message, content

        except ollama.ResponseError as e:
            return "", f"Ollama API Error: {e.status_code} - {str(e)}", f"Sent: {messages_payload}", ""
        except Exception as e:
            return "", f"Error communicating with Ollama: {e}", f"Sent: {messages_payload}", ""
