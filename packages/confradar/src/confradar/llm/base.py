from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .types import LLMResponse


class LLMClient(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> LLMResponse:
        """Generate a completion for the given prompt.

        Implementations should not raise on typical provider errors; instead, they should retry with backoff
        and raise a RuntimeError with a concise message if all retries fail.
        """
        raise NotImplementedError
