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
                f"CPM: {self.results.cpm:.1f}\n"
                f"🔥 Best Streak: {self.results.best_streak}"
            )
            yield Static(stats_text, classes="stats-row")
            
            yield Static(feedback, classes="feedback")
            
            yield Button("Return to Menu", id="menu-btn", variant="primary")
        
        yield Footer()

    @on(Button.Pressed, "#menu-btn")
    def return_to_menu(self):
        # We need to pop PracticeView as well.
        # Since we are on SummaryView, we can't easily pop the screen *underneath* us directly 
        # without closing ourselves first.
        # But if we close ourselves, this handler (owned by SummaryView) might be cancelled.
        # So we schedule the pops on the app level, independent of this screen's lifecycle.
        
        def pop_twice():
            self.app.pop_screen() # Pop SummaryView
            self.app.pop_screen() # Pop PracticeView
            
        self.app.call_after_refresh(pop_twice)
