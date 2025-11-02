"""Dagster definitions - main entry point for the orchestration pipeline.

This module defines all Dagster assets, jobs, schedules, and sensors for ConfRadar.
"""

from dagster import Definitions, ScheduleDefinition, define_asset_job

from confradar.dagster.assets.checks import (
    check_conference_count,
    check_deadline_dates,
    check_duplicate_conferences,
    check_required_fields,
)
from confradar.dagster.assets.scrapers import (
    acl_web_conferences,
    ai_deadlines_conferences,
    chairing_tool_conferences,
    elra_conferences,
    seeded_conferences,
    wikicfp_conferences,
)
from confradar.dagster.assets.storage import store_conferences
from confradar.dagster.sensors import (
    asset_check_failure_alert,
    pipeline_failure_alert,
)

# Define jobs
crawl_job = define_asset_job(
    name="crawl_job",
    description="Daily conference crawling pipeline - scrape all sources and store in database",
)

# Define schedules
daily_crawl_schedule = ScheduleDefinition(
    name="daily_crawl_schedule",
    job=crawl_job,
    cron_schedule="0 * * * *",  # Run once per hour (at minute 0)
    description="Run crawl pipeline once per hour",
)

# Main Definitions object
defs = Definitions(
    assets=[
        seeded_conferences,
        ai_deadlines_conferences,
        acl_web_conferences,
        chairing_tool_conferences,
        elra_conferences,
        wikicfp_conferences,
        store_conferences,
    ],
    asset_checks=[
        check_conference_count,
        check_required_fields,
        check_deadline_dates,
        check_duplicate_conferences,
    ],
    jobs=[crawl_job],
    schedules=[daily_crawl_schedule],
    sensors=[
        pipeline_failure_alert,
        asset_check_failure_alert,
    ],
)
