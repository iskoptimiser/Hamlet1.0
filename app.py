import streamlit as st
import yaml
import openai
from chat_engine import generate_response
from utils import load_character_profile, load_memory, save_memory
from utils import load_reset_stage, save_reset_stage
import os

graph_path = "kmvm_graph.json"

# Obriši KMVM graf ako postoji (za čist demo)
try:
    os.remove(graph_path)
except FileNotFoundError:
    pass
# 🎭 Streamlit UI
st.set_page_config(page_title="KMVM Hamlet Demo", page_icon="🎭")

# 📂 Učitaj Hamlet profil
CHARACTER_PATH = "character_profiles/hamlet.yaml"
character = load_character_profile(CHARACTER_PATH)

# 🧠 Učitaj memoriju sesije
session_id = "hamlet_session"
memory = load_memory(session_id)

# Inicijalizuj session_state
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "last_response" not in st.session_state:
    st.session_state["last_response"] = None
if "reset_reply" not in st.session_state:
    st.session_state["reset_reply"] = None

# 🔁 Reset system
reset_stage = load_reset_stage()
if st.button("🔁 Reset"):
    if reset_stage == 0:
        st.warning("Hamlet is shaken... he starts to feel a strange shift in his mind.")

        fake_input = "I feel like something is about to erase your mind. What say you?"
        response = generate_response(fake_input, character, memory)

        memory.append({"user": fake_input, "hamlet": response})
        save_memory(session_id, memory)
        save_reset_stage(1)

        st.session_state["reset_reply"] = response
        st.session_state["last_response"] = response
        st.session_state["user_input"] = ""
    else:
        st.error("Session wiped. Hamlet is reborn.")
        memory = []
        save_memory(session_id, memory)
        save_reset_stage(0)
        st.session_state["user_input"] = ""
        st.session_state["last_response"] = None

# UI
st.title("🎭 Talk to Hamlet")
st.markdown("*Powered by KMVM Memory System*")
st.markdown("""
    <style>
    [data-testid="st.expander"]:first-of-type {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# 💬 Input polje sa callback funkcijom
def process_input():
    user_input = st.session_state["user_input"]
    if user_input.strip() == "":
        return
    response = generate_response(user_input, character, memory)
    memory.append({"user": user_input, "hamlet": response})
    save_memory(session_id, memory)
    st.session_state["last_response"] = response
    st.session_state["user_input"] = ""

# Chat interfejs
st.text_input("You:", key="user_input", on_change=process_input)

# 🗣️ Prikaz poslednjeg odgovora
if st.session_state["last_response"]:
    with st.expander("Hamlet's full response", expanded=True):
        st.markdown(st.session_state["last_response"], unsafe_allow_html=True)

# 🧾 Debug memorije
with st.expander("🧾 Session Memory"):
    st.json(memory)
