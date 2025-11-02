"""Integration test for Dagster orchestration and run visibility."""
import subprocess
import time

def run_dagster_job(job_name="crawl_job"):
    print(f"Launching Dagster job: {job_name}")
    result = subprocess.run([
        "docker", "exec", "dagster-webserver",
        "uv", "run", "dagster", "job", "launch", "-j", job_name
    ], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, f"Dagster job launch failed: {result.stderr}"


def check_dagster_runs():
    print("Checking Dagster runs...")
    result = subprocess.run([
        "docker", "exec", "dagster-webserver",
        "uv", "run", "dagster", "run", "list"
    ], capture_output=True, text=True)
    print(result.stdout)
    assert "crawl_job" in result.stdout, "No crawl_job runs found in Dagster instance."


def main():
    # Launch job manually
    run_dagster_job()
    # Wait for run to be recorded
    time.sleep(10)
    check_dagster_runs()
    print("\n✓ Dagster integration test passed!")

if __name__ == "__main__":
    main()
