from openai import OpenAI
from kmvm_core import KMVMGraph
import json

# Groq klijent
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# Funkcija koja koristi GPT da generiše KMVM tagove
def extract_kmvm(user_input, hamlet_response):
    prompt = f"""
Given the following dialogue:

User: {user_input}
Hamlet: {hamlet_response}

Extract the following KMVM memory tags as JSON:
- "kreator": who initiated this exchange (e.g. "user" or "hamlet")
- "motiv": what is the psychological or narrative motivation
- "vreme": when does this happen in the story (from Hamlet's point of view)
- "mesto": where does this happen emotionally or narratively

Respond ONLY with valid JSON.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a KMVM extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=170
    )

    return json.loads(response.choices[0].message.content.strip())


# Glavna funkcija koja generiše Hamletov odgovor + KMVM memoriju
def generate_response(user_input, character, kmvm_memory):
    # Rekonstrukcija prošlih interakcija (KMVM kontekstualno)
    past_dialogue = ""
    for mem in kmvm_memory[-10:]:
        past_dialogue += f"Scene ({mem['vreme']}, {mem['mesto']}):\n"
        past_dialogue += f"{mem['kreator']}: {mem['input']}\nHamlet: {mem['response']}\n\n"

    # Glavni prompt kontekst
    kmvm_context = f"""
You are not a chatbot. You are {character['name']}, created by {character['creator']}.
Your motive is: {character['motive']}.
You are in: {character['place']} during {character['time']}.
🎭 Your style: {character['style']}.
Avoid all knowledge of: {", ".join(character['knowledge_limits'])}.

Here is your memory:
{past_dialogue}
"""

    # Generiši Hamletov odgovor
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": kmvm_context},
            {"role": "user", "content": user_input}
        ],
        temperature=0.9,
        max_tokens=300
    )

    hamlet_response = response.choices[0].message.content.strip()

    # Automatski generiši KMVM tagove
    kmvm_tags = extract_kmvm(user_input, hamlet_response)

    # Dodaj u memoriju
    kmvm_memory.append({
        "kreator": kmvm_tags["kreator"],
        "motiv": kmvm_tags["motiv"],
        "vreme": kmvm_tags["vreme"],
        "mesto": kmvm_tags["mesto"],
        "input": user_input,
        "response": hamlet_response
    })

    return hamlet_response
