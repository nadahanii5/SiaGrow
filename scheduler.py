import subprocess
import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler


def run():
    print(f"\n=== Pipeline run at {datetime.now():%Y-%m-%d %H:%M:%S} ===")
    subprocess.run([sys.executable, "run_pipeline.py"])


run()  

scheduler = BlockingScheduler()
scheduler.add_job(run, "interval", minutes=1) 
print("Scheduler started. Press Ctrl+C to stop.")
scheduler.start()