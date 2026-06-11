"""Line-oriented prompts after prompt_toolkit or Rich Live (y/N, confirmations)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rich.console import Console

_CAI_GREY = "#9aa0a6"
_CAI_GREEN = "#00ff9d"


def _restore_tty_after_prompt() -> None:
    from cai.util.streaming import restore_terminal_state

    restore_terminal_state(emit_trailing_newline=False)


def normalize_repl_line(value: str) -> str:
    """Strip carriage returns left over from non-canonical TTY reads."""
    return value.replace("\r", "").strip()


def read_repl_line(
    console: Console,
    prompt: str = "",
    *,
    markup: bool = True,
) -> str:
    """Read one line using prompt_toolkit (same stack as the CAI> prompt)."""
    from prompt_toolkit import prompt as ptk_prompt
    from prompt_toolkit.formatted_text import HTML

    _restore_tty_after_prompt()
    try:
        if prompt and markup:
            # Rich markup is for scrollback context only; ptk owns the input line.
            console.print(prompt, markup=markup, emoji=False, end="")
            raw = ptk_prompt("")
        elif prompt:
            raw = ptk_prompt(prompt)
        else:
            raw = ptk_prompt("")
    except (EOFError, KeyboardInterrupt):
        return ""
    finally:
        _restore_tty_after_prompt()
    return normalize_repl_line(raw)


def read_repl_yes_no(
    console: Console,
    label: str,
    *,
    default: bool = False,
    markup: bool = True,
) -> bool:
    """Return True when the user answers y/yes (default answer when they press Enter)."""
    from prompt_toolkit import prompt as ptk_prompt
    from prompt_toolkit.formatted_text import HTML

    _restore_tty_after_prompt()
    suffix = "Y/n" if default else "y/N"
    ptk_prompt_text = HTML(
        f'<style fg="{_CAI_GREY}">[CAI]</style> {label} '
        f'<style fg="{_CAI_GREEN}"><b>({suffix})</b></style>: '
    )
    try:
        raw = ptk_prompt(ptk_prompt_text)
    except (EOFError, KeyboardInterrupt):
        return default
    finally:
        _restore_tty_after_prompt()

    answer = normalize_repl_line(raw)
    if not answer:
        return default
    return answer.lower() in ("y", "yes")
