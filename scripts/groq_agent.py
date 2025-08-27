import os
import json
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_drone_commands(user_input, drone_names):
    """
    Sends a user command to the LLM and expects JSON output with
    coordinates for each drone.
    """
    # Ensure drone_names is a list of strings
    if not all(isinstance(name, str) for name in drone_names):
        drone_names = [str(d["drone"]) for d in drone_names]

    prompt = f"""
You are a drone swarm controller. The swarm has {len(drone_names)} drones: {', '.join(drone_names)}.
User command: "{user_input}"
Respond with JSON containing the target x, y, z positions for each drone.
Example format:
{{
    "drone1": {{"x": 0, "y": 0, "z": 10}},
    "drone2": {{"x": 1, "y": 0, "z": 10}},
    "drone3": {{"x": 0, "y": 1, "z": 10}}
}}
Do not include any explanation, only return valid JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_output = response.choices[0].message.content

    try:
        drone_targets = json.loads(raw_output)
    except json.JSONDecodeError:
        print("LLM did not return valid JSON:")
        print(raw_output)
        drone_targets = {}

    return drone_targets
