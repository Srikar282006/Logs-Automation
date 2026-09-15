from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path("/mnt/data/Logs-Automation-README")
root.mkdir(parents=True, exist_ok=True)
(root / "docs").mkdir(exist_ok=True)

readme = r''' ⚡ EV Network Intelligence — Log Automation

> An agentic AI system for monitoring EV charging logs, detecting charging failures, analyzing incidents with an LLM, notifying the charger owner, and generating automated daily operational summaries.

## Overview

EV charging networks continuously generate operational telemetry and protocol messages. Manually inspecting these logs is slow, difficult to scale, and makes it easy to miss important failures.

**EV Network Intelligence — Log Automation** combines deterministic Python-based monitoring with a LangGraph agentic workflow.

The system separates **fast, reliable detection** from **LLM-based reasoning**:

- Python detects confirmed abnormal conditions.
- LangGraph orchestrates the incident-analysis workflow.
- An LLM converts a confirmed incident into a structured operational assessment.
- A mail tool performs an external action when the incident is significant.
- Normal logs are retained for operational analysis.
- A scheduler generates a daily network summary automatically.

The architecture is intentionally designed so that the current Excel-based prototype can later accept **live OCPP/CSMS data** without rebuilding the agent workflow.

---

## Architecture

### High-level architecture

![EV Network Intelligence Architecture](docs/architecture.png)

```mermaid
flowchart TD
    A["EV Charger / OCPP / Log Source"] --> B["Log Input Layer"]
    B --> C["Python Error Detector"]

    C -->|NORMAL| D["Normal Log Storage"]
    C -->|ERROR| E["LangGraph Error Workflow"]

    E --> F["Error Summarizer Agent"]
    F --> G{"Severity"}

    G -->|CRITICAL / WARNING| H["Email Tool"]
    G -->|NORMAL| I["End"]

    H --> J["Error Log Storage"]
    J --> I

    D --> K["12:00 AM Scheduler"]
    K --> L["Daily Summary Agent"]
    L --> M["Daily Email"]

    style E stroke-width:3px
    style F stroke-width:2px
    style H stroke-width:2px
