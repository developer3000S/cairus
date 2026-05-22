import signal

import pytest

from cai.util import fix_message_list


def test_fix_message_list_handles_multiple_tool_results_without_loop():
    if not hasattr(signal, "SIGALRM"):
        pytest.skip("SIGALRM is required for this infinite-loop regression test")

    messages = [
        {"role": "user", "content": "Run both tools"},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_one",
                    "type": "function",
                    "function": {"name": "first_tool", "arguments": "{}"},
                },
                {
                    "id": "call_two",
                    "type": "function",
                    "function": {"name": "second_tool", "arguments": "{}"},
                },
            ],
        },
        {"role": "tool", "tool_call_id": "call_one", "content": "first result"},
        {"role": "tool", "tool_call_id": "call_two", "content": "second result"},
    ]

    def fail_on_timeout(_signum, _frame):
        raise TimeoutError("fix_message_list did not terminate")

    previous_handler = signal.signal(signal.SIGALRM, fail_on_timeout)
    signal.alarm(2)
    try:
        fixed_messages = fix_message_list(messages)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)

    assert fixed_messages == messages
