from typing import Union
# from fastapi import FastAPI
import requests
import whisper

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

def transcribe(audio_file_path):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_path)
    return result["text"]

text = transcribe("mike.mp3")

def save_file(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)

save_file("results/mike-medium.txt", text)