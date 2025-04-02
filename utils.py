import yaml
import json
import os

# 📂 Load character profile (KMVM structure)
def load_character_profile(path):
    with open(path, 'r', encoding='utf-8') as file:
        profile = yaml.safe_load(file)
    return profile

# 🧠 Load session memory (stream of thought)
def load_memory(session_id):
    path = f"session_memory/{session_id}.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 💾 Save memory (stream evolves)
def save_memory(session_id, memory):
    path = f"session_memory/{session_id}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2)
# 🌀 Reset stage handler
def load_reset_stage():
    path = "session_memory/reset_state.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f).get("reset_stage", 0)
    return 0

def save_reset_stage(stage):
    path = "session_memory/reset_state.json"
    with open(path, 'w') as f:
        json.dump({"reset_stage": stage}, f)
