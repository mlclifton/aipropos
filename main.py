from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TextArea
from textual.containers import Container
from textual.reactive import var
from textual.events import Key
from llm_service import LLMService
import pyperclip
from datetime import datetime
import sys
import argparse

class LogViewer(TextArea):
    BINDINGS = [("escape", "hide_logs", "Hide Logs")]

    def on_mount(self) -> None:
        self.focus()

    def action_hide_logs(self) -> None:
        self.remove()

class TUIApp(App):
    CSS_PATH = "tui_app.css"
    BINDINGS = [("q", "quit", "Quit"), ("c", "copy_commands", "Copy Commands"), ("l", "show_logs", "Show Logs")]

    def __init__(self, system_prompt: str, initial_query: str = None):
        super().__init__()
        self.llm_service = LLMService(system_prompt=system_prompt)
        self.commands = var("")
        self.explanation = var("")
        self.log_messages = [] # Stores (timestamp, message) tuples
        self.initial_query = initial_query

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Input(placeholder="Enter your command request here...", id="command_input")
            yield TextArea(placeholder="Generated Commands", id="commands_display", read_only=True)
            yield TextArea(placeholder="Explanation", id="explanation_display", read_only=True)
        yield Footer()

    async def on_mount(self) -> None:
        self._log_and_notify("TUIApp mounted.")
        if self.initial_query:
            self._log_and_notify(f"Initial query: {self.initial_query}")
            query_input = self.query_one("#command_input", Input)
            query_input.value = self.initial_query

            worker = self.run_worker(lambda: self._call_llm_service(self.initial_query), thread=True)
            parsed_json, error_message = await worker.wait()
            
            if parsed_json:
                self._handle_llm_success(parsed_json)
            else:
                self._handle_llm_error(error_message)

    def _log_and_notify(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_messages.append((timestamp, message))
        self.notify(f"[{timestamp}] {message}")

    def _call_llm_service(self, user_query: str):
        self._log_and_notify("Sending request to Ollama...")
        parsed_json, error_message, diagnostic_message, raw_ollama_response = self.llm_service.get_commands(user_query)
        self._log_and_notify("Received response from Ollama.")
        self._log_and_notify(diagnostic_message)
        self._log_and_notify(f"Raw Ollama Response: {raw_ollama_response}")
        return parsed_json, error_message

    def _handle_llm_success(self, parsed_json):
        self._log_and_notify("Handling LLM success.")
        self.commands = "\n".join(parsed_json.get("commands", []))
        self.explanation = parsed_json.get("explanation", "No explanation provided.")
        self._log_and_notify(f"Commands: {self.commands}")
        self._log_and_notify(f"Explanation: {self.explanation}")
        self.query_one("#commands_display", TextArea).text = self.commands
        self.query_one("#explanation_display", TextArea).text = self.explanation

    def _handle_llm_error(self, error_message):
        self.commands = ""
        self.explanation = error_message
        self.query_one("#commands_display", TextArea).text = "Error or unexpected response."
        self.query_one("#explanation_display", TextArea).text = f"Details: {error_message}"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "command_input":
            user_query = event.value
            if user_query:
                parsed_json, error_message = self._call_llm_service(user_query)
                if parsed_json:
                    self._handle_llm_success(parsed_json)
                else:
                    self._handle_llm_error(error_message)
                
                self.query_one("#commands_display").focus()
                self.query_one("#command_input", Input).clear()

    def action_show_logs(self) -> None:
        formatted_logs = []
        for timestamp, message in reversed(self.log_messages):
            formatted_logs.append(f"[{timestamp}] {message}")
        separated_logs = "\n" + "\n---\n".join(formatted_logs)
        log_viewer = LogViewer(separated_logs, id="log_viewer", read_only=True)
        self.screen.mount(log_viewer)
        log_viewer.add_class("-modal")

    def action_copy_commands(self) -> None:
        if self.commands:
            pyperclip.copy(self.commands)
            self.notify("Commands copied to clipboard!")

    def action_quit(self) -> None:
        self.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Text-based User Interface (TUI) for interacting with Ollama. "
                    "Specify the Ollama model via the OLLAMA_MODEL_NAME environment variable."
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="The user's query. If provided, the app will run in CLI mode."
    )
    parser.add_argument(
        "--profile",
        default="default",
        help="The profile to use from prompts.txt (e.g., 'default', 'git'). "
             "Defaults to 'default' if not specified."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available profiles from prompts.txt and exit."
    )
    parser.add_argument(
        "--edit",
        action="store_true",
        help="Edit the specified profile's prompt."
    )
    args = parser.parse_args()

    prompts = LLMService.load_prompts('prompts.txt')

    if args.list:
        print("Available profiles:")
        for profile in prompts:
            print(f"- {profile}")
        sys.exit(0)

    if args.edit:
        from prompt_editor import PromptEditorApp
        if args.profile not in prompts:
            print(f"Error: Profile '{args.profile}' not found in prompts.txt.")
            sys.exit(1)
        app = PromptEditorApp(profile=args.profile, prompts=prompts)
        result = app.run()
        if result:
            print(result)
        sys.exit(0)

    system_prompt = prompts.get(args.profile, prompts["default"])
    
    app = TUIApp(system_prompt=system_prompt, initial_query=args.query)
    app.run()
