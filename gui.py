import streamlit as st
import socket
import platform

from function.stt import stt as stt_gui
from function.pseudonymizer import pseudonymizer as pseudon_gui
from function.explain import explain as explain_gui

# Streamlit App
st.set_page_config(page_title="AI Toolbox", layout="wide", page_icon="🤖")



# # --- Node details ---
# hostname = socket.gethostname()
# try:
#     ip_address = socket.gethostbyname(hostname)
# except Exception:
#     ip_address = "Unknown"



# container = st.container(border=True)
# container.write("🖥️ Node details")
# container.write(hostname)
# container.write(ip_address)


try:
    import psutil
except ImportError:
    psutil = None

def system_panel():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "Unknown"

    with st.container(border=True):
        st.write("🖥️ Node details")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Hostname**")
            st.code(hostname)
            st.write("**IP address**")
            st.code(ip_address)
            st.write("**OS**")
            st.code(f"{platform.system()} {platform.release()}")

        with col2:
            st.write("**Python**")
            st.code(platform.python_version())
            if psutil:
                st.write("**CPU cores**")
                st.code(psutil.cpu_count(logical=True))
                mem = psutil.virtual_memory()
                st.write("**Memory (GB)**")
                st.code(round(mem.total / (1024**3), 2))
            else:
                st.write("_Install `psutil` for more metrics_")


st.title("AI Tools 📝")

tab1, tab2, tab3 = st.tabs(["Speech to Text 🎙️", "Pseudonymizer 🎭", "Explain 🤔"])

with tab1:
    stt_gui(display=True, label_prefix='stt')
with tab2:
    pseudon_gui()
# with tab3:
#     explain_gui()

