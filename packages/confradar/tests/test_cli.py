"""Tests for CLI module."""

from __future__ import annotations

from io import StringIO
from unittest.mock import Mock, patch

import pytest

from confradar.cli import build_parser, cmd_fetch, cmd_parse, main


def test_build_parser():
    """Test parser construction."""
    parser = build_parser()
    assert parser.prog == "confradar"
    assert parser.description == "ConfRadar CLI"


def test_cmd_parse_with_text():
    """Test parse command with text argument."""
    args = Mock()
    args.text = "Deadline: Nov 15, 2025"
    
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = cmd_parse(args)
    
    assert result == 0
    output = fake_out.getvalue()
    assert "2025-11-15" in output


def test_cmd_parse_with_stdin():
    """Test parse command reading from stdin."""
    args = Mock()
    args.text = None
    
    with patch("confradar.cli._read_stdin", return_value="Deadline: Dec 20, 2025"):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = cmd_parse(args)
    
    assert result == 0
    output = fake_out.getvalue()
    assert "2025-12-20" in output


def test_cmd_fetch_success():
    """Test fetch command with successful HTTP response."""
    args = Mock()
    args.url = "https://example.com"
    
    mock_response = Mock()
    mock_response.text = "Conference deadline: Jan 10, 2026"
    mock_response.raise_for_status = Mock()
    
    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = cmd_fetch(args)
    
    assert result == 0
    output = fake_out.getvalue()
    assert "2026-01-10" in output


def test_main_parse_subcommand():
    """Test main function with parse subcommand."""
    with patch("sys.stdout", new=StringIO()):
        result = main(["parse", "--text", "Deadline: Nov 1, 2025"])
    
    assert result == 0


def test_main_fetch_subcommand():
    """Test main function with fetch subcommand."""
    mock_response = Mock()
    mock_response.text = "Deadline: Feb 15, 2026"
    mock_response.raise_for_status = Mock()
    
    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        with patch("sys.stdout", new=StringIO()):
            result = main(["fetch", "https://example.com"])
    
    assert result == 0


def test_main_requires_command():
    """Test that main requires a command."""
    with pytest.raises(SystemExit):
        main([])
