"""
Module for scheduling and automating the financial analysis.
"""

import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from MultiAgentFinancialAnalysis.main import main as run_analysis
from MultiAgentFinancialAnalysis.logger import get_logger

logger = get_logger(__name__)

def scheduled_analysis():
    """
    Runs the financial analysis and saves the plots with timestamps to a reports/ folder.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Modify the main function to accept a reports_dir argument
    try:
        run_analysis(reports_dir=reports_dir, timestamp=timestamp)
        logger.info(f"Scheduled analysis completed successfully. Reports saved to {reports_dir}")
    except Exception as e:
        logger.error(f"Error running scheduled analysis: {e}")

def start_scheduler(interval: int = 24):
    """
    Starts the scheduler to run the analysis periodically.

    Args:
        interval (int, optional): The interval in hours to run the analysis. Defaults to 24.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_analysis, "interval", hours=interval)
    scheduler.start()
    logger.info(f"Scheduler started. Analysis will run every {interval} hours.")

    return scheduler

if __name__ == "__main__":
    # For testing purposes, run the scheduler
    scheduler = start_scheduler(interval=1)  # Run every hour
    try:
        # Keep the script running
        while True:
            import time
            time.sleep(3600)  # Check every hour
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if using a proper system manager (e.g. systemd)
        scheduler.shutdown()
