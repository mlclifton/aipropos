# Product Requirements Document: Command Line LLM Utility

## 1. Introduction

This document outlines the requirements for a command-line utility designed to assist users in generating Linux shell commands using natural language. The primary goal is to provide a fast, unobtrusive, and efficient way for users to interact with an LLM to obtain relevant commands without leaving their terminal environment.

## 2. Goals

*   **Speed and Unobtrusiveness**: The utility must be quick to launch and operate, minimizing disruption to the user's workflow. The choice of a Text-based User Interface (TUI) invoked directly from the command line is crucial for achieving this.
*   **Natural Language Interaction**: Allow users to describe their desired command-line actions in natural language.
*   **Accurate Command Generation**: Leverage an LLM to generate precise and executable Linux commands.
*   **Clear Explanation (On Demand)**: Provide a concise explanation for each generated command. This explanation should be readily available if the user requires it, but its provision should not compromise the utility's speed or unobtrusiveness.
*   **Seamless Integration**: Enable easy copying of generated commands to the clipboard for immediate use.
*   **Configurable Prompts and Models**: Allow users to configure the LLM prompts and models used by the utility.

## 3. Features

### 3.1 Command Line Invocation
The utility shall be invoked directly from the command line within a terminal session.

### 3.2 Text-based User Interface (TUI)
Upon invocation, the utility shall present a TUI with the following components:
*   **Input Text Box**: A dedicated area where the user can type natural language requests.
*   **Generated Commands Display**: A read-only text area to display the Linux commands returned by the LLM.
*   **Explanation Display (Collapsible)**: A read-only text area to provide a brief explanation of the generated commands, presented in a collapsible section to maintain unobtrusiveness.

### 3.3 LLM Integration
The utility shall integrate with an LLM API to:
*   Send the user's natural language query to the LLM.
*   Receive and parse the LLM's response, extracting the generated commands and their explanations.
*   The prompt sent to the LLM will emphasize that the AI is an expert in Linux development and should return only the actual commands to be executed, minimizing conversational overhead.
*   **Configuration**: The utility shall provide mechanisms to configure the LLM provider, model, and the system prompt used for generating commands.

### 3.4 Clipboard Functionality
*   Pressing the "Enter" key while the generated commands display is focused shall copy the displayed commands to the system clipboard.

## 4. Technology Stack

*   **Language**: Python
*   **UI Framework**: Textual
*   **Clipboard**: `pyperclip` library
*   **LLM Integration**: (To be determined, placeholder in `llm_service.py`)

## 5. Non-Functional Requirements

*   **Performance**: The utility should respond to user input and LLM calls with minimal latency.
*   **Usability**: The TUI should be intuitive and easy to navigate for command-line users, requiring the absolute minimum of keystrokes to copy suggested commands to the clipboard and return to the command line.
*   **Reliability**: The utility should gracefully handle LLM API errors or network issues.
*   *   **Security**: API keys for the LLM should be handled securely (e.g., via environment variables).

## 6. Use Cases

### UC-01: Generate and Copy Simple Command
**Description**: A user needs a command for a common task (e.g., "list all files in current directory") and wants to quickly get and copy it.
**Features Required**:
*   3.1 Command Line Invocation
*   3.2 Text-based User Interface (Input Text Box, Generated Commands Display)
*   3.3 LLM Integration (Send query, Receive/Parse response)
*   3.4 Clipboard Functionality
*   5. Non-Functional Requirements (Performance, Usability)

### UC-02: Understand Generated Command
**Description**: A user receives a generated command and wants to understand its purpose and how it works before executing it.
**Features Required**:
*   3.1 Command Line Invocation
*   3.2 Text-based User Interface (Input Text Box, Generated Commands Display, Explanation Display (Collapsible))
*   3.3 LLM Integration (Send query, Receive/Parse response)
*   5. Non-Functional Requirements (Performance, Usability)

### UC-03: Configure LLM Settings
**Description**: An advanced user wants to change the underlying LLM model or fine-tune the system prompt to get more tailored command suggestions.
**Features Required**:
*   3.3 LLM Integration (Configuration)
*   5. Non-Functional Requirements (Usability)

### UC-04: Refine Command Request
**Description**: A user types a request, and the generated command isn't quite what they intended. They need to quickly modify their input and get a new suggestion.
**Features Required**:
*   3.1 Command Line Invocation
*   3.2 Text-based User Interface (Input Text Box, Generated Commands Display)
*   3.3 LLM Integration (Send query, Receive/Parse response)
*   5. Non-Functional Requirements (Performance, Usability)

### UC-05: Quick Command & Exit
**Description**: A user needs a command and wants to paste it into their terminal and exit the utility with the absolute minimum number of keystrokes.
**Features Required**:
*   3.1 Command Line Invocation
*   3.2 Text-based User Interface (Input Text Box, Generated Commands Display)
*   3.3 LLM Integration (Send query, Receive/Parse response)
*   3.4 Clipboard Functionality
*   5. Non-Functional Requirements (Performance, Usability)
