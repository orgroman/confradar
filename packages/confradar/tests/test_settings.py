"""Tests for settings module."""

from __future__ import annotations

import os

import pytest

from confradar.settings import Settings, get_settings


def test_settings_default_values():
    """Test default settings values."""
    settings = Settings()
    assert settings.llm_provider == "openai"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.openai_base_url == "http://localhost:4000"
    assert settings.openai_timeout_s == 20.0
    assert settings.openai_max_retries == 3


def test_settings_from_env(monkeypatch):
    """Test settings loaded from environment variables."""
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("LLM_MODEL", "claude-3-sonnet")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("OPENAI_TIMEOUT_S", "30.0")
    
    settings = Settings()
    assert settings.llm_provider == "anthropic"
    assert settings.llm_model == "claude-3-sonnet"
    assert settings.database_url == "sqlite:///test.db"
    assert settings.openai_timeout_s == 30.0


def test_settings_openai_api_key_alias(monkeypatch):
    """Test that OpenAI API key can be loaded from multiple env var names."""
    monkeypatch.setenv("CONFRADAR_SA_OPENAI", "test-key-1")
    settings = Settings()
    assert settings.openai_api_key == "test-key-1"
    
    monkeypatch.delenv("CONFRADAR_SA_OPENAI")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-2")
    settings = Settings()
    assert settings.openai_api_key == "test-key-2"


def test_settings_base_url_alias(monkeypatch):
    """Test that base URL can be loaded from multiple env var names."""
    monkeypatch.setenv("LITELLM_BASE_URL", "http://litellm:8000")
    settings = Settings()
    assert settings.openai_base_url == "http://litellm:8000"
    
    monkeypatch.delenv("LITELLM_BASE_URL")
    monkeypatch.setenv("LLM_BASE_URL", "http://llm:9000")
    settings = Settings()
    assert settings.openai_base_url == "http://llm:9000"


def test_get_settings():
    """Test get_settings helper function."""
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.llm_provider == "openai"
