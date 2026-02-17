from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button

class AboutView(Screen):
    CSS = """
    AboutView {
        align: center middle;
    }

    #about-container {
        width: 60;
        height: auto;
        border: heavy $accent;
        padding: 2;
        background: $surface;
    }

    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 2;
    }
    
    .content {
        text-align: center;
        margin-bottom: 2;
    }

    #back-btn {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="about-container"):
            yield Static("MultiPy - Multiplication Practice", classes="title")
            yield Static(
                "A Terminal User Interface (TUI) for practicing multiplication tables.\n\n"
                "Built with Textual.\n"
                "Version 1.0.0",
                classes="content"
            )
            yield Button("Back to Menu", id="back-btn", variant="primary")
        yield Footer()

    @on(Button.Pressed, "#back-btn")
    def go_back(self):
        self.app.pop_screen()
