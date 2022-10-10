import os
from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import whisper


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def transcribe(audio_file_path):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_path)
    return result["text"]


def open_results(file_path):
    with open(file_path, "r") as f:
        text = f.read()
        return text


def save_file(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)


def split_into_chunks(long_string: str, per_period: int):
    split_string = long_string.split(".")
    processed_text = ""
    string_into_chunks = ""
    new_paragraph = False
    for index, the_string in enumerate(split_string):
        if new_paragraph:
            if len(the_string) < 1:
                continue
            if the_string[0] == " " and len(the_string) > 0 :
                the_string = the_string[1::]
            new_paragraph = False
        processed_text = processed_text + the_string + "."
        if index % per_period == 0 or index+per_period > (len(long_string)-1):
            string_into_chunks += processed_text + "\n"
            new_paragraph = True
            processed_text = ""

    return string_into_chunks

# item = open_results("results/mike.md")
# splitted = split_into_chunks(item, 7)
#
# print(splitted)
# save_file("results/mike-medium.txt", text)