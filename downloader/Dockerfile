FROM python:latest as base

WORKDIR /workspace/
COPY . .

RUN pip install poetry 
RUN poetry config virtualenvs.create false
RUN poetry install
# RUN poetry install

# CMD ["poetry", "run", "python", "main.py"]
# Run forever
# CMD ["sleep", "infinity"]
