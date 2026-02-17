from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, Select, Input
from textual.validation import Number

from multipy.models import Settings, GameMode
from multipy.views.practice_view import PracticeView
from multipy.views.about_view import AboutView

class MenuView(Screen):
    CSS = """
    MenuView {
        align: center middle;
    }

    #menu-container {
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
    
    .setting-row {
        height: auto;
        margin-bottom: 0;
        align: center middle;
    }

    Label {
        width: 20;
        text-align: right;
        padding-right: 2;
    }

    Input, Select {
        width: 30;
    }

    #start-btn {
        width: 100%;
        margin-top: 1;
    }
    
    #about-btn {
        width: 100%;
        margin-top: 1;
    }

    #quit-btn {
        width: 100%;
        margin-top: 1;
        background: $error;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="menu-container"):
            yield Static("✖  MultiPy ", classes="title")
            
            # Simple inputs for settings
            with Horizontal(classes="setting-row"):
                yield Label("Table Range:")
                yield Input("10", id="range-input", validators=[Number(minimum=1, maximum=50)])
            
            with Horizontal(classes="setting-row"):
                yield Label("Questions:")
                yield Input("10", id="questions-input", validators=[Number(minimum=1, maximum=100)])
                
            with Horizontal(classes="setting-row"):
                yield Label("Time (sec):")
                yield Input("30", id="time-input", validators=[Number(minimum=5, maximum=300)])
                
            with Horizontal(classes="setting-row"):
                yield Label("Mode:")
                yield Select.from_values(
                    ["Simple (Buttons)", "Normal (Typing)"],
                    value="Simple (Buttons)",
                    id="mode-select"
                )

            yield Button("Start Practice", id="start-btn", variant="success")
            yield Button("About", id="about-btn", variant="primary")
            yield Button("Quit", id="quit-btn", variant="error")
        yield Footer()

    @on(Button.Pressed, "#start-btn")
    def on_start(self):
        # Validate and gather settings
        range_input = self.query_one("#range-input", Input)
        questions_input = self.query_one("#questions-input", Input)
        time_input = self.query_one("#time-input", Input)
        mode_select = self.query_one("#mode-select", Select)
        
        # Basic validation fallback
        if not range_input.is_valid or not questions_input.is_valid or not time_input.is_valid:
            self.notify("Invalid settings. Please check your inputs.", severity="error")
            return

        table_range = int(range_input.value)
        max_questions = int(questions_input.value)
        time_limit = int(time_input.value)
        
        mode_val = mode_select.value
        game_mode = GameMode.SIMPLE if "Simple" in str(mode_val) else GameMode.NORMAL
        
        settings = Settings(
            table_range=table_range,
            max_questions=max_questions,
            time_limit=time_limit,
            game_mode=game_mode
        )
        
        self.app.push_screen(PracticeView(settings))

    @on(Button.Pressed, "#about-btn")
    def on_about(self):
        self.app.push_screen(AboutView())

    @on(Button.Pressed, "#quit-btn")
    def on_quit(self):
        self.app.exit()
