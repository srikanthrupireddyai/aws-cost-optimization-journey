from datetime import datetime
from pathlib import Path

def write_tip_to_github(topic: str, subtopic: str, content: str, tips_dir: Path):
    date_str = datetime.today().strftime("%Y-%m-%d")
    tips_dir.mkdir(exist_ok=True)
    filename = tips_dir / f"{date_str}.md"

    with open(filename, "w") as f:
        f.write(f"# AWS Cost Tip - {date_str}\n")
        f.write(f"**Topic:** {topic}\n")
        f.write(f"**Subtopic:** {subtopic}\n\n")
        f.write(content)
