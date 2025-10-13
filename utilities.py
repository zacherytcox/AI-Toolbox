import streamlit as st
import ollama
import requests
import datetime
from httpx import ConnectError, ConnectTimeout


def get_long_link(short_url):
    try:
        response = requests.get(short_url, allow_redirects=True, timeout=5)
        # The final URL after all redirects is stored in response.url
        full_url = response.url
        print(f"Original URL: {short_url}")
        print(f"Full Link: {full_url}")
        return full_url
    except requests.exceptions.RequestException as e:
        print(f"Failed to expand the URL: {e}")
        return short_url


def select_ollama_model(accuracy: str = "l") -> str:
    """
    Select the appropriate Ollama model based on the desired accuracy.

    Args:
        accuracy (str): The desired accuracy level. Can be 'h', 'm', or anything else.

    Returns:
        str: The selected Ollama model name.
    """
    if accuracy == "h":
        return "gemma3:27b"
    elif accuracy == "m":
        return "gemma3:12b"
    else:
        return "gemma3:4b"


def get_ollama_client(remote_ollama_url: str = None) -> ollama.Client:
    """
    Get an Ollama client instance.

    Args:
        remote_ollama_url (str): The URL of the remote Ollama server. If None, use the default local server.

    Returns:
        ollama.Client: An instance of the Ollama client.
    """
    default_ollama_client = ollama.Client()
    if remote_ollama_url is not None:
        try:
            # print(f"Checking: {remote_ollama_url}")
            this_client = ollama.Client(remote_ollama_url, timeout=2)
            response = this_client.list()
            # print(f"Found: {remote_ollama_url}")
            # return client that doesn't have a timeout
            return ollama.Client(remote_ollama_url)
        except (ConnectError, ConnectTimeout) as e:
            st.error(e)
            st.stop()
            pass
    return default_ollama_client


def pull_model(model: str, remote_ollama_url: str = None) -> bool:
    """
    Pull a model to the Ollama server.

    Args:
        model (str): The name of the model to pull.
        remote_ollama_url (str): The URL of the remote Ollama server. If None, use the default local server.

    Returns:
        bool: True if the model was successfully pulled, False otherwise.
    """
    try:
        client = get_ollama_client(remote_ollama_url)
        client.pull(model)
        return True
    except Exception as e:
        print(f"Error pulling model {model}: {e}")
        return False


def generate(
    prompt: str,
    model: str,
    temperature: float = 0.0,
    remote_ollama: str = None,
    think: bool = False,
    timeout: int = 10,
) -> str:
    import time

    # Check if the model exists on the Ollama server
    try:
        get_ollama_client(remote_ollama_url=remote_ollama).show(model)
    except ollama.ResponseError as e:
        print(f"Model {model} not found on Ollama server: {e}")
        if not pull_model(model, remote_ollama_url=remote_ollama):
            print(f"Failed to pull model {model}.")
            return "Model not found and failed to pull."

    this_client = get_ollama_client(remote_ollama_url=remote_ollama)
    processed = False
    count = 0
    output = {"response": None}
    while processed is False and count < 10:
        count += 1
        if count > 1:
            print(f"Trying again... {count}:{prompt}")
        try:
            output = this_client.generate(
                model=model,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": temperature,
                    "timeout": timeout,
                },
                think=think,
            )
            processed = True
            if think and model.startswith("qwen"):
                return output.response, output.thinking.replace('"', "'")
            else:
                return output.response
        except ollama.ResponseError as e:
            print(f"Error Ollama: {e}")
            time.sleep(10)
        except ollama.TimeoutError as e:
            print(f"Timeout Ollama: {e}")
            time.sleep(10)


def str_to_bool(value):
    if value in [True, False]:
        return value
    elif value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        print("defaulting bool")
        return False


def format_seconds_to_time(total_seconds):
    """
    Converts a given number of seconds into a human-readable string
    of weeks, days, hours, minutes, and seconds.
    """
    weeks = total_seconds // (7 * 24 * 3600)
    days = (total_seconds % (7 * 24 * 3600)) // (24 * 3600)
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if weeks > 0:
        parts.append(f"{weeks} Week{'s' if weeks != 1 else ''}")
    if days > 0:
        parts.append(f"{days} Day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} Hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} Minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} Second{'s' if seconds != 1 else ''}")

    return (
        " and ".join(parts)
        if len(parts) <= 2
        else ", ".join(parts[:-1]) + " and " + parts[-1]
    )


def get_desc_md(
    job_desc=None,
    remote_ollama=None,
    model="gemma3:4b",
    temperature=0.0,
):

    prompt = f"""
        Take the following block of text and convert it to Markdown format for easier readability.
        Do not modify any of the words in any way.
        Output solely in Markdown.

        Job Description:
        {job_desc}
        """

    new_desc = generate(
        prompt, model=model, temperature=temperature, remote_ollama=remote_ollama
    )
    return new_desc.replace('"', "'")


def extract_raw_json(output: str) -> str:
    import re

    # Removes markdown code fences like ```json ... ```
    code_fence_pattern = r"```(?:json)?\n(.*?)\n```"
    if output:
        match = re.search(code_fence_pattern, output, re.DOTALL)
        return match.group(1).strip() if match else output.strip()
    else:
        print(output)
        return "None"
    

def send_discord_webhook(webhook_url, message, title="Job Alert", color=0x00FF00):
    """
    Send a message to Discord via webhook

    Args:
        webhook_url (str): Discord webhook URL
        message (str): Message content to send
        title (str): Title for the embed (optional)
        color (int): Color for the embed in hex (optional)

    Returns:
        bool: True if successful, False otherwise
    """
    if not webhook_url or webhook_url.strip() == "":
        return False

    try:
        # Truncate message if it exceeds Discord's limit
        if len(message) > 2000:
            message = message[:1997] + "..."

        # Truncate title if it exceeds Discord's limit
        if len(title) > 256:
            title = title[:253] + "..."

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": message,
                    "color": color,
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            ]
        }

        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord webhook: {e}")
        return False
