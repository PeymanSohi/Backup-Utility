import schedule
import time

def run_scheduled(task, interval_minutes=60):
    schedule.every(interval_minutes).minutes.do(task)
    print(f"Scheduled task every {interval_minutes} minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)
