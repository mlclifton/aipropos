# Copilot Instructions for txtui_play

This document provides essential guidance for AI coding agents working on the `txtui_play` codebase.

## 1. Project Overview

`txtui_play` is a Text-based User Interface (TUI) utility written in Python using the Textual framework. Its primary function is to allow users to generate Linux shell commands from natural language input by interacting with a Large Language Model (LLM).

**Core Components:**
- `main.py`: Implements the TUI using the Textual framework. It handles user input, displays generated commands and explanations, and manages clipboard operations.
- `llm_service.py`: Manages interaction with the LLM. Currently, it contains placeholder logic for `get_commands` and loads the `LLM_API_KEY` from environment variables.
- `tui_app.css`: Defines the styling for the Textual application.

**Data Flow:**
1. User enters a natural language query into the input box in `main.py`.
2. `main.py` calls `llm_service.py`'s `get_commands` method with the user's query.
3. `llm_service.py` (in a real implementation) would interact with an LLM API to get commands and explanations.
4. `llm_service.py` returns the generated commands and explanations to `main.py`.
5. `main.py` displays these in dedicated text areas and allows copying to the clipboard.

## 2. Key Files and Directories

- `main.py`: Main application logic, TUI setup, event handling.
- `llm_service.py`: LLM integration logic (currently a placeholder).
- `tui_app.css`: Textual application styling.
- `requirements.txt`: Project dependencies.
- `solution_arch.md`: High-level architecture description.
- `spec.md`: Product requirements and use cases.

## 3. Developer Workflows

### 3.1 Setup and Installation

To set up the project, ensure you have Python 3.8+ and `pip` installed.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Variables:**
    The `llm_service.py` expects an `LLM_API_KEY` environment variable. Create a `.env` file in the project root with the following content:
    ```
    LLM_API_KEY="your_llm_api_key_here"
    ```
    Replace `"your_llm_api_key_here"` with an actual API key if integrating with a real LLM.

### 3.2 Running the Application

To run the TUI application:

```bash
python main.py
```

### 3.3 Testing

Currently, there are no dedicated test files. When adding new features, consider creating unit tests for `llm_service.py` and integration tests for `main.py`.

## 4. Project-Specific Conventions

- **Textual Framework:** All UI components and interactions are built using the Textual library. Refer to Textual documentation for UI-related tasks.
- **LLM Integration:** The `llm_service.py` file is the designated place for all LLM API interactions. When implementing actual LLM calls, ensure proper error handling and response parsing.
- **Styling:** UI styling is managed exclusively through `tui_app.css`.

## 5. Future Enhancements

- Replace placeholder LLM logic in `llm_service.py` with actual API calls (e.g., OpenAI, Gemini).
- Implement configurable LLM models and prompts as described in `spec.md`.
- Add comprehensive unit and integration tests.
- Enhance error handling and user feedback.
