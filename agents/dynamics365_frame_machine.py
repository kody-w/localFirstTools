"""Answer questions about the Dynamics 365 frame ledger using local JSON only."""

import json
from pathlib import Path

from agents.basic_agent import BasicAgent


class Dynamics365FrameMachineAgent(BasicAgent):
    def __init__(self):
        self.name = "Dynamics365FrameMachine"
        self.metadata = {
            "name": self.name,
            "description": (
                "Describe the local Dynamics 365 simulation's frames and active "
                "system data. Omit frame_id to list every frame."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "frame_id": {
                        "type": "string",
                        "description": "Machine frame id, for example lead-captured.",
                    }
                },
                "required": [],
                "additionalProperties": False,
            },
        }
        super().__init__()

    def perform(self, **kwargs) -> str:
        folder = Path(__file__).resolve().parents[1] / "data/frame-machines/dynamics365"
        machine = json.loads((folder / "machine.json").read_text(encoding="utf-8"))
        overlay = json.loads(
            (folder / "active-system-data.json").read_text(encoding="utf-8")
        )
        frame_id = kwargs.get("frame_id")
        frames = machine["frames"]
        if frame_id is not None:
            if not isinstance(frame_id, str) or not frame_id:
                raise ValueError("frame_id must be a nonempty string.")
            frames = [frame for frame in frames if frame["id"] == frame_id]
            if not frames:
                raise ValueError(f"Unknown Dynamics 365 frame_id: {frame_id}")

        answers = []
        for frame in frames:
            values = overlay["frames"][frame["id"]]["activeSystemData"]
            active = "; ".join(
                f'{item["label"]}: {json.dumps(item["value"], ensure_ascii=False)}'
                for item in values
            )
            answers.append(
                f'{frame["label"]} ({frame["id"]})\n'
                f'Clock: {frame["clock"]}\n{frame["summary"]}\n'
                f"Active system data: {active}"
            )
        return "\n\n".join(answers)
