import streamlit as st
import random
import time
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

def get_stt_model_selection(ss=st.session_state, label_prefix=None):
    if not label_prefix:
        label_prefix = str(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
    with st.popover("STT Model Select"):
        st.radio(
            label=str(label_prefix) + "radio",
            options=['turbo', 'large-v3-turbo', 'large-v3', 'large', 'medium', 'medium.en', 'small', 'base', 'tiny'],
            label_visibility='collapsed',
            key=str(label_prefix) + "radio"
        )
        return getattr(ss, str(label_prefix) + "radio")
    
def get_text_from_audio(ss=st.session_state, label_prefix=None, audio_value=None, this_model=None, debug=False):
    import tempfile
    import whisper
    if not label_prefix:
        label_prefix = str(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
    if debug:
        st.toast(label_prefix)
        st.toast(ss)
        st.toast(audio_value)
        st.toast(this_model)
    if getattr(ss, str(label_prefix) + 'process_stt'):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
            if audio_value == None or this_model == None:
                return None
            tmp.write(audio_value.read())
            tmp_path = tmp.name
            if tmp_path:
                msg = f"Loading Model {this_model}"
                with st.spinner(msg, show_time=True):
                    this_model = whisper.load_model(this_model)
                try:
                    msg = f"Transcribing Audio..."
                    with st.spinner(msg, show_time=True):
                        result = this_model.transcribe(audio=tmp_path)
                except Exception as e:
                    msg = f"Issue with transcribing, {e}"
                    st.text(msg)
                    result = {'text': 'error'}
                return result['text']


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
        this_model = get_stt_model_selection(st.session_state, label_prefix)

    with col2:
        if str(label_prefix) + 'audio_value' not in st.session_state:
            setattr(st.session_state, str(label_prefix) + 'audio_value', None)
        if str(label_prefix) + 'result_data' not in st.session_state:
            setattr(st.session_state, str(label_prefix) + 'result_data', None)
        if str(label_prefix) + 'process_stt' not in st.session_state:
            setattr(st.session_state, str(label_prefix) + 'process_stt', False)

        def added_audio():
            setattr(st.session_state, str(label_prefix) + 'process_stt', True)

        if st.audio_input(label=label_prefix+"audio_input", key=label_prefix+"audio_input", label_visibility='collapsed', on_change=added_audio):
            audio_value = getattr(st.session_state, label_prefix+"audio_input")

            if display:
                st.text(f"{bytes_to_megabytes(int(audio_value.size))}")
                st.audio(audio_value)

            this_text = get_text_from_audio(ss=st.session_state, label_prefix=label_prefix, audio_value=audio_value, this_model=this_model)
            setattr(st.session_state, str(label_prefix) + 'result_data', this_text)     
            setattr(st.session_state, str(label_prefix) + 'process_stt', False)

    if getattr(st.session_state, str(label_prefix) + 'result_data'):

        if display:
            st.text(getattr(st.session_state, str(label_prefix) + 'result_data'))
        else:
            return getattr(st.session_state, str(label_prefix) + 'result_data')
        
        
if __name__ == "__main__":
    stt()