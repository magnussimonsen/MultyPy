import time
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input, Label, ProgressBar
from textual.reactive import reactive

from multipy.models import Settings, SessionResults, GameMode
from multipy.services.math_generator import MathGenerator, MathProblem
from multipy.views.summary_view import SummaryView

class PracticeView(Screen):
    CSS = """
    PracticeView {
        align: center middle;
    }

    #game-container {
        width: 80%;
        height: auto;
        border: heavy $accent;
        padding: 2;
        background: $surface;
        align: center middle;
    }

    #stats-bar {
        height: 3;
        dock: top;
        align: center middle;
        text-align: center;
        background: $primary-darken-2;
        color: $text;
        padding: 1;
    }
    
    .problem-display {
        text-align: center;
        text-style: bold;
        color: $accent;
        height: 5;
        content-align: center middle;
        background: $surface-lighten-1;
        border: solid $secondary;
        margin-bottom: 2;
        text-size: 32; /* Fake large text via style if possible, or just standard bold */
    }

    #input-container {
        align: center middle;
        height: 5;
        margin-top: 1;
    }

    Input {
        width: 20;
        text-align: center;
    }

    .answer-btn {
        margin: 1;
        width: 15;
    }
    
    #timer-bar {
        margin-top: 1;
    }
    """

    time_left = reactive(0.0)
    current_question_idx = reactive(1)
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.results = SessionResults()
        self.current_problem: MathProblem = None
        self.timer_active = False
        self.start_time = 0.0

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(id="stats-bar"):
            yield Label("", id="stats-label")

        with Container(id="game-container"):
            yield Static("Ready?", id="problem-display", classes="problem-display")
            
            with Container(id="input-container"):
                if self.settings.game_mode == GameMode.NORMAL:
                    yield Input(placeholder="?", type="integer", id="answer-input")
                else:
                    # Placeholders for buttons, will be added dynamically or updated
                    yield Horizontal(id="buttons-container")
            
            yield ProgressBar(total=self.settings.time_limit, show_eta=False, id="time-progress")
        
        yield Footer()

    def on_mount(self):
        self.start_game()
    
    def start_game(self):
        self.results = SessionResults()
        self.current_question_idx = 1
        self.time_left = float(self.settings.time_limit)
        self.timer_active = True
        self.start_time = time.time()
        self.set_interval(0.1, self.update_timer)
        self.next_problem()

    def update_timer(self):
        if not self.timer_active:
            return
            
        elapsed = time.time() - self.start_time
        self.results.elapsed_time = elapsed
        remaining = self.settings.time_limit - elapsed
        
        if remaining <= 0:
            remaining = 0
            self.timer_active = False
            self.end_game()
        
        self.time_left = remaining
        
        # Update UI
        progress = self.query_one("#time-progress", ProgressBar)
        progress.progress = elapsed
        
        stats_label = self.query_one("#stats-label", Label)
        stats_label.update(f"Q: {self.current_question_idx}/{self.settings.max_questions} | Time: {int(remaining)}s | Score: {self.results.correct_answers}")

    def next_problem(self):
        if self.current_question_idx > self.settings.max_questions:
            self.end_game()
            return

        is_simple = self.settings.game_mode == GameMode.SIMPLE
        self.current_problem = MathGenerator.generate_problem(self.settings.table_range, simple_mode=is_simple)
        
        # Update Display
        display = self.query_one("#problem-display", Static)
        display.update(f"{self.current_problem.factor_a} x {self.current_problem.factor_b}")
        
        if is_simple:
            container = self.query_one("#buttons-container", Horizontal)
            container.remove_children()
            for opt in self.current_problem.options:
                btn = Button(str(opt), variant="primary", classes="answer-btn")
                # Store the value on the button logic
                # We can't attach arbitrary data easily to button unless we subclass, 
                # but we can parse the label.
                container.mount(btn)
        else:
            inp = self.query_one("#answer-input", Input)
            inp.value = ""
            inp.focus()

    def check_answer(self, user_answer: int):
        self.results.total_questions += 1
        
        if user_answer == self.current_problem.answer:
            self.results.correct_answers += 1
            # Visual feedback could go here (flash green)
        else:
            self.results.mistakes += 1
            # Visual feedback (flash red)
        
        self.current_question_idx += 1
        self.next_problem()

    @on(Input.Submitted, "#answer-input")
    def on_input_submitted(self, event: Input.Submitted):
        if not event.value.isdigit():
            return
        self.check_answer(int(event.value))

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed):
        # Only handle answer buttons (which have numeric labels)
        if event.button.label.plain.isdigit():
            val = int(event.button.label.plain)
            self.check_answer(val)

    def end_game(self):
        self.timer_active = False
        self.app.push_screen(SummaryView(self.results))
