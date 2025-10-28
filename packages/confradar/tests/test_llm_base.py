"""Tests for LLM types and base classes."""

from __future__ import annotations

import pytest

from confradar.llm.base import LLMClient
from confradar.llm.types import LLMResponse


class TestLLMResponse:
    """Test LLMResponse dataclass."""
    
    def test_llm_response_creation(self):
        """Test creating an LLMResponse with all fields."""
        response = LLMResponse(
            text="This is a test response",
            model="gpt-4o-mini",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            latency_s=1.5,
            cost_usd=0.001
        )
        
        assert response.text == "This is a test response"
        assert response.model == "gpt-4o-mini"
        assert response.prompt_tokens == 100
        assert response.completion_tokens == 50
        assert response.total_tokens == 150
        assert response.latency_s == 1.5
        assert response.cost_usd == 0.001
    
    def test_llm_response_minimal(self):
        """Test creating an LLMResponse with only required fields."""
        response = LLMResponse(
            text="Test response",
            model="gpt-4o"
        )
        
        assert response.text == "Test response"
        assert response.model == "gpt-4o"
        assert response.prompt_tokens is None
        assert response.completion_tokens is None
        assert response.total_tokens is None
        assert response.latency_s is None
        assert response.cost_usd is None
    
    def test_llm_response_with_partial_tokens(self):
        """Test LLMResponse with partial token information."""
        response = LLMResponse(
            text="Response",
            model="gpt-4o-mini",
            prompt_tokens=50,
            completion_tokens=25
        )
        
        assert response.prompt_tokens == 50
        assert response.completion_tokens == 25
        assert response.total_tokens is None


class MockLLMClient(LLMClient):
    """Mock LLM client for testing."""
    
    def generate(self, prompt, *, system=None, model=None, max_tokens=512, temperature=0.0, **kwargs):
        """Mock generate method."""
        return LLMResponse(
            text=f"Mock response to: {prompt[:20]}",
            model=model or "mock-model",
            prompt_tokens=len(prompt.split()),
            completion_tokens=5,
            total_tokens=len(prompt.split()) + 5
        )


class TestLLMClient:
    """Test LLMClient abstract base class."""
    
    def test_llm_client_cannot_instantiate(self):
        """Test that LLMClient cannot be instantiated directly."""
        with pytest.raises(TypeError):
            LLMClient()
    
    def test_mock_llm_client_generate(self):
        """Test mock LLM client generate method."""
        client = MockLLMClient()
        response = client.generate("Test prompt")
        
        assert isinstance(response, LLMResponse)
        assert "Mock response to: Test prompt" in response.text
        assert response.model == "mock-model"
    
    def test_mock_llm_client_with_custom_model(self):
        """Test mock client with custom model."""
        client = MockLLMClient()
        response = client.generate("Test prompt", model="custom-model")
        
        assert response.model == "custom-model"
    
    def test_mock_llm_client_with_system_prompt(self):
        """Test mock client with system prompt."""
        client = MockLLMClient()
        response = client.generate(
            "User prompt",
            system="You are a helpful assistant",
            model="test-model"
        )
        
        assert isinstance(response, LLMResponse)
        assert response.model == "test-model"
    
    def test_mock_llm_client_with_temperature(self):
        """Test mock client with temperature parameter."""
        client = MockLLMClient()
        response = client.generate(
            "Test prompt",
            temperature=0.7
        )
        
        assert isinstance(response, LLMResponse)
    
    def test_mock_llm_client_with_max_tokens(self):
        """Test mock client with max_tokens parameter."""
        client = MockLLMClient()
        response = client.generate(
            "Test prompt",
            max_tokens=1000
        )
        
        assert isinstance(response, LLMResponse)
    
    def test_mock_llm_client_token_counting(self):
        """Test that mock client counts tokens correctly."""
        client = MockLLMClient()
        prompt = "This is a test prompt with multiple words"
        response = client.generate(prompt)
        
        assert response.prompt_tokens == len(prompt.split())
        assert response.completion_tokens == 5
        assert response.total_tokens == len(prompt.split()) + 5


class FailingLLMClient(LLMClient):
    """LLM client that raises NotImplementedError."""
    pass


class TestLLMClientInterface:
    """Test LLM client interface requirements."""
    
    def test_llm_client_requires_generate_implementation(self):
        """Test that subclass must implement generate method."""
        # FailingLLMClient doesn't implement generate, so instantiation
        # should succeed but calling generate should fail
        with pytest.raises(TypeError):
            client = FailingLLMClient()
