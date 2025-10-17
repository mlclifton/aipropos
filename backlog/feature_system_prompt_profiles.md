# Task List: Implement System Prompt Profiles

This task list outlines the steps to implement the "System Prompt Profiles" feature, allowing users to select a system prompt via a command-line argument.

- [ ] **1. Create `prompts.txt` Configuration File**
    - In the project root, create a new file named `prompts.txt`.
    - Add a `[default]` profile for general Linux commands.
    - Add a `[git]` profile for Git-related queries.
    - Add a `[linux]` profile for linux commands.

- [ ] **2. Implement Prompt Loading in `llm_service.py`**
    - Create a new static method `load_prompts(filepath: str) -> dict` in the `LLMService` class.
    - This method will read the `prompts.txt` file.
    - It should parse the file content into a dictionary mapping profile names (e.g., "default", "git") to their corresponding prompt text.
    - The parser should handle the `[profile_name]` syntax.
    - It should raise an error if the `[default]` profile is missing.

- [ ] **3. Modify `LLMService` to Accept a System Prompt**
    - Update the `LLMService.__init__` method to accept a `system_prompt` string as an argument.
    - Store this `system_prompt` as an instance variable (e.g., `self.system_prompt`).
    - In the `get_commands` method, use `self.system_prompt` when making the call to the LLM API, instead of the previously hardcoded one.

- [ ] **4. Update `main.py` to Handle CLI Arguments and Pass Prompt**
    - In the `if __name__ == "__main__"` block:
        - Use `sys.argv` to get the profile name from the command line. Default to "default" if no argument is given.
        - Call the new `LLMService.load_prompts` method to get all available prompts.
        - Select the correct prompt from the dictionary based on the profile name. Fall back to the default prompt if the name is not found.
    - Modify `TUIApp.__init__` to accept the `system_prompt` string.
    - When instantiating `TUIApp`, pass the selected system prompt to it.
    - Inside `TUIApp.__init__`, pass the received `system_prompt` when creating the `LLMService` instance.

- [ ] **5. Update Tests in `test_llm_service.py`**
    - Create a temporary `prompts.txt` for testing purposes.
    - Add a new test case to verify that `LLMService.load_prompts` correctly parses the test file and returns the expected dictionary.
    - Add a test to ensure `LLMService` uses the custom system prompt provided during its initialization.
