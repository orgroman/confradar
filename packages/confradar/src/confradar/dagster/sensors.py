"""Dagster sensors for monitoring and alerting.

This module defines sensors that monitor pipeline runs and trigger alerts on failures.
"""

import logging
from typing import Optional

from dagster import (
    DefaultSensorStatus,
    RunFailureSensorContext,
    RunRequest,
    SensorEvaluationContext,
    run_failure_sensor,
    sensor,
)

logger = logging.getLogger(__name__)


@run_failure_sensor(
    name="pipeline_failure_sensor",
    description="Monitors all pipeline runs and logs failures for alerting",
    default_status=DefaultSensorStatus.RUNNING,
)
def pipeline_failure_alert(context: RunFailureSensorContext):
    """Alert on pipeline run failures.
    
    This sensor monitors all Dagster runs and logs detailed failure information.
    Can be extended to send email/Slack notifications.
    
    Args:
        context: Sensor context with failure information
    """
    run_id = context.dagster_run.run_id
    job_name = context.dagster_run.job_name
    failure_event = context.failure_event
    
    # Extract failure details
    error_message = "Unknown error"
    if failure_event and failure_event.event_specific_data:
        error_data = failure_event.event_specific_data
        if hasattr(error_data, "error"):
            error_message = str(error_data.error)
    
    # Log the failure
    logger.error(
        f"Pipeline failure detected:\n"
        f"  Job: {job_name}\n"
        f"  Run ID: {run_id}\n"
        f"  Error: {error_message}"
    )
    
    # TODO: Send email notification
    # Example: send_email_alert(job_name, run_id, error_message)
    
    # TODO: Send Slack notification
    # Example: send_slack_alert(job_name, run_id, error_message)
    
    # Log alert metadata
    context.log.error(
        f"⚠️ ALERT: Pipeline '{job_name}' failed",
        extra={
            "run_id": run_id,
            "job_name": job_name,
            "error": error_message,
        },
    )


@run_failure_sensor(
    name="asset_check_failure_sensor",
    description="Monitors asset check failures and logs quality issues",
    default_status=DefaultSensorStatus.RUNNING,
)
def asset_check_failure_alert(context: RunFailureSensorContext):
    """Alert on asset check failures.
    
    This sensor specifically monitors asset checks (data quality validations)
    and logs when checks fail, indicating data quality issues.
    
    Args:
        context: Sensor context with failure information
    """
    run_id = context.dagster_run.run_id
    job_name = context.dagster_run.job_name
    
    # Only alert on asset check failures (not regular asset materializations)
    if "check" not in job_name.lower():
        return
    
    failure_event = context.failure_event
    error_message = "Asset check failed"
    
    if failure_event and failure_event.event_specific_data:
        error_data = failure_event.event_specific_data
        if hasattr(error_data, "error"):
            error_message = str(error_data.error)
    
    logger.warning(
        f"Asset check failure detected:\n"
        f"  Check: {job_name}\n"
        f"  Run ID: {run_id}\n"
        f"  Issue: {error_message}"
    )
    
    context.log.warning(
        f"⚠️ DATA QUALITY ALERT: Asset check '{job_name}' failed",
        extra={
            "run_id": run_id,
            "job_name": job_name,
            "error": error_message,
        },
    )


# Helper functions for future email/Slack integration
def send_email_alert(job_name: str, run_id: str, error: str) -> None:
    """Send email alert for pipeline failure.
    
    TODO: Implement email sending logic using SMTP or email service.
    
    Args:
        job_name: Name of the failed job
        run_id: Dagster run ID
        error: Error message
    """
    # Example implementation:
    # import smtplib
    # from email.message import EmailMessage
    # 
    # msg = EmailMessage()
    # msg['Subject'] = f'[ConfRadar] Pipeline Failure: {job_name}'
    # msg['From'] = 'alerts@confradar.com'
    # msg['To'] = 'team@confradar.com'
    # msg.set_content(f'Job {job_name} failed.\nRun ID: {run_id}\nError: {error}')
    # 
    # with smtplib.SMTP('localhost') as s:
    #     s.send_message(msg)
    pass


def send_slack_alert(job_name: str, run_id: str, error: str) -> None:
    """Send Slack alert for pipeline failure.
    
    TODO: Implement Slack webhook integration.
    
    Args:
        job_name: Name of the failed job
        run_id: Dagster run ID
        error: Error message
    """
    # Example implementation:
    # import requests
    # 
    # webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    # payload = {
    #     'text': f'🚨 *Pipeline Failure: {job_name}*\nRun ID: {run_id}\nError: {error}',
    #     'username': 'ConfRadar Alerts',
    # }
    # requests.post(webhook_url, json=payload)
    pass
