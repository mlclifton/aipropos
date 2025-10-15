## Project Tasks

- [X] **Setup Project Structure**
  - [X] Create `main.py` for the Textual application.
  - [X] Create `llm_service.py` for LLM API interaction.
  - [X] Create `requirements.txt` for dependencies (Textual, LLM client library).
  - [X] Create `tui_app.css` for styling.

- [X] **Implement TUI Layout**
  - [X] Design the main Textual app in `main.py`.
  - [X] Add an input text area for user queries.
  - [X] Add a display area for the generated commands.
  - [X] Add a display area for the LLM's explanation.
  - [X] Implement basic layout using Textual widgets (e.g., `Input`, `TextArea`, `Container`).

- [X] **Integrate LLM API**
  - [X] In `llm_service.py`, implement a function to call the LLM API.
  - [X] Define the prompt for the LLM, specifying it as a Linux development expert.
  - [X] Handle API key management (e.g., environment variables).
  - [X] Parse the LLM's response to extract commands and explanations.
  - [X] Integrate `llm_service.py` into `main.py` to send user input and display results.

- [X] **Command Copy to Clipboard**
  - [X] Implement a mechanism to copy the selected command(s) to the clipboard when the user presses Enter in the command display area.
  - [X] Research Textual's capabilities for clipboard interaction or external libraries (e.g., `pyperclip`).

- [X] **Error Handling and Enhancements**
  - [X] Add error handling for LLM API calls (network issues, invalid responses).
  - [X] Provide user feedback for loading states, errors, etc.
  - [X] Consider adding a way to execute commands directly from the TUI (optional, but useful).
  - [X] Refine UI/UX for better usability.
