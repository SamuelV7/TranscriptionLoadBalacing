FROM python:latest as base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get update --fix-missing
# RUN apt-get install deb-multimedia-keyring 
RUN apt-get install -y --no-install-recommends ffmpeg 
RUN rm -rf /var/lib/apt/lists/*


WORKDIR /workspace/
COPY . .

RUN pip install poetry 
RUN pwd && ls
RUN poetry config virtualenvs.create false
RUN poetry install
# RUN poetry install

# CMD ["poetry", "run", "python", "main.py"]
# Run forever
# CMD ["sleep", "infinity"]
