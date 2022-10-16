from dataclasses import dataclass
import os
# import requests
import whisper
from datetime import datetime
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


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
        print("Transcribing Sermon " + sermon_audio)
        sermon = Sermon(sermon_audio[:-4], transcribe("mp3/" + sermon_audio))
        sermon.transcript = "# " + sermon.name + "\n" + sermon.transcript
        print("Saving")
        save_file("results/" + sermon.name + ".md", sermon.transcript)
        print("Save successful")


def divide_into_paragraphs(long_text: str, lines_per_paragraph: int):
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


def formats_existing_text(text: str):
    md = text.split("---")
    sermon_text = md[2]
    fixed_format = divide_into_paragraphs(sermon_text, 5)
    output = "---\n" + md[1] + "---\n" + fixed_format
    return output


def fix_formatting():
    file_list = os.listdir("frontend\content\posts")
    files = [file for file in file_list if file != "first.md"]
    for file in files:
        fixed = formats_existing_text(open_results("frontend/content/posts/" + file))
        save_file("frontend/content/posts/" + file, fixed)
        # to_save = fixing_formats(open_results("frontend\content\posts/"+files[0]))
    # save_file("test1.md", to_save)

def create_content_for_hugo(title: str, draft: str):
    the_date = datetime.now()
    formatted_date = the_date.strftime("%Y-%m-%d")
    return "---\n" + title + "\n" + formatted_date +"\n"+ "draft: " + draft + " ---\n"

def transcribe_low_level(audio_locations: str):
    model = whisper.load_model("medium")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_locations)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    # print the recognized text
    return result.text

def transcribe_save(audio_location: str):
    sermon = transcribe(audio_location)
    name = audio_location.split(".")[0]
    paragraphed = divide_into_paragraphs(sermon, 7)
    hugo_metadata = create_content_for_hugo(name, "false")

    save_file("results/"+name+".md", hugo_metadata+paragraphed)

transcribe_save("Transformed Priorities for Young Men.mp3")
# fix_formatting()
# get_text = open_results("results\Church in a World Gone Mad - Titus 1_1-4.md")
# formatted_text = divide_into_paragraphs(get_text, 7)
# save_file("test.md", formatted_text)

# item = open_results("results/mike.md")
# splitted = split_into_chunks(item, 7)
#
# print(splitted)
# save_file("results/mike-medium.md", text)
