from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TextArea, Collapsible
from textual.containers import Container
from textual.reactive import var
from textual.events import Key
from llm_service import LLMService
import pyperclip

class TUIApp(App):
    CSS_PATH = "tui_app.css"
    BINDINGS = [("q", "quit", "Quit"), ("c", "copy_commands", "Copy Commands")]

    llm_service = LLMService()
    commands = var("")
    explanation = var("")

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield TextArea(placeholder="Enter your command request here...", id="command_input", show_line_numbers=False, show_cursor=True)
            yield TextArea(placeholder="Generated Commands", id="commands_display", read_only=True)
            with Collapsible(title="Explanation", collapsed=True):
                yield TextArea(placeholder="Explanation", id="explanation_display", read_only=True)
        yield Footer()

    def on_key(self, event: Key) -> None:
        if self.focused.id == "command_input" and event.key == "enter":
            user_query = self.query_one("#command_input", TextArea).text
            if user_query:
                self.commands, self.explanation = self.llm_service.get_commands(user_query)
                self.query_one("#commands_display", TextArea).text = self.commands
                self.query_one("#explanation_display", TextArea).text = self.explanation
                self.query_one("#commands_display").focus()
                self.query_one("#command_input", TextArea).clear()
                event.prevent_default()

    def action_copy_commands(self) -> None:
        if self.commands:
            pyperclip.copy(self.commands)
            self.notify("Commands copied to clipboard!")

    def action_quit(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = TUIApp()
    app.run()
