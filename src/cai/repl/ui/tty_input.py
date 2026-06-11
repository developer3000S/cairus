"""Line-oriented prompts after prompt_toolkit or Rich Live (y/N, confirmations)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rich.console import Console


def prepare_tty_for_line_input() -> None:
    """Restore cooked TTY before ``input()`` / Rich ``console.input``."""
    from cai.util.streaming import ensure_cooked_tty, restore_terminal_state

    restore_terminal_state(emit_trailing_newline=False)
    ensure_cooked_tty()


def normalize_repl_line(value: str) -> str:
    """Strip carriage returns left over from non-canonical TTY reads."""
    return value.replace("\r", "").strip()


def read_repl_line(
    console: Console,
    prompt: str = "",
    *,
    markup: bool = True,
) -> str:
    """Read one line with Rich prompt styling; safe after the main CAI> prompt."""
    prepare_tty_for_line_input()
    if prompt:
        console.print(prompt, markup=markup, emoji=False, end="")
    try:
        raw = input()
    except EOFError:
        return ""
    return normalize_repl_line(raw)


def read_repl_yes_no(
    console: Console,
    prompt: str,
    *,
    default: bool = False,
    markup: bool = True,
) -> bool:
    """Return True when the user answers y/yes (default answer when they press Enter)."""
    answer = read_repl_line(console, prompt, markup=markup)
    if not answer:
        return default
    return answer.lower() in ("y", "yes")
