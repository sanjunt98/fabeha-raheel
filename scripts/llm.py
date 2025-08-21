#!/usr/bin/env python3
import os
from typing import Optional, Literal
from pydantic import BaseModel
from groq import Groq


class SwarmCommand(BaseModel):
    """Defines the structure of commands that can be interpreted by the LLM."""
    action: Literal[
        "takeoff",
        "land",
        "rtl",
        "move_line",
        "move_flock",
        "move_helical",
        "unknown"
    ]
    reason: Optional[str] = None


class LLMInterface:
    """Wrapper for Groq LLM API to interpret user text into swarm commands."""

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key="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")
        self.model = model

    def parse_command(self, user_input: str) -> SwarmCommand:
        """Send natural language input to LLM and return structured command."""

        system_prompt = """
        You are a UAV swarm command interpreter.
        Convert user natural language commands into one of the following actions:
        - takeoff (leader + followers takeoff)
        - land (all UAVs land)
        - rtl (return to launch/home)
        - move_line (switch to line formation)
        - move_flock (switch to flock formation)
        - move_helical (switch to helical formation)
        - unknown (if not possible to interpret)

        If the command cannot be executed, explain why in 'reason'.
        Respond ONLY in JSON following the SwarmCommand schema.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            response_format={"type": "json_object"},
        )

        json_output = response.choices[0].message.content

        try:
            return SwarmCommand.parse_raw(json_output)
        except Exception:
            return SwarmCommand(action="unknown", reason="Could not parse command.")



if __name__ == "__main__":
    llm = LLMInterface()
    cmd = llm.parse_command("move to flock formation")
    print(cmd.json(indent=2))
