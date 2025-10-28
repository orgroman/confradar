"""Extended tests for date parsing module."""

from __future__ import annotations

from datetime import datetime

import pytest

from confradar.parsers.dates import DATE_REGEX, extract_dates_from_text


def test_extract_simple_month_name_date():
    """Test extraction of simple month name date."""
    text = "Submission Deadline: Nov 15, 2025 (AoE)"
    dates = extract_dates_from_text(text)
    assert any(d.date().isoformat() == "2025-11-15" for d in dates)


def test_extract_iso_date():
    """Test extraction of ISO format date."""
    text = "Notification: 2025-12-20"
    dates = extract_dates_from_text(text)
    assert any(d.date().isoformat() == "2025-12-20" for d in dates)


def test_extract_multiple_dates():
    """Test extraction of multiple dates from text."""
    text = """
    Submission: Jan 15, 2026
    Notification: March 20, 2026
    Camera Ready: April 10, 2026
    """
    dates = extract_dates_from_text(text)
    assert len(dates) >= 3
    date_strings = [d.date().isoformat() for d in dates]
    assert "2026-01-15" in date_strings
    assert "2026-03-20" in date_strings
    assert "2026-04-10" in date_strings


def test_extract_date_with_day_first():
    """Test extraction of date with day before month."""
    text = "Deadline: 20 December 2025"
    dates = extract_dates_from_text(text)
    assert any(d.date().isoformat() == "2025-12-20" for d in dates)


def test_extract_no_dates():
    """Test that no dates are extracted from text without dates."""
    text = "This is a conference about machine learning and AI."
    dates = extract_dates_from_text(text)
    assert len(dates) == 0


def test_extract_abbreviated_month():
    """Test extraction with abbreviated month names."""
    text = "Feb 28, 2026 - Mar 1, 2026"
    dates = extract_dates_from_text(text)
    assert len(dates) >= 2
    date_strings = [d.date().isoformat() for d in dates]
    assert "2026-02-28" in date_strings
    assert "2026-03-01" in date_strings


def test_extract_deduplicate_dates():
    """Test that duplicate dates are deduplicated."""
    text = """
    First mention: Nov 15, 2025
    Second mention: November 15, 2025
    Third mention: 2025-11-15
    """
    dates = extract_dates_from_text(text)
    # Should have only 1 unique date
    date_strings = [d.date().isoformat() for d in dates]
    assert date_strings.count("2025-11-15") == 1


def test_extract_dates_sorted():
    """Test that extracted dates are sorted."""
    text = """
    Last: Dec 31, 2026
    First: Jan 1, 2026
    Middle: June 15, 2026
    """
    dates = extract_dates_from_text(text)
    assert dates == sorted(dates)


def test_date_regex_matches_month_day_year():
    """Test DATE_REGEX matches 'Month Day, Year' format."""
    text = "Nov 15, 2025"
    matches = list(DATE_REGEX.finditer(text))
    assert len(matches) == 1
    assert matches[0].group(0) == "Nov 15, 2025"


def test_date_regex_matches_iso_format():
    """Test DATE_REGEX matches ISO format."""
    text = "2025-11-15"
    matches = list(DATE_REGEX.finditer(text))
    assert len(matches) == 1
    assert matches[0].group(0) == "2025-11-15"


def test_date_regex_matches_day_month_year():
    """Test DATE_REGEX matches 'Day Month Year' format."""
    text = "15 November 2025"
    matches = list(DATE_REGEX.finditer(text))
    assert len(matches) == 1
    assert matches[0].group(0) == "15 November 2025"


def test_date_regex_case_insensitive():
    """Test DATE_REGEX is case insensitive."""
    text = "JANUARY 1, 2026"
    matches = list(DATE_REGEX.finditer(text))
    assert len(matches) == 1


def test_extract_month_without_year():
    """Test extraction of month/day without year (should use current/future year)."""
    text = "Deadline: Nov 15"
    dates = extract_dates_from_text(text)
    # Should have at least one date
    assert len(dates) > 0
    # Date should be a future date
    assert dates[0].date() >= datetime.utcnow().date()
