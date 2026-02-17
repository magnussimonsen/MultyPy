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
        width: 100%;
        height: auto;
        max-height: 90%;
        border: heavy $accent;
        padding: 1;
        background: $surface;
        overflow-y: auto;
    }

    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 2;
    }
    
    .content {
        text-align: left;
        margin-bottom: 2;
    }

    #back-btn {
        width: 100%;
        margin-bottom: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="about-container"):
            yield Static("MultiPy - Multiplication Practice", classes="title")
            yield Button("Back to Menu", id="back-btn", variant="primary")
            yield Static(
                "A Terminal User Interface (TUI) for practicing multiplication tables.\n\n"
                "Built with Textual.\n"
                "Version 1.0.0\n\n"
                "Authors: Magnus Simonsen and Claude Sonnet\n\n"
                "Licensed under the MIT License\n"
                "Copyright (c) 2026 Magnus Simonsen\n\n"
                "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
                "of this software and associated documentation files (the \"Software\"), to deal\n"
                "in the Software without restriction, including without limitation the rights\n"
                "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
                "copies of the Software, and to permit persons to whom the Software is\n"
                "furnished to do so, subject to the following conditions:\n\n"
                "The above copyright notice and this permission notice shall be included in all\n"
                "copies or substantial portions of the Software.\n\n"
                "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
                "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
                "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.",
                classes="content"
            )
        yield Footer()

    @on(Button.Pressed, "#back-btn")
    def go_back(self):
        self.app.pop_screen()
