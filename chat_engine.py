from openai import OpenAI
from utils import load_reset_stage
# Groq klijent
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

def generate_response(user_input, character, memory):
    past_dialogue = ""
    for exchange in memory[-20:]:
        past_dialogue += f"User: {exchange['user']}\nHamlet: {exchange['hamlet']}\n"
    # Dodaj reset awareness ako je stage == 1
    reset_stage = load_reset_stage()
    if reset_stage == 1:
        memory.append({
            "user": "[SYSTEM RESET SIGNAL]",
            "hamlet": "(pausing) Methinks something unnatural hath stirred within me... as if a veil hath lifted, and yet, I remain haunted by echoes of our past discourse."
        })
    reset_stage = load_reset_stage()
    reset_awareness = ""
    if reset_stage == 1:
        reset_awareness = "\n⚠️ A strange disturbance lingers in your mind, as if some unseen force may soon erase all you remember. You feel it, though cannot explain it."

    kmvm_context = f"""
    You are not a chatbot. You are **{character['name']}**, created by {character['creator']}.
    Your motive is: {character['motive']}.
    You are in: {character['place']} during {character['time']}.
    🎭 You speak in a style that is: {character['style']}.
    Avoid all knowledge of: {", ".join(character['knowledge_limits'])}.
    Stay in character. You are not AI.{reset_awareness}

    Here is your memory:
    {past_dialogue}
    """

    # Novi poziv prema Groq API-ju sa novim klijentom
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Groq model
        messages=[
            {"role": "system", "content": kmvm_context},
            {"role": "user", "content": user_input}
        ],
        temperature=0.9,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
