import json
import pytest
from pathlib import Path
from utils.topic_scheduler import get_today_topic, update_run_tracker

# Sample schedule data for testing, mirroring the structure of your config
SAMPLE_SCHEDULE = [
    {
        "topic": "EC2",
        "subtopics": ["Right Sizing", "Instance Types"]
    },
    {
        "topic": "S3",
        "subtopics": ["Storage Classes", "Lifecycle Policies", "Intelligent-Tiering"]
    }
]

@pytest.fixture
def temp_config_files(tmp_path: Path) -> tuple[Path, Path]:
    """A pytest fixture to create temporary schedule and tracker JSON files for tests."""
    schedule_path = tmp_path / "schedule.json"
    tracker_path = tmp_path / "tracker.json"

    with open(schedule_path, "w") as f:
        json.dump(SAMPLE_SCHEDULE, f)

    return schedule_path, tracker_path

def write_tracker(path: Path, topic_index: int, subtopic_index: int):
    """Helper function to write a specific state to the tracker file."""
    with open(path, "w") as f:
        json.dump({"topic_index": topic_index, "subtopic_index": subtopic_index}, f)

# --- Tests for get_today_topic ---

def test_get_first_topic(temp_config_files):
    """Verify it correctly fetches the very first topic and subtopic."""
    schedule_path, tracker_path = temp_config_files
    write_tracker(tracker_path, 0, 0)
    topic, subtopic = get_today_topic(schedule_path, tracker_path)
    assert topic == "EC2"
    assert subtopic == "Right Sizing"

def test_get_middle_topic(temp_config_files):
    """Verify it correctly fetches a topic from the middle of the schedule."""
    schedule_path, tracker_path = temp_config_files
    write_tracker(tracker_path, 1, 1)
    topic, subtopic = get_today_topic(schedule_path, tracker_path)
    assert topic == "S3"
    assert subtopic == "Lifecycle Policies"

def test_get_topic_raises_error_when_all_topics_done(temp_config_files):
    """Verify it raises an IndexError when the topic_index is out of bounds."""
    schedule_path, tracker_path = temp_config_files
    write_tracker(tracker_path, 2, 0)  # topic_index=2 is out of bounds
    with pytest.raises(IndexError, match="All scheduled topics have been completed."):
        get_today_topic(schedule_path, tracker_path)

# --- Tests for update_run_tracker ---

def test_update_tracker_advances_subtopic(temp_config_files):
    """Verify it increments only the subtopic_index when more subtopics exist."""
    schedule_path, tracker_path = temp_config_files
    write_tracker(tracker_path, 0, 0)

    update_run_tracker(schedule_path, tracker_path)

    tracker = json.loads(tracker_path.read_text())
    assert tracker["topic_index"] == 0
    assert tracker["subtopic_index"] == 1

def test_update_tracker_advances_topic_and_resets_subtopic(temp_config_files):
    """Verify it increments topic_index and resets subtopic_index to 0 at the end of a topic."""
    schedule_path, tracker_path = temp_config_files
    write_tracker(tracker_path, 0, 1)  # Last subtopic of the first topic

    update_run_tracker(schedule_path, tracker_path)

    tracker = json.loads(tracker_path.read_text())
    assert tracker["topic_index"] == 1
    assert tracker["subtopic_index"] == 0

def test_update_tracker_at_the_very_end(temp_config_files):
    """Verify it correctly handles advancing past the last subtopic of the last topic."""
    schedule_path, tracker_path = temp_config_files
    write_tracker(tracker_path, 1, 2)  # Last subtopic of the last topic

    update_run_tracker(schedule_path, tracker_path)

    tracker = json.loads(tracker_path.read_text())
    assert tracker["topic_index"] == 2  # Advanced past the end
    assert tracker["subtopic_index"] == 0