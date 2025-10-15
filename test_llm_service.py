import unittest
from unittest.mock import patch
import os
import ollama
from llm_service import LLMService

class TestLLMService(unittest.TestCase):

    @patch.dict(os.environ, {'OLLAMA_API_BASE_URL': 'http://localhost:11434', 'OLLAMA_MODEL_NAME': 'test_model'})
    def setUp(self):
        self.llm_service = LLMService()

    @patch('ollama.Client')
    def test_get_commands_success(self, mock_ollama_client):
        # Configure the mock client to return a successful response
        mock_instance = mock_ollama_client.return_value
        mock_instance.chat.return_value = {
            "message": {
                "content": "```bash\nls -l\n```\nLists files in the current directory."
            }
        }

        command, explanation = self.llm_service.get_commands("list files")
        self.assertEqual(command, "ls -l")
        self.assertEqual(explanation, "Lists files in the current directory.")
        mock_ollama_client.assert_called_once_with(host='http://localhost:11434')
        mock_instance.chat.assert_called_once()

    @patch('ollama.Client')
    def test_get_commands_api_error(self, mock_ollama_client):
        # Configure the mock client to raise an API error
        mock_instance = mock_ollama_client.return_value
        mock_instance.chat.side_effect = ollama.ResponseError("API Error", 500)

        command, explanation = self.llm_service.get_commands("some query")
        self.assertEqual(command, "")
        self.assertIn("Ollama API Error: 500", explanation)

    @patch('ollama.Client')
    def test_get_commands_unexpected_format(self, mock_ollama_client):
        # Configure the mock client to return an unexpected format
        mock_instance = mock_ollama_client.return_value
        mock_instance.chat.return_value = {
            "message": {
                "content": "This is not the expected format."
            }
        }

        command, explanation = self.llm_service.get_commands("some query")
        self.assertEqual(command, "")
        self.assertIn("Ollama response format unexpected", explanation)

    @patch('ollama.Client')
    def test_get_commands_general_exception(self, mock_ollama_client):
        # Configure the mock client to raise a general exception
        mock_instance = mock_ollama_client.return_value
        mock_instance.chat.side_effect = Exception("Network issue")

        command, explanation = self.llm_service.get_commands("some query")
        self.assertEqual(command, "")
        self.assertIn("Error communicating with Ollama: Network issue", explanation)

if __name__ == '__main__':
    unittest.main()
