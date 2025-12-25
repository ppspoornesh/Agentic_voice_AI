import time
import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3

# Offline TTS engine as a fallback when online TTS fails
offline_engine = pyttsx3.init()
offline_engine.setProperty("rate", 165)


def get_voice_input(language="te-IN", retries=2):
    """
    Captures voice input from the microphone and converts it to text.
    Retries a few times to handle background noise or recognition failure.
    """
    r = sr.Recognizer()

    for _ in range(retries):
        with sr.Microphone() as source:
            # Adjust microphone sensitivity based on ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=8)
                return r.recognize_google(audio, language=language)
            except:
                # Retry in case of timeout or recognition error
                time.sleep(0.5)

    return None


def speak_text(text, language="te"):
    """
    Converts text to speech and plays it back to the user.
    Tries online TTS first and falls back to offline TTS if needed.
    """
    file = f"out_{int(time.time() * 1000)}.mp3"

    try:
        # Online TTS using Google Text-to-Speech
        gTTS(text=text, lang=language).save(file)
        play(AudioSegment.from_mp3(file))
        return
    except:
        pass
    finally:
        # Clean up temporary audio file
        if os.path.exists(file):
            os.remove(file)

    try:
        # Offline TTS fallback
        offline_engine.say(text)
        offline_engine.runAndWait()
    except:
        # Final fallback for debugging
        print("[AGENT]:", text)
