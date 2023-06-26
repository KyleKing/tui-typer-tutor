"""The main screen for the application."""

import math
import sys
from contextlib import suppress
from os import get_terminal_size
from typing import ClassVar

from beartype import beartype
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.css.query import NoMatches
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Footer, Header, Label

from ..core.seed_data import DEFAULT_SEED_FILE, load_seed_data
from ..core.typing import Keys, on_keypress

MAX_CHARS = math.floor(0.80 * get_terminal_size()[0])
"""Determine maximum characters that can fit in 80% of the terminal width."""


class Main(Screen[None]):
    """The main screen for the application."""

    DEFAULT_CSS: ClassVar[str] = """
    Screen {
        background: #1b2b34;
    }

    #left-pad {
        width: 10%;
    }
    #content {
        width: 80%;
        align: center middle;
    }

    .tutor-container {
        content-align-horizontal: left;
        height: 2;
    }
    #text-container {
        color: #7e8993;
    }
    #typed-container .error {
        color: #ec5f67;
    }
    #typed-container .success {
        color: #99c794;
    }
    """

    BINDINGS: ClassVar[list[Binding]] = [  # type: ignore[assignment]
        Binding('ctrl+q', 'quit_and_save', 'Quit and Save'),
    ]

    keys: Keys

    def action_quit_and_save(self) -> None:
        """Quit and save."""
        sys.exit(0)
        # FIXME: Save metrics

    def compose(self) -> ComposeResult:
        """Layout."""
        yield Header()
        with Horizontal():
            yield Vertical(id='left-pad')
            # HACK: ^^ couldn't get 'center' alignment to work
            with Vertical(id='content'):
                # TOOD: Add a horizontal progress bar above the content
                #   Docs: https://textual.textualize.io/widgets/progress_bar/#__tabbed_1_4
                yield Horizontal(id='text-container', classes='tutor-container')
                yield Horizontal(id='typed-container', classes='tutor-container')
        # FYI: If using WezTerm, adjust font size with <C-> and <C+>, reset with <C0>
        yield Footer()

    def on_mount(self) -> None:
        """On widget mount."""
        # TODO: Support user-configurable seed data file and more customization
        self.keys = Keys(expected=load_seed_data(seed_text=DEFAULT_SEED_FILE.read_text()))
        cont = self.query_one('#text-container', Horizontal)
        for key in self.keys.get_expected(0, MAX_CHARS):
            cont.mount(Label(key.text, classes='text'))

    @beartype
    def on_key(self, event: Key) -> None:
        """Capture all key presses and show in the typed input."""
        # TODO: Export metrics from the session
        # FIXME: Handle reaching the end!
        on_keypress(event.key, self.keys)

        count = max(self.keys.accum.typed)  # FIXME: Expose this somehow?
        if self.keys.last_was_delete:
            with suppress(NoMatches):
                self.query('Label.typed').last().remove()
        elif count:
            if count >= MAX_CHARS:
                self.query('Label.typed').first().remove()
                self.query('Label.text').first().remove()
            color_class = 'success' if self.keys.typed[-1].was_correct else 'error'
            next_label = Label(self.keys.typed[-1].text, classes=f'typed {color_class}')
            self.query_one('#typed-container', Horizontal).mount(next_label)

            if (start := (count - MAX_CHARS)) > 0:
                next_expected = self.keys.get_expected(start, start + MAX_CHARS)[-1]
                self.query_one('#text-container', Horizontal).mount(Label(next_expected.text, classes='text'))