# Task List for REFACTOR_04: Break Down Large Methods in main.py

This task list outlines the steps to refactor the `on_input_submitted` method in `main.py` to improve its structure and maintainability.

- [x] Create a new private method (e.g., `_call_llm_service`) for handling the LLM service call.
    - [x] The method should accept the user query string as an argument.
    - [x] It should contain the logic for logging the request, calling `self.llm_service.get_commands()`, and logging the response.
    - [x] It should return the result from `get_commands`.

- [x] Create a new private method (e.g., `_handle_llm_success`) for processing a successful response.
    - [x] The method should accept the `parsed_json` dictionary as an argument.
    - [x] It should update `self.commands` and `self.explanation`.
    - [x] It should update the `.text` property of the `commands_display` and `explanation_display` widgets.

- [x] Create a new private method (e.g., `_handle_llm_error`) for processing an error response.
    - [x] The method should accept the `error_message` string as an argument.
    - [x] It should clear `self.commands`.
    - [x] It should update `self.explanation` with the error details.
    - [x] It should update the text of the `commands_display` and `explanation_display` widgets to show the error state.

- [x] Refactor the `on_input_submitted` method to act as a coordinator.
    - [x] The method should get the `event.value`.
    - [x] It should call the new `_call_llm_service` method.
    - [x] It should use an `if/else` block to check the result.
    - [x] It should call `_handle_llm_success` on success.
    - [x] It should call `_handle_llm_error` on failure.
    - [x] It should retain the final logic for focusing the next widget and clearing the input.