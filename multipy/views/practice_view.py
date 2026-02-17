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

def big_text(num: int) -> str:
    """Convert a number to larger ASCII art style."""
    digits = {
        '0': ['███', '█ █', '█ █', '█ █', '███'],
        '1': [' █ ', '██ ', ' █ ', ' █ ', '███'],
        '2': ['███', '  █', '███', '█  ', '███'],
        '3': ['███', '  █', '███', '  █', '███'],
        '4': ['█ █', '█ █', '███', '  █', '  █'],
        '5': ['███', '█  ', '███', '  █', '███'],
        '6': ['███', '█  ', '███', '█ █', '███'],
        '7': ['███', '  █', '  █', '  █', '  █'],
        '8': ['███', '█ █', '███', '█ █', '███'],
        '9': ['███', '█ █', '███', '  █', '███'],
    }
    
    num_str = str(num)
    lines = ['', '', '', '', '']
    
    for i, char in enumerate(num_str):
        if char in digits:
            for line_idx in range(5):
                lines[line_idx] += digits[char][line_idx]
                if i < len(num_str) - 1:  # Add spacing between digits
                    lines[line_idx] += ' '
    
    return '\n'.join(lines)

class PracticeView(Screen):
    CSS = """
    PracticeView {
        align: center middle;
    }

    #game-container {
        width: 80%;
        height: auto;
        border: $accent;
        padding: 1;
        background: $surface;
        align: center middle;
    }

    #stats-bar {
        height: auto;
        dock: top;
        background: $primary-darken-2;
        color: $text;
        padding: 1;
    }
    
    #stats-info {
        height: auto;
        text-align: center;
        margin-bottom: 1;
    }
    
    #bars-container {
        height: auto;
        width: 100%;
    }
    
    .stat-bar-row {
        height: 1;
        margin-bottom: 1;
        align: center middle;
    }
    
    .stat-label {
        width: 15;
        text-align: right;
        padding-right: 1;
    }
    
    .stat-bar-container {
        width: 1fr;
        height: 1;
        background: $panel-darken-2;
        border: none;
    }
    
    #correct-bar-fill {
        width: 0%;
        height: 100%;
        background: $success;
    }
    
    #mistakes-bar-fill {
        width: 0%;
        height: 100%;
        background: $error;
    }
    
    .streak-display {
        text-align: center;
        text-style: bold;
        color: $warning;
        margin-top: 0;
    }
    
    .problem-display {
        text-align: center;
        text-style: bold;
        color: $accent;
        height: auto;
        content-align: center middle;
        background: $surface-lighten-1;
        border: solid $secondary;
        margin-bottom: 1;
        padding: 1;
    }

    #input-container {
        align: center middle;
        height: 5;
        margin-top: 1;
    }
    
    #buttons-container {
        align: center middle;
        width: 100%;
    }

    Input {
        width: 20;
        text-align: center;
    }

    .answer-btn {
        margin: 1;
        width: 10;
    }
    
    #timer-container {
        width: 100%;
        height: 1;
        margin-top: 1;
        background: $panel-darken-2;
        border: none;
    }
    
    #timer-fill {
        width: 0%;
        height: 100%;
        background: $accent;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "abort_practice", "Abort Practice"),
        ("t", "toggle_text_size", "Toggle Text Size"),
    ]
    
    time_left = reactive(0.0)
    current_question_idx = reactive(1)
    big_text_enabled = reactive(True)
    
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
            yield Label("", id="stats-info")
            with Vertical(id="bars-container"):
                with Horizontal(classes="stat-bar-row"):
                    yield Label("✓ Correct:", classes="stat-label")
                    with Container(classes="stat-bar-container"):
                        yield Static("", id="correct-bar-fill")
                with Horizontal(classes="stat-bar-row"):
                    yield Label("✗ Mistakes:", classes="stat-label")
                    with Container(classes="stat-bar-container"):
                        yield Static("", id="mistakes-bar-fill")
            yield Label("", id="streak-label", classes="streak-display")

        with Container(id="game-container"):
            yield Static("Ready?", id="problem-display", classes="problem-display")
            
            with Container(id="input-container"):
                if self.settings.game_mode == GameMode.NORMAL:
                    yield Input(placeholder="?", type="integer", id="answer-input")
                else:
                    # Placeholders for buttons, will be added dynamically or updated
                    yield Horizontal(id="buttons-container")
            
            with Container(id="timer-container"):
                yield Static("", id="timer-fill")
        
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
        time_percentage = (elapsed / self.settings.time_limit) * 100
        timer_fill = self.query_one("#timer-fill", Static)
        timer_fill.styles.width = f"{time_percentage}%"
        
        stats_info = self.query_one("#stats-info", Label)
        stats_info.update(f"Question {self.current_question_idx}/{self.settings.max_questions} | Time: {int(remaining)}s")
        
        # Update progress bars
        correct_percentage = (self.results.correct_answers / max(self.settings.max_questions, 1)) * 100
        correct_bar = self.query_one("#correct-bar-fill", Static)
        correct_bar.styles.width = f"{correct_percentage}%"
        
        mistakes_percentage = (self.results.mistakes / max(self.settings.max_questions, 1)) * 100
        mistakes_bar = self.query_one("#mistakes-bar-fill", Static)
        mistakes_bar.styles.width = f"{mistakes_percentage}%"
        
        # Update streak
        streak_label = self.query_one("#streak-label", Label)
        if self.results.current_streak > 0:
            streak_text = f"🔥 Streak: {self.results.current_streak}"
            if self.results.best_streak > self.results.current_streak:
                streak_text += f" (Best: {self.results.best_streak})"
            streak_label.update(streak_text)
        else:
            if self.results.best_streak > 0:
                streak_label.update(f"Best Streak: {self.results.best_streak}")
            else:
                streak_label.update("")

    def next_problem(self):
        if self.current_question_idx > self.settings.max_questions:
            self.end_game()
            return

        is_simple = self.settings.game_mode == GameMode.SIMPLE
        self.current_problem = MathGenerator.generate_problem(self.settings.table_range, simple_mode=is_simple)
        
        # Update Display
        display = self.query_one("#problem-display", Static)
        
        if self.big_text_enabled:
            # Big text mode with ASCII art
            big_num1 = big_text(self.current_problem.factor_a)
            big_num2 = big_text(self.current_problem.factor_b)
            
            # Create the multiplication symbol in ASCII art
            times_symbol = ['   ', '   ', ' × ', '   ', '   ']
            
            # Combine the numbers with the multiplication symbol
            lines1 = big_num1.split('\n')
            lines2 = big_num2.split('\n')
            combined = '\n'.join(lines1[i] + times_symbol[i] + lines2[i] for i in range(5))
            
            display.update(combined)
        else:
            # Normal text mode
            display.update(f"{self.current_problem.factor_a} × {self.current_problem.factor_b}")
        
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
            # Update streak
            self.results.current_streak += 1
            if self.results.current_streak > self.results.best_streak:
                self.results.best_streak = self.results.current_streak
            # Visual feedback could go here (flash green)
        else:
            self.results.mistakes += 1
            # Reset streak on wrong answer
            self.results.current_streak = 0
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

    def action_abort_practice(self):
        """Abort the current practice session and return to menu."""
        self.timer_active = False
        self.app.pop_screen()
    
    def action_toggle_text_size(self):
        """Toggle between big ASCII art text and normal text."""
        self.big_text_enabled = not self.big_text_enabled
        # Refresh the current problem display
        if self.current_problem:
            display = self.query_one("#problem-display", Static)
            if self.big_text_enabled:
                big_num1 = big_text(self.current_problem.factor_a)
                big_num2 = big_text(self.current_problem.factor_b)
                times_symbol = ['   ', '   ', ' × ', '   ', '   ']
                lines1 = big_num1.split('\n')
                lines2 = big_num2.split('\n')
                combined = '\n'.join(lines1[i] + times_symbol[i] + lines2[i] for i in range(5))
                display.update(combined)
            else:
                display.update(f"{self.current_problem.factor_a} × {self.current_problem.factor_b}")

    def end_game(self):
        self.timer_active = False
        self.app.push_screen(SummaryView(self.results))
