# utils/topic_scheduler.py
import json
from pathlib import Path

def _load_json(path: Path):
    """Helper to load a JSON file."""
    with open(path) as f:
        return json.load(f)

def _write_json(path: Path, data: dict):
    """Helper to write data to a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_today_topic(schedule_path: Path, tracker_path: Path) -> tuple[str, str]:
    """
    Gets the current topic and subtopic based on the run tracker.
    This function is read-only and does not modify the tracker.
    """
    schedule = _load_json(schedule_path)
    tracker = _load_json(tracker_path)

    topic_index = tracker.get("topic_index", 0)
    subtopic_index = tracker.get("subtopic_index", 0)

    if topic_index >= len(schedule):
        raise IndexError("All scheduled topics have been completed.")

    topic_info = schedule[topic_index]
    topic = topic_info["topic"]
    subtopics = topic_info["subtopics"]

    if subtopic_index >= len(subtopics):
        # This case indicates an inconsistent state. The update function will
        # handle advancing to the next topic, but getting a topic here is an error.
        raise IndexError(f"Subtopic index {subtopic_index} is out of bounds for topic '{topic}'.")

    return topic, subtopics[subtopic_index]

def update_run_tracker(schedule_path: Path, tracker_path: Path):
    """
    Updates the run tracker to point to the next subtopic or topic.
    - Increments the subtopic index.
    - If all subtopics for the current topic are done, it increments the
      topic index and resets the subtopic index to 0.
    """
    schedule = _load_json(schedule_path)
    tracker = _load_json(tracker_path)

    topic_index = tracker.get("topic_index", 0)
    subtopic_index = tracker.get("subtopic_index", 0)

    if topic_index >= len(schedule):
        print("✅ All topics have been processed.")
        return # Nothing more to update

    current_topic_subtopics = schedule[topic_index]["subtopics"]

    # Move to the next subtopic
    next_subtopic_index = subtopic_index + 1

    if next_subtopic_index < len(current_topic_subtopics):
        # We are still within the same topic
        tracker["subtopic_index"] = next_subtopic_index
    else:
        # Move to the next topic and reset subtopic index
        tracker["topic_index"] = topic_index + 1
        tracker["subtopic_index"] = 0

    _write_json(tracker_path, tracker)
    print(f"📈 Run tracker updated to topic_index: {tracker['topic_index']}, subtopic_index: {tracker['subtopic_index']}")