import streamlit as st
import whisper
import tempfile
import random
import string


def bytes_to_megabytes(nbytes: int, binary: bool = True, precision: int = 2) -> str:
    """
    Convert a byte count to a human‑readable megabyte string.

    Parameters
    ----------
    nbytes : int
        The number of bytes.
    binary : bool, optional
        If True return MiB (1024‑based), otherwise MB (1000‑based). Default True.
    precision : int, optional
        Number of decimal places. Default 2.

    Returns
    -------
    str
        Formatted string like '4.00 MiB' or '4.19 MB'.
    """
    factor = 1024 ** 2 if binary else 1_000_000
    value = nbytes / factor
    unit = "MiB" if binary else "MB"
    return f"{value:.{precision}f} {unit}"

def stt(display=False, label_prefix=None):
    if not label_prefix:
        label_prefix = str(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
    if display:
        st.title("🎙️ Speech to Text")
        st.markdown(
            """
            Perform local Speech to Text. Does not send audio to external server for processing. Maximum Privacy.
            """
        )
    col1, col2 = st.columns([1, 7])
    with col1:
        with st.popover("STT Model Select"):
            this_model = st.radio(
                label=str(label_prefix) + "radio",
                options=['turbo', 'large-v3-turbo', 'large-v3', 'large', 'medium', 'medium.en', 'small', 'base', 'tiny'],
                label_visibility='collapsed',
            )
            # this_model = st.selectbox("Select model for processing", ['turbo', 'large-v3-turbo', 'large-v3', 'large', 'medium', 'medium.en', 'small', 'base', 'tiny'])
    with col2:
        audio_value = st.audio_input(label=label_prefix+"audio_input", label_visibility='collapsed')

    if audio_value:
        if display:
            st.text(f"{bytes_to_megabytes(int(audio_value.size))}")
            st.audio(audio_value)

        model = whisper.load_model(this_model)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_value.read())
            tmp_path = tmp.name
            result = model.transcribe(tmp_path)
        if display:
            st.text(result["text"])
        else:
            return result["text"]

if __name__ == "__main__":
    stt()