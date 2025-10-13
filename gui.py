import streamlit as st

from function.stt import stt as stt_gui
from function.pseudonymizer import pseudonymizer as pseudon_gui
from function.explain import explain as explain_gui

# Streamlit App
st.set_page_config(page_title="AI Toolbox", layout="wide", page_icon="🤖")

st.title("AI Tools 📝")

tab1, tab2, tab3 = st.tabs(["Speech to Text 🎙️", "Pseudonymizer 🎭", "Explain 🤔"])

with tab1:
    stt_gui(display=True, label_prefix='stt')
with tab2:
    pseudon_gui()
with tab3:
    explain_gui()

