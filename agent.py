import json
import requests
from datetime import datetime
from pathlib import Path
from utils.topic_scheduler import get_today_topic, update_run_tracker
from utils.content_generator import generate_tip_for_topic
from utils.file_writer import write_tip_to_github
from dotenv import load_dotenv
import os

load_dotenv()

# --- CONFIG FILES ---
CONFIG_DIR = Path(__file__).parent / "config"
SCHEDULE_CONFIG_PATH = CONFIG_DIR / "schedule_config.json"
RUN_TRACKER_PATH = CONFIG_DIR / "run_tracker.json"

# --- SLACK ---
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # Replace with your actual webhook URL

def post_to_slack(message: str, webhook_url: str):
    payload = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("✅ Successfully posted to Slack")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to post to Slack: {e}")

# --- MAIN WORKFLOW ---
def run_daily_agent():
    topic, subtopic = get_today_topic(SCHEDULE_CONFIG_PATH, RUN_TRACKER_PATH)
    print(f"📌 Today's Topic: {topic} / {subtopic}")

    # Generate tip
    generated_tip = generate_tip_for_topic(topic, subtopic)
    print("🧠 Tip Generated")

    # Post to Slack
    post_to_slack(generated_tip, SLACK_WEBHOOK_URL)

    # Write to GitHub
    write_tip_to_github(topic, subtopic, generated_tip)
    print("📘 Tip written to GitHub")

    # Update run tracker
    update_run_tracker(SCHEDULE_CONFIG_PATH, RUN_TRACKER_PATH)

if __name__ == "__main__":
    run_daily_agent()
