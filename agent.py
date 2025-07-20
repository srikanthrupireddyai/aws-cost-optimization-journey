import json
import requests
from datetime import datetime
from pathlib import Path
from utils.topic_scheduler import get_today_topic, update_run_tracker
from utils.content_generator import generate_tip_for_topic
from utils.file_writer import write_tip_to_github
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# --- CONFIG FILES ---
ROOT_DIR = Path(__file__).parent
CONFIG_DIR = ROOT_DIR / "config"
SCHEDULE_CONFIG_PATH = CONFIG_DIR / "schedule_config.json"
RUN_TRACKER_PATH = CONFIG_DIR / "run_tracker.json"
TIPS_DIR = ROOT_DIR / "daily-tips"

# --- SLACK ---
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # Replace with your actual webhook URL
GITHUB_REPOSITORY_URL = os.getenv("GITHUB_REPOSITORY_URL")

def post_to_slack(message: str, webhook_url: str):
    """Posts a message to a Slack channel via webhook and raises on failure."""
    if not webhook_url:
        print("⚠️ SLACK_WEBHOOK_URL not set. Skipping post to Slack.")
        return

    # Use Slack's Block Kit for better formatting control
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ],
        "text": message  # Fallback for notifications and older clients
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        print("✅ Successfully posted to Slack")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to post to Slack: {e}")
        raise  # Re-raise the exception to be caught by the main workflow

# --- MAIN WORKFLOW ---
def run_daily_agent():
    """
    Main workflow for the daily agent.
    It gets a topic, generates a tip, posts it to Slack and GitHub,
    and only updates the tracker if all steps succeed.
    """
    # Check if a tip for today has already been generated to prevent duplicates
    date_str = datetime.today().strftime("%Y-%m-%d")
    todays_tip_path = TIPS_DIR / f"{date_str}.md"

    if todays_tip_path.exists():
        print(f"✅ Tip for {date_str} already exists. Exiting gracefully.")
        sys.exit(0)

    try:
        topic, subtopic = get_today_topic(SCHEDULE_CONFIG_PATH, RUN_TRACKER_PATH)
        print(f"📌 Today's Topic: {topic} / {subtopic}")

        # Generate tip
        generated_tip = generate_tip_for_topic(topic, subtopic)
        print("🧠 Tip Generated")

        # Write to GitHub first, so we can link to it
        write_tip_to_github(topic, subtopic, generated_tip, TIPS_DIR)
        print("📘 Tip written to GitHub")

        # Post a summary to Slack with a link to the new tip
        if not GITHUB_REPOSITORY_URL:
            print("⚠️ GITHUB_REPOSITORY_URL not set. Cannot generate link for Slack message.")
            slack_message = f"✅ New AWS Cost Tip Generated: *{topic} / {subtopic}*"
        else:
            tip_url = f"{GITHUB_REPOSITORY_URL.strip('/')}/blob/main/{TIPS_DIR.name}/{todays_tip_path.name}"
            slack_message = (
                f"💡 *New AWS Cost Optimization Tip Published!*\n\n"
                f"*{topic} → {subtopic}*\n\n"
                f"Read the full guide here: {tip_url}"
            )
        post_to_slack(slack_message, SLACK_WEBHOOK_URL)

        # Update run tracker ONLY if all steps were successful
        update_run_tracker(SCHEDULE_CONFIG_PATH, RUN_TRACKER_PATH)
    except Exception as e:
        print(f"\n--- ❌ WORKFLOW FAILED ---")
        print(f"An error occurred: {e}")
        print("🛑 The run tracker has NOT been updated. The same topic will be retried on the next run.")
        sys.exit(1)

if __name__ == "__main__":
    run_daily_agent()
