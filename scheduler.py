import os
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

from agents.summarize_agent import summarize_agent
from agents.mail_agent import send_mail


def generate_daily_summary():
    normal_file = "logs_data/normal/normal_logs.csv"

    if not os.path.exists(normal_file):
        print("No normal logs found.")
        return

    df = pd.read_csv(normal_file)

    if df.empty:
        print("Normal logs are empty.")
        return

    print("Generating daily summary...")

    summary = summarize_agent(df)

    result = send_mail.invoke({
        "subject": "EV Charging Network - Daily Summary",
        "body": summary,
        "receiver": os.getenv("OWNER_EMAIL")
    })

    print(result)


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        generate_daily_summary,
        "cron",
        hour=0,
        minute=0
    )

    scheduler.start()

    print("Scheduler started. Daily summary will run at 12:00 AM.")

    return scheduler