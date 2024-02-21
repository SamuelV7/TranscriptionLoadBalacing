# FROM python:buster

# WORKDIR /app
# COPY ./main.py ./
# COPY ./requirements.txt ./

# RUN pip install -r requirements.txt
# RUN pip install "uvicorn[standard]" uvloop

# EXPOSE 80

# ENTRYPOINT ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "80"]

FROM ghcr.io/ggerganov/whisper.cpp:main as base

FROM python:latest as dev
COPY --from=base /app /app

WORKDIR /app
EXPOSE 8080
