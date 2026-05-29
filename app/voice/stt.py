import speech_recognition as sr


def speech_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("🎤 Habla ahora...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)
    
    try:

        text = recognizer.recognize_google(
            audio,
            language="es-ES"
        )

        return text

    except Exception:

        return ""