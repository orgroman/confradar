from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_s: float | None = None
    cost_usd: float | None = None
