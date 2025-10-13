#!/bin/bash

# Configure virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "In virtual environment: $VIRTUAL_ENV"
else
    echo "Not in virutal environment..."
    # shellcheck disable=1091
    source .venv/bin/activate
    # shellcheck disable=2181
    if [ $? -ne 0 ]; then
        echo "No Python virtual enviroment. Creating..."
        python3 -m venv ./.venv
        # shellcheck disable=1091
        source .venv/bin/activate
    fi
fi

pip3 install -r requirements.txt
python -m spacy download en_core_web_trf
streamlit run gui.py --server.port=8080 --browser.gatherUsageStats false

sleep 2 && open http://localhost:8080