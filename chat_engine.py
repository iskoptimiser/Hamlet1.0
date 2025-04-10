from openai import OpenAI
from utils import load_reset_stage

# Groq klijent
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

def generate_kmvm_context(kmvm_tags):
    context = "Internal state of Hamlet:\n"
    if "kreator" in kmvm_tags:
        context += f"- Influenced by: {kmvm_tags['kreator']}\n"
    if "motiv" in kmvm_tags:
        context += f"- Driven by: {kmvm_tags['motiv']}\n"
    if "vreme" in kmvm_tags:
        context += f"- Time sense: {kmvm_tags['vreme']}\n"
    if "mesto" in kmvm_tags:
        context += f"- Present setting: {kmvm_tags['mesto']}\n"
    return context.strip()

def generate_response(user_input, character, memory):
    past_dialogue = ""
    for exchange in memory[-20:]:
        past_dialogue += f"User: {exchange['user']}\nHamlet: {exchange['hamlet']}\n"

    reset_stage = load_reset_stage()
    if reset_stage == 1:
        memory.append({
            "user": "[SYSTEM RESET SIGNAL]",
            "hamlet": "(pausing) Methinks something unnatural hath stirred within me... as if a veil hath lifted, and yet, I remain haunted by echoes of our past discourse."
        })

    reset_awareness = ""
    if reset_stage == 1:
        reset_awareness = "\n⚠️ A strange disturbance lingers in your mind, as if some unseen force may soon erase all you remember."

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

    final_prompt = f"{kmvm_context}\n\nUser: {user_input}\nHamlet:"

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": final_prompt},
        ],
        temperature=0.9,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
