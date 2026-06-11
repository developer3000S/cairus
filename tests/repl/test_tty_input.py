"""Tests for REPL follow-up prompts (y/N after prompt_toolkit)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from cai.repl.ui.tty_input import (
    normalize_repl_line,
    read_repl_line,
    read_repl_yes_no,
)


class TestNormalizeReplLine:
    def test_strips_carriage_return_from_enter(self):
        assert normalize_repl_line("y\r") == "y"

    def test_strips_whitespace(self):
        assert normalize_repl_line("  yes  \r\n") == "yes"


class TestReadReplYesNo:
    @patch("prompt_toolkit.prompt", return_value="y\r")
    @patch("cai.repl.ui.tty_input._restore_tty_after_prompt")
    def test_yes_with_carriage_return(self, _restore, _prompt):
        console = MagicMock()
        assert read_repl_yes_no(console, "Continue") is True

    @patch("prompt_toolkit.prompt", return_value="")
    @patch("cai.repl.ui.tty_input._restore_tty_after_prompt")
    def test_empty_defaults_to_no(self, _restore, _prompt):
        console = MagicMock()
        assert read_repl_yes_no(console, "Continue", default=False) is False

    @patch("prompt_toolkit.prompt", return_value="n")
    @patch("cai.repl.ui.tty_input._restore_tty_after_prompt")
    def test_no_answer(self, _restore, _prompt):
        console = MagicMock()
        assert read_repl_yes_no(console, "Continue") is False


class TestReadReplLine:
    @patch("prompt_toolkit.prompt", return_value="RESET\r")
    @patch("cai.repl.ui.tty_input._restore_tty_after_prompt")
    def test_restores_tty_around_prompt(self, restore, _prompt):
        console = MagicMock()
        assert read_repl_line(console, "> ", markup=False) == "RESET"
        assert restore.call_count == 2
