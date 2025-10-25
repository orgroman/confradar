from __future__ import annotations

import time
from typing import Any, Optional

from litellm import completion, completion_cost

from ..settings import settings
from .base import LLMClient
from .types import LLMResponse


class OpenAIClient(LLMClient):
    """OpenAI-compatible client implemented via LiteLLM.

    Uses LiteLLM's completion API, which supports multiple providers and optional proxy server.
    API key is read from CONFRADAR_SA_OPENAI (or OPENAI_API_KEY fallback) via settings.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        key = api_key or settings.openai_api_key
        if not key:
            raise RuntimeError("OpenAI API key not configured (CONFRADAR_SA_OPENAI or OPENAI_API_KEY)")
        self.api_key = key
        self.base_url = base_url or settings.openai_base_url
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
                resp = completion(
                    model=model or settings.llm_model,
                    messages=messages,  # type: ignore[arg-type]
                    max_tokens=max_tokens,
                    temperature=temperature,
                    api_key=self.api_key,
                    base_url=self.base_url,
                )
                # LiteLLM returns an OpenAI-like dict or object; normalize access
                choices = getattr(resp, "choices", None) or resp.get("choices", [])
                usage = getattr(resp, "usage", None) or resp.get("usage", {})
                model_name = getattr(resp, "model", None) or resp.get("model", model or settings.llm_model)
                text = ""
                if choices:
                    msg = getattr(choices[0], "message", None) or choices[0].get("message", {})
                    text = getattr(msg, "content", None) or msg.get("content", "")
                end = time.perf_counter()
                # Cost (if pricing known) via LiteLLM helper
                try:
                    cost = completion_cost(resp)
                except Exception:
                    cost = None
                return LLMResponse(
                    text=text,
                    model=model_name,
                    prompt_tokens=getattr(usage, "prompt_tokens", None) or usage.get("prompt_tokens"),
                    completion_tokens=getattr(usage, "completion_tokens", None) or usage.get("completion_tokens"),
                    total_tokens=getattr(usage, "total_tokens", None) or usage.get("total_tokens"),
                    latency_s=end - start,
                    cost_usd=cost,
                )
            except Exception as e:
                last_error = e
                if attempt >= self.max_retries:
                    break
                time.sleep(delay)
                delay = min(delay * 2, 8.0)

        raise RuntimeError(f"OpenAI (via LiteLLM) request failed after {self.max_retries} attempts: {last_error}")
