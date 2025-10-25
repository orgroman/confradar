from confradar.parsers.dates import extract_dates_from_text


def test_extract_simple_month_name_date():
    text = "Submission Deadline: Nov 15, 2025 (AoE)"
    dates = extract_dates_from_text(text)
    assert any(d.date().isoformat() == "2025-11-15" for d in dates)


def test_extract_iso_date():
    text = "Notification: 2025-12-20"
    dates = extract_dates_from_text(text)
    assert any(d.date().isoformat() == "2025-12-20" for d in dates)
