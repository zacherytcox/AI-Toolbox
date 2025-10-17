# syntax=docker/dockerfile:1.7-labs
FROM python:latest

RUN apt-get update

RUN apt install build-essential python3-dev -y

ENV TZ=America/New_York

WORKDIR /app

COPY --exclude=files* --exclude=.venv* . .

RUN chmod -R 777 /app

RUN bash build_docker_image.sh

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT /bin/sh -c "cron; streamlit run gui.py --server.address=0.0.0.0 --server.port=8501 --browser.gatherUsageStats false"
# ENTRYPOINT ["streamlit", "run", "gui.py", "--server.address=0.0.0.0", "--server.port=8501", "--browser.gatherUsageStats", "false"]