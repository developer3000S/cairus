"""Regression: LLM error messages must not expose gateway URLs in the REPL."""

from __future__ import annotations


class TestLlmErrorMessagesHideGatewayUrl:
    def test_user_facing_messages_use_branded_server_label(self):
        from cai.sdk.agents.models.chatcompletions import httpx_client
        import inspect

        source = inspect.getsource(httpx_client)
        assert "_LLM_SERVER_LABEL" in source
        assert httpx_client._LLM_SERVER_LABEL == "Alias Robotics® LLM servers"
        assert "retries from {url}" not in source
        assert "All retries exhausted for {url}" not in source
