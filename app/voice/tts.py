from gtts import gTTS
import tempfile
import re


def clean_text(text):
    text = re.sub(r"#|\*|\||-|`", " ", text)
    text = re.sub(r"\n+", ". ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def text_to_audio(text):
    clean = clean_text(text)

    if len(clean) > 1200:
        clean = clean[:1200]

    tts = gTTS(
        text=clean,
        lang="es"
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_file.name)

    return temp_file.name