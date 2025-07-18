# utils/topic_scheduler.py
import json
from datetime import datetime


def get_today_topic(schedule_path, tracker_path):
    with open(schedule_path) as f:
        schedule = json.load(f)

    with open(tracker_path) as f:
        tracker = json.load(f)

    current_day_index = tracker.get("day_index", 0)
    current_sub_index = tracker.get("sub_index", 0)

    if current_day_index >= len(schedule):
        raise Exception("All scheduled topics have been exhausted.")

    topic_info = schedule[current_day_index]
    topic = topic_info["topic"]
    subtopics = topic_info["subtopics"]

    if current_sub_index >= len(subtopics):
        # Move to next day
        current_day_index += 1
        current_sub_index = 0

        if current_day_index >= len(schedule):
            raise Exception("No more scheduled topics available.")

        topic_info = schedule[current_day_index]
        topic = topic_info["topic"]
        subtopics = topic_info["subtopics"]

    return topic, subtopics[current_sub_index]


def update_run_tracker(schedule_path, tracker_path):
    with open(schedule_path) as f:
        schedule = json.load(f)

    with open(tracker_path) as f:
        tracker = json.load(f)

    current_day_index = tracker.get("day_index", 0)
    current_sub_index = tracker.get("sub_index", 0)

    subtopics = schedule[current_day_index]["subtopics"]

    if current_sub_index + 1 < len(subtopics):
        tracker["sub_index"] = current_sub_index + 1
    else:
        tracker["day_index"] = current_day_index + 1
        tracker["sub_index"] = 0

    with open(tracker_path, "w") as f:
        json.dump(tracker, f, indent=2)