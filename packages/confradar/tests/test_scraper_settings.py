"""Tests for Scrapy settings module."""

from __future__ import annotations

from confradar.scrapers import settings


def test_bot_name():
    """Test BOT_NAME is set correctly."""
    assert settings.BOT_NAME == "confradar"


def test_spider_modules():
    """Test spider modules configuration."""
    assert settings.SPIDER_MODULES == ["confradar.scrapers.spiders"]
    assert settings.NEWSPIDER_MODULE == "confradar.scrapers.spiders"


def test_user_agent():
    """Test user agent is set."""
    assert "confradar" in settings.USER_AGENT
    assert "github.com" in settings.USER_AGENT


def test_robotstxt_obey():
    """Test robots.txt is respected."""
    assert settings.ROBOTSTXT_OBEY is True


def test_concurrent_requests():
    """Test concurrent request limits."""
    assert settings.CONCURRENT_REQUESTS == 8
    assert settings.CONCURRENT_REQUESTS_PER_DOMAIN == 4
    assert settings.CONCURRENT_REQUESTS_PER_IP == 4


def test_download_delay():
    """Test download delay configuration."""
    assert settings.DOWNLOAD_DELAY == 1


def test_cookies_disabled():
    """Test cookies are disabled."""
    assert settings.COOKIES_ENABLED is False


def test_telnet_disabled():
    """Test telnet console is disabled."""
    assert settings.TELNETCONSOLE_ENABLED is False


def test_default_request_headers():
    """Test default request headers."""
    assert isinstance(settings.DEFAULT_REQUEST_HEADERS, dict)
    assert "Accept" in settings.DEFAULT_REQUEST_HEADERS
    assert "Accept-Language" in settings.DEFAULT_REQUEST_HEADERS


def test_item_pipelines():
    """Test item pipelines configuration."""
    assert isinstance(settings.ITEM_PIPELINES, dict)
    assert "confradar.scrapers.pipelines.ValidationPipeline" in settings.ITEM_PIPELINES
    assert "confradar.scrapers.pipelines.DeduplicationPipeline" in settings.ITEM_PIPELINES
    assert "confradar.scrapers.pipelines.DatabasePipeline" in settings.ITEM_PIPELINES
    
    # Check pipeline order (lower numbers run first)
    assert settings.ITEM_PIPELINES["confradar.scrapers.pipelines.ValidationPipeline"] == 100
    assert settings.ITEM_PIPELINES["confradar.scrapers.pipelines.DeduplicationPipeline"] == 200
    assert settings.ITEM_PIPELINES["confradar.scrapers.pipelines.DatabasePipeline"] == 300


def test_autothrottle_enabled():
    """Test autothrottle configuration."""
    assert settings.AUTOTHROTTLE_ENABLED is True
    assert settings.AUTOTHROTTLE_START_DELAY == 1
    assert settings.AUTOTHROTTLE_MAX_DELAY == 10
    assert settings.AUTOTHROTTLE_TARGET_CONCURRENCY == 2.0
    assert settings.AUTOTHROTTLE_DEBUG is False


def test_httpcache_enabled():
    """Test HTTP caching configuration."""
    assert settings.HTTPCACHE_ENABLED is True
    assert settings.HTTPCACHE_EXPIRATION_SECS == 3600
    assert settings.HTTPCACHE_DIR == "httpcache"
    assert isinstance(settings.HTTPCACHE_IGNORE_HTTP_CODES, list)
    assert 500 in settings.HTTPCACHE_IGNORE_HTTP_CODES
    assert 404 in settings.HTTPCACHE_IGNORE_HTTP_CODES


def test_feed_export_encoding():
    """Test feed export encoding."""
    assert settings.FEED_EXPORT_ENCODING == "utf-8"


def test_request_fingerprinter():
    """Test request fingerprinter implementation."""
    assert settings.REQUEST_FINGERPRINTER_IMPLEMENTATION == "2.7"


def test_twisted_reactor():
    """Test Twisted reactor configuration."""
    assert "asyncio" in settings.TWISTED_REACTOR.lower()
