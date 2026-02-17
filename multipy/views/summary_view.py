from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button

from multipy.models import SessionResults
from multipy.services.metrics import MetricsService

class SummaryView(Screen):
    CSS = """
    SummaryView {
        align: center middle;
    }

    #summary-container {
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
        text-size: 200%; # Attempting bigger text - textual might ignore percentage in terminal valid units are cells
        margin-bottom: 1;
    }

    .stats-row {
        height: auto;
        margin-bottom: 1;
        text-align: center;
    }

    .feedback {
        text-align: center;
        color: $success;
        text-style: bold;
        margin-bottom: 2;
    }

    #menu-btn {
        width: 100%;
        margin-top: 2;
    }
    """

    def __init__(self, results: SessionResults):
        super().__init__()
        self.results = results

    def compose(self) -> ComposeResult:
        yield Header()
        
        feedback = MetricsService.get_feedback_message(self.results)
        
        with Container(id="summary-container"):
            yield Static("Session Complete", classes="title")
            
            stats_text = (
                f"Correct: {self.results.correct_answers}\n"
                f"Mistakes: {self.results.mistakes}\n"
                f"Time: {self.results.elapsed_time:.1f}s\n"
                f"CPM: {self.results.cpm:.1f}"
            )
            yield Static(stats_text, classes="stats-row")
            
            yield Static(feedback, classes="feedback")
            
            yield Button("Return to Menu", id="menu-btn", variant="primary")
        
        yield Footer()

    @on(Button.Pressed, "#menu-btn")
    def return_to_menu(self):
        self.app.pop_screen() # Pops summary
        # Depending on flow, we might need to ensure we are back at menu.
        # Typically PracticeView pushes SummaryView, so popping returns to PracticeView.
        # But we want to go to Menu.
        
        # A clearer pattern:
        # App has Menu. 
        # Menu pushes Practice.
        # Practice pushes Summary.
        # Summary pop -> Practice.
        # So we probably want to pop twice or use a mode switch.
        
        # Alternatively, we can use app.switch_screen if we register them.
        # Let's assume we want to go back to the 'main' screen which is Menu.
        self.app.pop_screen() # Pop Summary, revealing Practice
        self.app.pop_screen() # Pop Practice, revealing Menu
