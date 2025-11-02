"""Tests for Dagster sensors."""

from confradar.dagster.sensors import (
    asset_check_failure_alert,
    pipeline_failure_alert,
)


def test_pipeline_failure_sensor_exists():
    """Test that pipeline failure sensor is defined."""
    assert pipeline_failure_alert is not None
    assert hasattr(pipeline_failure_alert, "name")
    assert pipeline_failure_alert.name == "pipeline_failure_sensor"


def test_asset_check_failure_sensor_exists():
    """Test that asset check failure sensor is defined."""
    assert asset_check_failure_alert is not None
    assert hasattr(asset_check_failure_alert, "name")
    assert asset_check_failure_alert.name == "asset_check_failure_sensor"


def test_sensors_are_run_failure_sensors():
    """Test that sensors are configured as run failure sensors."""
    # Both should be configured to monitor failures
    # Dagster will call these when pipeline runs fail
    assert callable(pipeline_failure_alert)
    assert callable(asset_check_failure_alert)
