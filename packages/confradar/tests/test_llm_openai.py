from __future__ import annotations

from types import SimpleNamespace
import pytest

from confradar.llm.openai import OpenAIClient


def test_openai_success(monkeypatch):
    # Fake OpenAI response object structure
    fake_usage = SimpleNamespace(prompt_tokens=10, completion_tokens=6, total_tokens=16)
    fake_choice = SimpleNamespace(message=SimpleNamespace(content="Hello world"))
    fake_resp = SimpleNamespace(model="gpt-4o-mini", choices=[fake_choice], usage=fake_usage)

    class FakeCompletions:
        def create(self, **kwargs):
            return fake_resp

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.chat = FakeChat()

    monkeypatch.setattr("confradar.llm.openai.OpenAI", FakeClient)

    client = OpenAIClient(api_key="test-key", base_url="https://api.openai.com/v1")
    res = client.generate("Say hi")
    assert res.text == "Hello world"
    assert res.total_tokens == 16
    assert res.model == "gpt-4o-mini"


def test_openai_retries_then_fails(monkeypatch):
    class FakeCompletions:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            self.calls += 1
            raise RuntimeError("server error")

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.chat = FakeChat()

    monkeypatch.setattr("confradar.llm.openai.OpenAI", FakeClient)

    client = OpenAIClient(api_key="test-key", base_url="https://api.openai.com/v1")
    client.max_retries = 2
    with pytest.raises(RuntimeError) as ex:
        client.generate("Say hi")
    assert "failed after" in str(ex.value)
