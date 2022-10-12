from dataclasses import dataclass
import os
from typing import Union
# from fastapi import FastAPI
# from fastapi.responses import FileResponse
# import requests
# import whisper


# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# def transcribe(audio_file_path):
#     model = whisper.load_model("medium")
#     result = model.transcribe(audio_file_path)
#     return result["text"]


def open_results(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        return text


def save_file(file_name, text):
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(text)

@dataclass
class Sermon:
    name: str
    transcript: str

def batch_transcribe(locations_of_sermons):
    files = os.listdir(locations_of_sermons)
    sermons_audios = [file for file in files if file.endswith(".mp3")]
    print("Starting Transcription...")
    for sermon_audio in sermons_audios:
        print("Transcribing Sermon "+ sermon_audio)
        sermon = Sermon(sermon_audio[:-4], transcribe("mp3/"+sermon_audio))
        sermon.transcript = "# "+ sermon.name + "\n" + sermon.transcript
        print("Saving")
        save_file("results/"+sermon.name+".md", sermon.transcript)
        print("Save successful")


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

def divide_into_paragraphs(long_text : str, lines_per_paragraph:int):
    text_arr = long_text.split(".")
    stripped_space = [text.strip() for text in text_arr]
    formatted_text = ""

    for index, sentence in enumerate(stripped_space):
        if index == 0:
            formatted_text += sentence + ". "
            continue
        if index % lines_per_paragraph == 0 or index + lines_per_paragraph > (len(long_text)):
            formatted_text += "\n" + "\n"
        formatted_text += sentence + ". "
    return formatted_text

def fixing_formats(text: str):
    md = text.split("---")
    sermon_text = md[2]
    fixed_fromat = divide_into_paragraphs(sermon_text, 5)
    output = "---\n" + md[1] + "---\n" + fixed_fromat
    return output

def fix_formatting():
    file_list = os.listdir("frontend\content\posts")
    files = [file for file in file_list if file != "first.md"]
    for file in files:
        fixed = fixing_formats(open_results("frontend/content/posts/"+file))
        save_file("frontend/content/posts/"+file, fixed) 
    # to_save = fixing_formats(open_results("frontend\content\posts/"+files[0]))
    # save_file("test1.md", to_save)

fix_formatting()
get_text = open_results("results\Church in a World Gone Mad - Titus 1_1-4.md")
formatted_text = divide_into_paragraphs(get_text, 7)
save_file("test.md", formatted_text)
# item = open_results("results/mike.md")
# splitted = split_into_chunks(item, 7)
#
# print(splitted)
# save_file("results/mike-medium.md", text)