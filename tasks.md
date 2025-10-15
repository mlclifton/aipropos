# Ollama Integration Task List

This document outlines the steps required to integrate Ollama into the `txtui_play` project, replacing the current placeholder LLM service.

## Phase 1: Setup and Initial Integration

- [X] **Task 1.1: Research Ollama Python Client/API Interaction**
    - [X] Investigate official Ollama Python client libraries or common methods for interacting with its REST API using `requests`.
    - [X] Understand the required API endpoints, request formats (e.g., `/api/generate`), and response structures for generating text.

- [X] **Task 1.2: Update `requirements.txt`**
    - [X] Add any new Python packages identified in Task 1.1 (e.g., `ollama` client library, `requests` if not already present) to `requirements.txt`.

- [X] **Task 1.3: Configure Ollama Endpoint and Model**
    - [X] Modify `llm_service.py` to load the Ollama API URL (e.g., `OLLAMA_API_BASE_URL`) and the desired model name (e.g., `OLLAMA_MODEL_NAME`) from environment variables.
    - [X] Update `.env.example` (or create if it doesn't exist) to include these new environment variables.

## Phase 2: Implement LLMService Logic

- [X] **Task 2.1: Modify `LLMService.get_commands` for Ollama API Call**
    - [X] Replace the hardcoded response logic in `llm_service.py` with an actual API call to the configured Ollama endpoint.
    - [X] Construct the request payload, including the user's query and the system prompt (e.g., "You are an expert Linux development assistant...").
    - [X] Send the request and receive the response.

- [X] **Task 2.2: Parse Ollama Response**
    - [X] Extract the generated command(s) and explanation from the Ollama API response. This may involve parsing JSON and potentially extracting specific fields or using regular expressions if the output is less structured.
    - [X] Ensure the extracted data can be returned in the format expected by `main.py`.

- [X] **Task 2.3: Implement Robust Error Handling**
    - [X] Add `try-except` blocks to handle potential network errors (e.g., `requests.exceptions.ConnectionError`).
    - [X] Handle non-200 HTTP responses from the Ollama API.
    - [X] Gracefully manage cases where the Ollama response does not contain the expected command or explanation format.
    - [X] Provide informative error messages to the user via the TUI.

## Phase 3: Testing and Verification

- [X] **Task 3.1: Manual Testing with Local Ollama Instance**
    - [X] **Instructions for setting up Ollama:**
        1.  **Download and Install Ollama:** Follow the instructions on the official Ollama website (https://ollama.ai/download) to download and install Ollama for your operating system.
        2.  **Pull a Model:** Open your terminal and pull a suitable model. For example, to pull the `llama2` model, run: `ollama pull llama2`.
        3.  **Verify Ollama is Running:** Ensure the Ollama server is running. It usually starts automatically after installation.
    - [X] Manually test the TUI with various natural language queries to ensure correct command generation and explanation display.

- [X] **Task 3.2: (Optional) Add Unit Tests for `LLMService`**
    - [X] Create a test file (e.g., `test_llm_service.py`).
    - [X] Write unit tests for the `LLMService` class, mocking the Ollama API calls to ensure correct request construction, response parsing, and error handling.

## Phase 4: Refinement and Documentation

- [X] **Task 4.1: Update `solution_arch.md`**
    - [X] Reflect the changes made for Ollama integration in the architecture document.
    - [X] Update any diagrams (e.g., package associations) if new dependencies are introduced.

- [X] **Task 4.2: Update `spec.md` (if necessary)**
    - [X] Review `spec.md` to ensure all requirements related to LLM integration are still met or if any updates are needed based on Ollama's capabilities.
