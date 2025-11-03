import unittest
from unittest.mock import patch, MagicMock
import os
import ollama
from llm_service import LLMService
import json

class TestLLMService(unittest.TestCase):

    def setUp(self):
        # Create a dummy prompts file for testing
        self.prompts_filepath = "test_prompts.txt"
        with open(self.prompts_filepath, "w") as f:
            f.write("[default]\nDefault prompt\n\n[git]\nGit prompt\n")

    def tearDown(self):
        # Clean up the dummy prompts file
        if os.path.exists(self.prompts_filepath):
            os.remove(self.prompts_filepath)

    def test_load_prompts_success(self):
        prompts = LLMService.load_prompts(self.prompts_filepath)
        self.assertEqual(prompts, {"default": "Default prompt", "git": "Git prompt"})

    def test_load_prompts_no_default(self):
        # Create a prompts file without a default profile
        with open(self.prompts_filepath, "w") as f:
            f.write("[git]\nGit prompt\n")
        with self.assertRaises(ValueError):
            LLMService.load_prompts(self.prompts_filepath)

    @patch.dict(os.environ, {'OLLAMA_API_BASE_URL': 'http://localhost:11434', 'OLLAMA_MODEL_NAME': 'test_model'})
    @patch('ollama.Client')
    def test_get_commands_uses_custom_prompt(self, mock_ollama_client):
        # Arrange
        mock_chat_response = {
            "message": {
                "content": json.dumps({
                    "request": "test request",
                    "commands": ["test command"],
                    "explanation": "test explanation"
                })
            }
        }
        mock_client_instance = MagicMock()
        mock_client_instance.chat.return_value = mock_chat_response
        mock_ollama_client.return_value = mock_client_instance

        custom_prompt = "This is a custom system prompt."
        llm_service = LLMService(system_prompt=custom_prompt)
        
        # Act
        llm_service.get_commands("some user query")

        # Assert
        mock_ollama_client.assert_called_once_with(host='http://localhost:11434')
        mock_client_instance.chat.assert_called_once()
        called_messages = mock_client_instance.chat.call_args[1]['messages']
        self.assertEqual(len(called_messages), 2)
        self.assertEqual(called_messages[0]['role'], 'system')
        self.assertEqual(called_messages[0]['content'], custom_prompt)
        self.assertEqual(called_messages[1]['role'], 'user')
        self.assertEqual(called_messages[1]['content'], "some user query")

if __name__ == '__main__':
    unittest.main()
