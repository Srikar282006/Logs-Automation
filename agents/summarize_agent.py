from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_agent(df):
    prompt = f"""
You are an EV Charging Network Operations Analyst.

Your job is to report ONLY what is happening with the EV charging network.

Do NOT describe the provided data, columns, rows, JSON, log structure, or message types.

DATA:
{df}

Report:

1. CURRENT ACTIVITY
- What is happening with the charger.
- Charging activity, stopped charging, connector activity, or other important operational events.
- Mention important values only when they explain what is happening.

2. PROBLEMS
- Report only actual failures, errors, faults, or clearly abnormal behavior.
- For each problem provide:
  - Problem
  - Charger/Connector ID
  - Date and time
  - What is happening
  - Likely cause, only if supported
  - Recommended action
  - Whether it can potentially be resolved

3. OWNER ACTION
- Tell the charger owner what needs attention.
- Prioritize critical problems.
- If everything is operating normally, simply state that no action is required.

4. FINAL STATUS
Return one:
- NORMAL
- WARNING
- CRITICAL

STRICT RULES:
- Never describe the data.
- Never say "the data shows", "the logs contain", "the dataset contains", etc.
- Never explain JSON, columns, rows, or OCPP messages.
- Do not list routine successful events.
- Do not create a timeline of normal events.
- Do not hallucinate.
- Use only information provided.
- Separate confirmed problems from suspected causes.
- Be concise and owner-focused.

Return only the operational update.
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

    return response.choices[0].message.content