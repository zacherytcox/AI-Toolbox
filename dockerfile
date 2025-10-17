# syntax=docker/dockerfile:1.7-labs
FROM python:3.10

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    g++

RUN pip install --upgrade pip setuptools wheel cython

# RUN pip install spacy -vvv

ENV TZ=America/New_York

WORKDIR /app

COPY --exclude=files* --exclude=.venv* . .

RUN chmod -R 777 /app

RUN bash build_docker_image.sh

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT /bin/sh -c "cron; streamlit run gui.py --server.address=0.0.0.0 --server.port=8501 --browser.gatherUsageStats false"
# ENTRYPOINT ["streamlit", "run", "gui.py", "--server.address=0.0.0.0", "--server.port=8501", "--browser.gatherUsageStats", "false"]