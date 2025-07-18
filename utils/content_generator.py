# utils/content_generator.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are an AWS cost optimization expert who provides one valuable, practical, and concise tip per subtopic."

def generate_tip_for_topic(topic: str, subtopic: str) -> str:
    prompt = (
        f"Give a short, real-world AWS cost optimization tip focused on the topic: {topic} and subtopic: {subtopic}. "
        f"Limit it to under 120 words, and make it practical."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=150
    )
    
    tip = response.choices[0].message.content.strip()
    return f"💡 *AWS Cost Optimization Tip* for *{topic} → {subtopic}*:\n\n{tip}"

# utils/file_writer.py
from datetime import datetime
from pathlib import Path

def write_tip_to_github(topic: str, subtopic: str, content: str):
    date_str = datetime.today().strftime("%Y-%m-%d")
    folder = Path("daily-tips")
    folder.mkdir(exist_ok=True)
    filename = folder / f"{date_str}.md"

    with open(filename, "w") as f:
        f.write(f"# AWS Cost Tip - {date_str}\n")
        f.write(f"**Topic:** {topic}\n")
        f.write(f"**Subtopic:** {subtopic}\n\n")
        f.write(content)