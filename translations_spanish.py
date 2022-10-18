from enum import Enum
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

class Models(Enum):
    Nllb200 = "facebook/nllb-200-distilled-600M"
    Helsinki = "Helsinki-NLP/opus-mt-en-es"
    M2m100_testing = 4

def translate_helsinki_opus(text: str):
    model_checkpoint = "Helsinki-NLP/opus-mt-en-es"
    translator = pipeline("translation", model=model_checkpoint)
    output = translator(text)
    return output[0]['translation_text']

# translate function above is better, this is nllb-200 and results are not great
def translate_nllb_model(text: str):
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
    inputs = tokenizer(text, return_tensors="pt")
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["spa_Latn"],
                                       max_length=1000)
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]


def split_into_sentence_with_max_limit(limit: int, sentence: str):
    if len(sentence) < limit:
        return [sentence]
    sentence_split = sentence.split(".")
    total_in_chunk = 0
    temp_sentence = []
    sentence_arr = []
    print("Sentence split len : ", len(sentence_split))
    for the_sentence in sentence_split:
        if len(the_sentence) + total_in_chunk > limit:
            sentence_arr.append(temp_sentence)
            temp_sentence = [the_sentence+"."]
            total_in_chunk = len(the_sentence)

        if total_in_chunk == limit:
            sentence_arr.append(temp_sentence+".")
            temp_sentence = []
            total_in_chunk = 0

        if total_in_chunk < limit:
            temp_sentence.append(the_sentence+".")
            total_in_chunk += len(the_sentence)
    array_of_strings = ["".join(item) for item in sentence_arr]
    return array_of_strings

# def array_of_arrays_into_string_array

def translate_large(large_text):
    translatable_chunk = split_into_sentence_with_max_limit(400, large_text)
    # [chunk['translation_text'] for chunk in translatable_chunk]
    translated = []
    for chunk in translatable_chunk:
        translation = translate_helsinki_opus(chunk)[0]
        translated.append(translation['translation_text'])
    return translated

# print(text)
# result = translate_helsinki_opus(text)
# print(result)
# main.save_file("test.md", result)
