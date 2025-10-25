from __future__ import annotations

import time
from typing import Any, Dict, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion

from ..settings import settings
from .base import LLMClient
from .types import LLMResponse


class OpenAIClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        key = api_key or settings.openai_api_key
        if not key:
            raise RuntimeError("OpenAI API key not configured (CONFRADAR_SA_OPENAI or OPENAI_API_KEY)")
        self.client = OpenAI(api_key=key, base_url=base_url or settings.openai_base_url)
        self.max_retries = settings.openai_max_retries

    def generate(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> LLMResponse:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        attempt = 0
        delay = 1.0
        start = time.perf_counter()
        last_error: Optional[Exception] = None
        while attempt < self.max_retries:
            attempt += 1
            try:
                resp: ChatCompletion = self.client.chat.completions.create(
                    model=model or settings.llm_model,
                    messages=messages,  # type: ignore[arg-type]
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                text = resp.choices[0].message.content or ""
                usage = resp.usage
                end = time.perf_counter()
                return LLMResponse(
                    text=text,
                    model=resp.model or (model or settings.llm_model),
                    prompt_tokens=getattr(usage, "prompt_tokens", None),
                    completion_tokens=getattr(usage, "completion_tokens", None),
                    total_tokens=getattr(usage, "total_tokens", None),
                    latency_s=end - start,
                    cost_usd=None,  # Optional: add pricing map later
                )
            except Exception as e:
                last_error = e
                if attempt >= self.max_retries:
                    break
                time.sleep(delay)
                delay = min(delay * 2, 8.0)

        raise RuntimeError(f"OpenAI request failed after {self.max_retries} attempts: {last_error}")
