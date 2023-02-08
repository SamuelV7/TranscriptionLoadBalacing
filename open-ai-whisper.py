import whisper

def transcribe(audio_file_path: str) -> str:
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_path, language='en')
    return result["text"]