from enum import Enum
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

import main


class Models(Enum):
    Nllb200 = "facebook/nllb-200-distilled-600M"
    Helsinki = "Helsinki-NLP/opus-mt-en-es"
    M2m100_testing = 4

def translate_helsinki_opus(text: str):
    model_checkpoint = "Helsinki-NLP/opus-mt-en-es"
    translator = pipeline("translation", model=model_checkpoint)
    return translator(text)

# translate function above is better, this is nllb-200 and results are not great
def translate_nllb_model(text: str):
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    inputs = tokenizer(text, return_tensors="pt")

    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["spa_Latn"],
                                       max_length=1000)
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

text = main.open_results("frontend/content/posts/first.md")[0:1000]
print(text)
result = translate_helsinki_opus(text)
print(result)
# main.save_file("test.md", result)
