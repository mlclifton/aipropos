This project is a Text-based User Interface (TUI) utility that allows users to generate Linux shell commands using natural language. It leverages an LLM (Large Language Model) to interpret user requests and provide corresponding commands and explanations.

## Purpose

The purpose of this solution, as described in `spec.md`, is to provide a command-line utility that:
- Presents a text box for natural language input.
- Calls an LLM API to get specific Linux commands.
- Displays the generated commands and their explanations in separate text areas.
- Copies the selected commands to the clipboard upon pressing Enter.
- Is written in Python using the Textual framework.

## How the Solution Works

The solution consists of two main Python components: `main.py` which implements the TUI using Textual, and `llm_service.py` which handles the interaction with the LLM.

### Main Components and Source Files

*   **`main.py`**: This file contains the `TUIApp` class, which is the core of the Textual application.
    *   It sets up the TUI layout with input and output text areas using `textual.widgets.Input`, `textual.widgets.TextArea`, and `textual.containers.Container`.
    *   It handles user input, specifically the "Enter" key press in the command input area, to trigger the LLM call.
    *   It displays the commands and explanations received from the `LLMService`.
    *   It provides key bindings for quitting the application (`q`) and copying commands to the clipboard (`c`).
    *   It uses `pyperclip` for clipboard operations.

*   **`llm_service.py`**: This file defines the `LLMService` class, responsible for interacting with the Large Language Model.
    *   It loads the Ollama API URL and model name from environment variables using `dotenv`.
    *   The `get_commands` method now makes an actual API call to the configured Ollama instance, sending the user's natural language query and a system prompt. It then parses the Ollama's response to extract the generated commands and their explanations, handling various error conditions.

*   **`tui_app.css`**: This CSS file styles the Textual application, defining the appearance of containers and text areas.

### Mermaid Diagrams

#### File Associations

```mermaid
graph TD
    A[main.py] --> B[llm_service.py]
    A --> C[tui_app.css]
    A --> D[pyperclip]
    B --> E[os]
    B --> F[dotenv]
    B --> G[ollama]
```

#### Class Associations

```mermaid
classDiagram
    TUIApp "1" *-- "1" LLMService
    TUIApp --|> App
    LLMService --|> object
```

#### Package Associations

```mermaid
graph TD
    A[textual] --> B[main.py]
    C[pyperclip] --> B
    D[dotenv] --> E[llm_service.py]
    F[os] --> E
    G[ollama] --> E
```