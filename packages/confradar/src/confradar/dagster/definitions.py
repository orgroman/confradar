"""Dagster definitions - main entry point for the orchestration pipeline.

This module defines all Dagster assets, jobs, schedules, and sensors for ConfRadar.
"""

from dagster import Definitions, ScheduleDefinition, define_asset_job

from confradar.dagster.assets.checks import (
    conference_count_check,
    data_freshness_check,
    duplicate_detection_check,
    volume_change_check,
)
from confradar.dagster.assets.scrapers import (
    acl_web_conferences,
    ai_deadlines_conferences,
    chairing_tool_conferences,
    elra_conferences,
    wikicfp_conferences,
)
from confradar.dagster.assets.storage import store_conferences

# Define jobs
crawl_job = define_asset_job(
    name="crawl_job",
    description="Daily conference crawling pipeline - scrape all sources and store in database",
)

# Define schedules
daily_crawl_schedule = ScheduleDefinition(
    name="daily_crawl_schedule",
    job=crawl_job,
    cron_schedule="0 2 * * *",  # Run at 2 AM daily
    description="Run daily conference crawl pipeline",
)

# Main Definitions object
defs = Definitions(
    assets=[
        ai_deadlines_conferences,
        acl_web_conferences,
        chairing_tool_conferences,
        elra_conferences,
        wikicfp_conferences,
        store_conferences,
    ],
    asset_checks=[
        conference_count_check,
        data_freshness_check,
        volume_change_check,
        duplicate_detection_check,
    ],
    jobs=[crawl_job],
    schedules=[daily_crawl_schedule],
)
