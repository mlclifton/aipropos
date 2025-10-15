from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TextArea, Collapsible
from textual.containers import Container
from textual.reactive import var
from textual.events import Key
from llm_service import LLMService
import pyperclip
from datetime import datetime

class LogViewer(TextArea):
    BINDINGS = [("escape", "hide_logs", "Hide Logs")]

    def on_mount(self) -> None:
        self.focus()

    def action_hide_logs(self) -> None:
        self.remove()

class TUIApp(App):
    CSS_PATH = "tui_app.css"
    BINDINGS = [("q", "quit", "Quit"), ("c", "copy_commands", "Copy Commands"), ("l", "show_logs", "Show Logs")]

    llm_service = LLMService()
    commands = var("")
    explanation = var("")
    log_messages = [] # Stores (timestamp, message) tuples

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Input(placeholder="Enter your command request here...", id="command_input")
            yield TextArea(placeholder="Generated Commands", id="commands_display", read_only=True)
            with Collapsible(title="Explanation", collapsed=True):
                yield TextArea(placeholder="Explanation", id="explanation_display", read_only=True)
        yield Footer()

    def _log_and_notify(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_messages.append((timestamp, message))
        self.notify(f"[{timestamp}] {message}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "command_input":
            user_query = event.value
            if user_query:
                self._log_and_notify("Sending request to Ollama...")
                self.commands, self.explanation, diagnostic_message, raw_ollama_response = self.llm_service.get_commands(user_query)
                self._log_and_notify("Received response from Ollama.")
                self._log_and_notify(diagnostic_message)
                self._log_and_notify(f"Raw Ollama Response: {raw_ollama_response}")

                if not self.commands and self.explanation:
                    # If no command but there's an explanation (likely an error or unexpected format)
                    self.query_one("#commands_display", TextArea).text = "Error or unexpected response." 
                    self.query_one("#explanation_display", TextArea).text = f"Details: {self.explanation}"
                elif self.commands:
                    self.query_one("#commands_display", TextArea).text = self.commands
                    self.query_one("#explanation_display", TextArea).text = self.explanation
                else:
                    self.query_one("#commands_display", TextArea).text = "No command generated."
                    self.query_one("#explanation_display", TextArea).text = "Ollama did not provide a command or explanation."

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
    app = TUIApp()
    app.run()
