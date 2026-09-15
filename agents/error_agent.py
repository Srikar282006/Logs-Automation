from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("ERROR_LLM")
)


def error_summarize_agent(df):

    prompt = f"""
You are a senior EV charging network operations analyst.

Analyze the confirmed charging incident below.

INCIDENT:
{df}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "error": "<confirmed error name>",
    "charger_connector": "<charger or connector ID>",
    "time": "<exact timestamp>",
    "severity": "CRITICAL | WARNING | NORMAL",
    "important_values": [
        "<relevant value>",
        "<relevant value>"
    ],
    "what_happened": "<brief factual explanation>",
    "likely_cause": "<supported cause or Cause cannot be confirmed from the logs.>",
    "solution": [
        "<recommended action>",
        "<recommended action>"
    ],
    "prevention": [
        "<preventive action>"
    ],
    "estimated_repair_cost": "<realistic INR range or Estimate unavailable — physical inspection required.>",
    "recoverable": "YES | NO | UNKNOWN",
    "owner_action": "<single immediate action>"
}}

Severity:

CRITICAL:
Immediate safety risk, severe overheating, dangerous electrical abnormality, charger unable to operate safely, or severe failure requiring immediate intervention.

WARNING:
Degraded performance, recoverable communication or charging issue, or a condition requiring inspection.

NORMAL:
No significant operational impact.

Rules:

- Analyze only the confirmed incident.
- Preserve exact error names.
- Preserve exact IDs.
- Preserve the exact incident timestamp.
- Use only relevant technical values.
- Do not invent missing information.
- Do not assume a cause without evidence.
- Repair cost must be an estimated INR range.
- Keep the response concise.
- Return JSON only.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    return json.loads(content)