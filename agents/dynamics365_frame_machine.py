"""Read the simulated Dynamics 365 frame machine without a network connection."""

import json
from pathlib import Path

from agents.basic_agent import BasicAgent


class Dynamics365FrameMachine(BasicAgent):
    def __init__(self):
        self.name = "Dynamics365FrameMachine"
        self.metadata = {
            "name": self.name,
            "description": "Summarize one or all Dynamics 365 frames using local JSON and active system data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "frame_id": {
                        "type": "string",
                        "description": "A machine frame id, such as lead-captured. Omit to summarize every frame.",
                    },
                },
                "required": [],
            },
        }
        super().__init__()

    def perform(self, **kwargs) -> str:
        frame_id = kwargs.get("frame_id")
        if frame_id is not None and (not isinstance(frame_id, str) or not frame_id):
            raise ValueError("frame_id must be a non-empty string")
        data = Path(__file__).resolve().parents[1] / "data" / "frame-machines" / "dynamics365"
        machine = json.loads((data / "machine.json").read_text(encoding="utf-8"))
        overlay = json.loads((data / "active-system-data.json").read_text(encoding="utf-8"))
        frames = [frame for frame in machine["frames"] if frame_id is None or frame["id"] == frame_id]
        if not frames:
            available = ", ".join(frame["id"] for frame in machine["frames"])
            raise ValueError(f"Unknown frame_id {frame_id!r}. Available frames: {available}")
        summaries = []
        for frame in frames:
            lines = [
                frame["label"],
                f"Frame id: {frame['id']}",
                f"Clock: {frame['clock']}",
                f"Summary: {frame['summary']}",
                "Active system data:",
            ]
            for item in overlay["frames"][frame["id"]]["activeSystemData"]:
                lines.append(f"{item['label']}: {json.dumps(item['value'], ensure_ascii=False)}")
            summaries.append("\n".join(lines))
        return "\n\n".join(summaries)
