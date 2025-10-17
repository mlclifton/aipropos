# Task List for REFACTOR_04: Break Down Large Methods in main.py

This task list outlines the steps to refactor the `on_input_submitted` method in `main.py` to improve its structure and maintainability.

- [ ] Create a new private method (e.g., `_call_llm_service`) for handling the LLM service call.
    - [ ] The method should accept the user query string as an argument.
    - [ ] It should contain the logic for logging the request, calling `self.llm_service.get_commands()`, and logging the response.
    - [ ] It should return the result from `get_commands`.

- [ ] Create a new private method (e.g., `_handle_llm_success`) for processing a successful response.
    - [ ] The method should accept the `parsed_json` dictionary as an argument.
    - [ ] It should update `self.commands` and `self.explanation`.
    - [ ] It should update the `.text` property of the `commands_display` and `explanation_display` widgets.

- [ ] Create a new private method (e.g., `_handle_llm_error`) for processing an error response.
    - [ ] The method should accept the `error_message` string as an argument.
    - [ ] It should clear `self.commands`.
    - [ ] It should update `self.explanation` with the error details.
    - [ ] It should update the text of the `commands_display` and `explanation_display` widgets to show the error state.

- [ ] Refactor the `on_input_submitted` method to act as a coordinator.
    - [ ] The method should get the `event.value`.
    - [ ] It should call the new `_call_llm_service` method.
    - [ ] It should use an `if/else` block to check the result.
    - [ ] It should call `_handle_llm_success` on success.
    - [ ] It should call `_handle_llm_error` on failure.
    - [ ] It should retain the final logic for focusing the next widget and clearing the input.
