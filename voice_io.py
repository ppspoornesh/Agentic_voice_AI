import time
import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3

offline_engine = pyttsx3.init()
offline_engine.setProperty("rate", 165)


def get_voice_input(language="te-IN", retries=2):
    r = sr.Recognizer()

    for _ in range(retries):
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=8)
                return r.recognize_google(audio, language=language)
            except:
                time.sleep(0.5)

    return None


def speak_text(text, language="te"):
    file = f"out_{int(time.time()*1000)}.mp3"

    try:
        gTTS(text=text, lang=language).save(file)
        play(AudioSegment.from_mp3(file))
        return
    except:
        pass
    finally:
        if os.path.exists(file):
            os.remove(file)

    try:
        offline_engine.say(text)
        offline_engine.runAndWait()
    except:
        print("[AGENT]:", text)
