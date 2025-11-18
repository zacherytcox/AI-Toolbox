import streamlit as st
import socket

from function.stt import stt as stt_gui
from function.pseudonymizer import pseudonymizer as pseudon_gui
from function.explain import explain as explain_gui

# Streamlit App
st.set_page_config(page_title="AI Toolbox", layout="wide", page_icon="🤖")



# --- Node details ---
hostname = socket.gethostname()
try:
    ip_address = socket.gethostbyname(hostname)
except Exception:
    ip_address = "Unknown"

# --- Persistent top-right badge ---
st.markdown(
    f"""
    <style>
    .node-popup {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 9999;
        background-color: #262730;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        font-size: 0.85rem;
        max-width: 260px;
    }}
    .node-popup-title {{
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}
    .node-popup-line {{
        margin: 0;
    }}
    </style>
    <div class="node-popup">
        <div class="node-popup-title">🖥️ Node details</div>
        <p class="node-popup-line"><strong>Host:</strong> {hostname}</p>
        <p class="node-popup-line"><strong>IP:</strong> {ip_address}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.title("AI Tools 📝")

tab1, tab2, tab3 = st.tabs(["Speech to Text 🎙️", "Pseudonymizer 🎭", "Explain 🤔"])

with tab1:
    stt_gui(display=True, label_prefix='stt')
with tab2:
    pseudon_gui()
# with tab3:
#     explain_gui()

