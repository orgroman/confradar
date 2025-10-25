from __future__ import annotations

import pytest

from confradar.llm.openai import OpenAIClient


def test_openai_success(monkeypatch):
    # Fake LiteLLM completion response shape (OpenAI-like)
    fake_usage = {"prompt_tokens": 10, "completion_tokens": 6, "total_tokens": 16}
    fake_choice = {"message": {"content": "Hello world"}}
    fake_resp = {"model": "gpt-4o-mini", "choices": [fake_choice], "usage": fake_usage}

    def fake_completion(**kwargs):
        return fake_resp

    # Patch completion used inside confradar.llm.openai
    monkeypatch.setattr("confradar.llm.openai.completion", fake_completion, raising=False)

    client = OpenAIClient(api_key="test-key", base_url="https://api.openai.com/v1")
    res = client.generate("Say hi")
    assert res.text == "Hello world"
    assert res.total_tokens == 16
    assert res.model == "gpt-4o-mini"


def test_openai_retries_then_fails(monkeypatch):
    calls = {"n": 0}

    def fake_completion(**kwargs):
        calls["n"] += 1
        raise RuntimeError("server error")

    monkeypatch.setattr("confradar.llm.openai.completion", fake_completion, raising=False)

    client = OpenAIClient(api_key="test-key", base_url="https://api.openai.com/v1")
    client.max_retries = 2
    with pytest.raises(RuntimeError) as ex:
        client.generate("Say hi")
    assert "failed after" in str(ex.value)
