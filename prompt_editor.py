from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea, Static
from textual.containers import Vertical
from llm_service import LLMService

class PromptEditorApp(App):
    CSS = """
    .main-container {
        padding: 1;
    }
    #prompt-editor {
        height: 80%;
        border: round white;
    }
    .help-text {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("escape", "command_mode", "Command Mode"),
        ("s", "save_and_quit", "Save & Quit"),
        ("q", "quit_without_saving", "Quit"),
        ("i", "edit_mode", "Edit Mode"),
    ]

    def __init__(self, profile: str, prompts: dict):
        super().__init__()
        self.profile = profile
        self.prompts = prompts
        self.prompt_content = self.prompts.get(self.profile, "")
        self.mode = "edit"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="main-container"):
            yield TextArea(self.prompt_content, id="prompt-editor")
            yield Static("Press 'escape' to enter command mode.", classes="help-text")
        yield Footer()

    def on_mount(self) -> None:
        self.action_edit_mode()

    def action_edit_mode(self) -> None:
        self.mode = "edit"
        self.query_one("#prompt-editor").focus()
        self.query_one(".help-text").update("Press 'escape' to enter command mode.")

    def action_command_mode(self) -> None:
        self.mode = "command"
        self.set_focus(None)
        self.query_one(".help-text").update("Press 's' to save, 'q' to quit, or 'i' to edit.")

    def action_save_and_quit(self) -> None:
        if self.mode == "command":
            new_content = self.query_one("#prompt-editor").text
            self.prompts[self.profile] = new_content
            LLMService.save_prompts('prompts.txt', self.prompts)
            self.exit(message="Prompt saved.")

    def action_quit_without_saving(self) -> None:
        if self.mode == "command":
            self.exit(message="Quit without saving.")