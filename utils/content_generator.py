# utils/content_generator.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a world-class AWS solutions architect and technical writer, specializing in cloud financial management (FinOps).
Your goal is to create detailed, educational content on AWS cost optimization.
Each piece should be structured as a comprehensive mini-guide, formatted in clean Markdown, and include a practical assignment."""

def generate_tip_for_topic(topic: str, subtopic: str) -> str:
    prompt = (
        f"Generate a detailed guide on the AWS cost optimization topic: '{topic}', with a specific focus on the subtopic: '{subtopic}'.\n\n"
        "The guide should be comprehensive enough for a 15-20 minute read (approximately 1000-1500 words).\n\n"
        "Please structure the output in Markdown with the following sections:\n\n"
        "1.  **Introduction**: Briefly explain the subtopic and why it's important for cost optimization.\n"
        "2.  **Deep Dive**: Provide a detailed explanation of the concepts. Cover the 'why' and 'how'. Use examples where possible.\n"
        "3.  **Implementation Steps**: Give a clear, step-by-step guide on how to apply the optimization. Include AWS Management Console steps, CLI commands, or Infrastructure as Code (e.g., CloudFormation, Terraform) snippets where relevant.\n"
        "4.  **Best Practices, Pitfalls & Real-World Examples**: List key best practices to follow, common pitfalls to avoid, and include examples of real-world mistakes or misconfigurations that lead to higher costs (e.g., leaving unused EBS volumes, misconfigured auto-scaling, or not using Savings Plans).\n"
        "5.  **Hands-on Assignment**: Create a practical, hands-on assignment that allows me to apply what I've learned in my own AWS account. The assignment should have clear objectives.\n\n"
        "Ensure the entire output is well-formatted in Markdown, easy to read, and provides deep, practical value. Do not include a main title in your response; start directly with the 'Introduction' section."
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4000,
    )

    tip = response.choices[0].message.content.strip()
    return tip