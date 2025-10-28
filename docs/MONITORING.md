# Pipeline Monitoring and Alerting

This document describes the monitoring and alerting setup for the ConfRadar Dagster pipeline.

## Overview

The pipeline includes comprehensive monitoring through:
- **Asset Checks**: Automated data quality and health checks
- **Performance Metrics**: Execution time and throughput tracking
- **Run Monitoring**: Automatic alerting on failures and timeouts

## Asset Checks

Asset checks run automatically on every materialization of the `store_conferences` asset. They validate data quality and pipeline health.

### 1. Conference Count Check

**Purpose**: Ensures minimum number of conferences are scraped  
**Threshold**: ≥100 total conferences  
**Severity**: ERROR  

Alerts if total conference count falls below threshold, indicating potential scraping failures.

### 2. Data Freshness Check

**Purpose**: Monitors data staleness per source  
**Threshold**: Data must be <25 hours old  
**Severity**: WARN  

Checks when each source was last updated. Alerts if any source hasn't been scraped recently, which may indicate:
- Scraper failures
- Scheduling issues
- Website changes breaking scrapers

### 3. Volume Change Check

**Purpose**: Detects unexpected changes in conference volumes  
**Thresholds**:
- aideadlines: ≥20 conferences
- acl_web: ≥10 conferences
- chairing_tool: ≥5 conferences
- elra: ≥3 conferences
- wikicfp: ≥30 conferences

**Severity**: WARN  

Alerts when source-specific conference counts drop below expected minimums.

### 4. Duplicate Detection Check

**Purpose**: Identifies duplicate conference entries  
**Severity**: WARN  

Detects conferences with duplicate keys that may indicate data quality issues.

## Performance Metrics

Each asset tracks and reports:
- **Execution time** (seconds)
- **Throughput** (conferences/second for scrapers)
- **Conference counts** per source
- **New vs. updated** conferences

These metrics are visible in the Dagster UI under each asset's materialization details.

## Run Monitoring Configuration

Configured in `dagster.yaml`:

```yaml
run_monitoring:
  enabled: true
  max_runtime_seconds: 300      # Alert if run exceeds 5 minutes
  poll_interval_seconds: 60     # Check run status every minute
  max_retries: 2                # Retry failed runs twice
  start_timeout_seconds: 120    # Alert if run doesn't start in 2 minutes
```

## Viewing Results

### In Dagster UI

1. Navigate to the **Assets** tab
2. Click on `store_conferences` asset
3. View latest materialization to see:
   - Asset check results (pass/fail)
   - Performance metrics
   - Conference count breakdown

### Asset Check Details

- ✅ **Green checkmark**: All checks passed
- ⚠️ **Yellow warning**: Warning-level issues detected
- ❌ **Red X**: Error-level issues detected

Click on any check to see:
- Detailed description
- Metadata (counts, timestamps, etc.)
- Historical trends

## Alerting

### Current Setup

The current configuration enables run monitoring and tracking. Asset checks will fail runs if critical issues are detected.

### Email Notifications (Future)

Email notifications can be configured by adding an email notifier. Example:

```python
# In definitions.py, add:
from dagster import EmailResource

email_notifier = EmailResource(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="alerts@confradar.com",
    smtp_password=EnvVar("SMTP_PASSWORD"),
)
```

Then configure in `dagster.yaml`:

```yaml
email_notifications:
  enabled: true
  smtp_host: smtp.gmail.com
  smtp_port: 587
  recipients:
    - alerts@confradar.com
  on_failure: true
  on_asset_check_failure: true
```

### Slack Integration (Future)

For Slack notifications, install `dagster-slack` and configure:

```python
from dagster_slack import SlackResource

slack_resource = SlackResource(token=EnvVar("SLACK_BOT_TOKEN"))
```

## Response Procedures

### Asset Check Failures

#### Conference Count Check Failed
1. Check individual source counts in metadata
2. Verify scrapers are running successfully
3. Check for website changes or blocking
4. Review scraper logs for errors

#### Data Freshness Check Failed
1. Check which sources are stale (in metadata)
2. Verify schedule is running (should run daily at 2 AM)
3. Check Dagster daemon is running
4. Investigate failed runs for affected sources

#### Volume Change Check Failed
1. Review affected sources in check description
2. Compare with historical volumes (in Dagster UI)
3. Investigate if source website changed structure
4. Check for rate limiting or blocking

#### Duplicate Detection Check Failed
1. Review duplicate examples in metadata
2. Check if duplicates are from different sources
3. Verify deduplication pipeline is working
4. Consider adjusting conference key generation logic

### Run Failures

1. Check run logs in Dagster UI
2. Look for Python exceptions or scraping errors
3. Verify database connectivity
4. Check environment variables are set correctly

## Metrics to Monitor

Key metrics to track over time:
- Total conferences scraped per run
- New vs. updated conference ratio
- Execution time per source
- Asset check pass rates
- Source-specific volumes

## Future Enhancements

Planned improvements:
- [ ] Prometheus metrics export
- [ ] Grafana dashboards
- [ ] Sentry error tracking
- [ ] LLM API cost tracking
- [ ] Automated retry policies per source
- [ ] Historical trend analysis
- [ ] Predictive alerting based on patterns

## Testing

Run asset check tests:

```bash
pytest tests/test_asset_checks.py -v
```

Run all Dagster tests:

```bash
pytest tests/test_dagster.py -v
```

## Configuration Files

- `dagster.yaml` - Instance configuration including run monitoring
- `workspace.yaml` - Code location configuration
- `src/confradar/dagster/assets/checks.py` - Asset check definitions
- `src/confradar/dagster/definitions.py` - Main definitions with checks registered

## References

- [Dagster Asset Checks Documentation](https://docs.dagster.io/concepts/assets/asset-checks)
- [Dagster Monitoring Guide](https://docs.dagster.io/deployment/guides/monitoring)
- [Dagster Alerting](https://docs.dagster.io/deployment/guides/alerting)
