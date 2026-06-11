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
    @patch("cai.repl.ui.tty_input.input", return_value="y\r")
    @patch("cai.repl.ui.tty_input.prepare_tty_for_line_input")
    def test_yes_with_carriage_return(self, _prepare, _input):
        console = MagicMock()
        assert read_repl_yes_no(console, "Continue? (y/N): ") is True

    @patch("cai.repl.ui.tty_input.input", return_value="")
    @patch("cai.repl.ui.tty_input.prepare_tty_for_line_input")
    def test_empty_defaults_to_no(self, _prepare, _input):
        console = MagicMock()
        assert read_repl_yes_no(console, "Continue? (y/N): ", default=False) is False

    @patch("cai.repl.ui.tty_input.input", return_value="n")
    @patch("cai.repl.ui.tty_input.prepare_tty_for_line_input")
    def test_no_answer(self, _prepare, _input):
        console = MagicMock()
        assert read_repl_yes_no(console, "Continue? (y/N): ") is False


class TestReadReplLine:
    @patch("cai.repl.ui.tty_input.input", return_value="RESET\r")
    @patch("cai.repl.ui.tty_input.prepare_tty_for_line_input")
    def test_prepares_tty_before_read(self, prepare, _input):
        console = MagicMock()
        assert read_repl_line(console, "> ") == "RESET"
        prepare.assert_called_once()
