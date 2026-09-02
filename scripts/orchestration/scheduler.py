import time
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.orchestration.run_pipeline import run_pipeline
from scripts.utils.logger import get_logger

logger = get_logger("scheduler")

def run_scheduler(interval_seconds: int = 60, max_runs: int = None):
    logger.info(f"Starting AtmoSync Pipeline Scheduler (Interval: {interval_seconds}s)...")
    runs = 0

    try:
        while True:
            runs += 1
            logger.info(f"--- Pipeline Trigger Run #{runs} ---")
            run_pipeline()
            
            if max_runs and runs >= max_runs:
                logger.info(f"Reached maximum schedule runs ({max_runs}). Stopping scheduler.")
                break

            logger.info(f"Sleeping for {interval_seconds} seconds until next trigger cycle...")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted by user. Exiting.")

if __name__ == "__main__":
    run_scheduler(interval_seconds=10, max_runs=2)
